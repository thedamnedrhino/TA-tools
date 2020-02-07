
def charint(char):
	return ord(char) - ord('A') + 1
def intchar(integer):
	return chr(integer + ord('A') - 1)

class Column:
	def __init__(self, text=None, _num=None):
		self.text = text
		self.num = None if _num is None else self._fix_num(_num)
		self.initialize()

	def _fix_num(self, num):
		# turn 0s into 1s
		order = 1
		fixed = 0
		while num > 0:
			modul = num % self._alphabet_range()
			modul = 1 if modul == 0 else modul
			fixed += modul*order
			order *= self._alphabet_range()
			num /= self._alphabet_range()

		return fixed


	def _alphabet_range(self):
		return charint('Z') - charint('A') + 2

	def initialize(self):
		assert self.text is None or self.num is None
		if self.num is None:
			num = 0
			order = 1
			for i in range(len(self.text)):
				num *= self._alphabet_range()
				c = self.text[i]
				num += charint(c)
			assert num == self._fix_num(num), "{}, {}".format(num, self._fix_num(num))
			self.num = num
		else:
			text = ""
			if self.num == 0:
				self.text += intchar(0)
				return
			num = self.num
			while num > 0:
				text = intchar(num % self._alphabet_range()) + text
				num /= self._alphabet_range()
			self.text = text



	def absolute_reference(self, rownum):
		text = ""
		text = "${}${}".format(self.text, rownum) + text
		return text

	def relative_reference(self, rownum):
		return "{}{}".format(self.text, rownum)

	def next(self):
		return Column(_num=self.num+1)

	def leq(self, other):
		return self.num <= other.num

class FormulaGenerator:
	def __init__(self, valuerow=1, titlerow=2, markrow=3):
		self.valuerow = valuerow
		self.titlerow = titlerow
		self.markrow = markrow

	def generate_total(self, columns):
		text = ""
		for c in columns:
			text += "{}*{} +".format(c.absolute_reference(self.valuerow), c.relative_reference(self.markrow))

		return text.strip("+").strip()

	def generate_summary(self, columns, questionnumber=True, commentscolumn=None):
		c = columns[0]
		text = "{} & CHAR(10) & ".format(c.absolute_reference(self.titlerow)) if questionnumber else ""
		columns = columns[1:] if questionnumber else columns
		for c in columns:
			text += "{} & \": \" & {}*{} & \"/\" & {} & CHAR(10) & ".format(c.absolute_reference(self.titlerow), c.absolute_reference(self.valuerow), c.relative_reference(self.markrow), c.absolute_reference(self.valuerow))
		text =  text.strip(" & ")

		if commentscolumn:
			text += " & {} & CHAR(10)".format(commentscolumn.relative_reference(self.markrow))

		return text

class Columns:
	def __init__(self, start, end, exclude=[], include=[]):
		self.start = Column(text=start)
		self.end = Column(text=end)
		self.exclude = exclude
		self.include = include

	def get(self):
		l = []
		c = self.start
		while c.leq(self.end):
			if c.text not in self.exclude:
				l.append(c)
			c = c.next()
		l += [Column(text=x) for x in self.include]
		return l

	@staticmethod
	def comments_column(columntext):
		return Column(text=columntext)

if __name__ == '__main__':
	assert intchar(charint('A')) == 'A'
	fg = FormulaGenerator()
	columns = Columns('D', 'H', ['G', 'H']).get()
	assert fg.generate_total(columns) == "$D$1*D3 +$E$1*E3 +$F$1*F3", fg.generate_total(columns)
	assert fg.generate_summary(columns, commentscolumn=Column(text='AB')) =='$D$2 & CHAR(10) & $E$2 & ": " & $E$1*E3 & "/" & $E$1 & CHAR(10) & $F$2 & ": " & $F$1*F3 & "/" & $F$1 & CHAR(10) & AB3 & CHAR(10)', fg.generate_summary(columns, commentscolumn=Column(text='AB'))

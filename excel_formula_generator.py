
def charint(char):
	return ord(char) - ord('A')
def intchar(integer):
	return chr(integer + ord('A'))

class Column:
	def __init__(self, text=None, num=None):
		self.text = text
		self.num = num
		self.initialize()

	def _alphabet_range(self):
		return charint('Z') - charint('A') + 1

	def initialize(self):
		assert self.text is None or self.num is None
		if self.num is None:
			num = 0
			for i in range(len(self.text)):
				num *= self._alphabet_range()
				c = self.text[i]
				num += charint(c)
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
		return Column(num=self.num+1)

	def leq(self, other):
		return self.num <= other.num

class FormulaGenerator:
	def __init__(self, valuerow=1, titlerow=2, markrow=3):
		self.valuerow = valuerow
		self.titlerow = titlerow
		self.markrow = markrow

	def generate_total(self, startcolumn, endcolumn):
		c = startcolumn
		text = ""
		while c.leq(endcolumn):
			text += "{}*{} +".format(c.absolute_reference(self.valuerow), c.relative_reference(self.markrow))
			c = c.next()

		return text.strip("+").strip()

	def generate_summary(self, startcolumn, endcolumn, questionnumber=True):
		c = startcolumn
		text = "{} & CHAR(10) & ".format(c.absolute_reference(self.titlerow)) if questionnumber else ""
		if questionnumber:
			c = c.next()
		while c.leq(endcolumn):
			text += "{} & \": \" & {}*{} & \"/\" & {} & CHAR(10) & ".format(c.absolute_reference(self.titlerow), c.absolute_reference(self.valuerow), c.relative_reference(self.markrow), c.absolute_reference(self.valuerow))
			c = c.next()

		return text.strip(" & ")


if __name__ == '__main__':
	assert intchar(charint('A')) == 'A'
	fg = FormulaGenerator()
	s = Column(text='D')
	e = Column(text = 'F')
	assert fg.generate_total(s, e) == "$D$1*D3 +$E$1*E3 +$F$1*F3", fg.generate_total(s, e)
	assert fg.generate_summary(s, e) =='$D$2 & CHAR(10) & $E$2 & ": " & $E$1*E3 & "/" & $E$1 & CHAR(10) & $F$2 & ": " & $F$1*F3 & "/" & $F$1 & CHAR(10)', fg.generate_summary(s, e)

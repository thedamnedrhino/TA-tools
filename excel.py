"""
The command file for excel_formula_generator
"""
import argparse
from excel_formula_generator import *


if __name__ == '__main__':
	parser = argparse.ArgumentParser('generate excel cell formulas for grading')
	parser.add_argument('command', choices=['total', 'summary'])
	parser.add_argument('startcolumn')
	parser.add_argument('endcolumn')
	parser.add_argument('--exclude', nargs='+', required=False, default=[])
	parser.add_argument('--include', nargs='+', required=False, default=[])
	parser.add_argument('--total', required=False, default=None)
	parser.add_argument('--comments', required=False, default=None)
	parser.add_argument('--bonus', required=False, default=None)
	parser.add_argument('--nq', '--no-question-number', required=False, default=False, action='store_true', dest='noquestion')
	parser.add_argument('--value-row', default=2)
	parser.add_argument('--title-row', default=3)
	parser.add_argument('--mark-row', default=4)
	args = parser.parse_args()

	columns = Columns(args.startcolumn, args.endcolumn, exclude=args.exclude, include=args.include).get()
	fg = FormulaGenerator(valuerow=args.value_row, titlerow=args.title_row, markrow=args.mark_row)
	if args.command == 'total':
		print(fg.generate_total(columns))
	elif args.command == 'summary':
		totalcolumn = None if args.total is None else Columns.column(args.total)
		commentscolumn = None if args.comments is None else Columns.comments_column(args.comments)
		bonuscolumn = None if args.bonus is None else Columns.bonus_column(args.bonus)
		print(fg.generate_summary(columns, questionnumber=(not args.noquestion), totalcolumn=totalcolumn, commentscolumn=commentscolumn, bonuscolumn=bonuscolumn))

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
	parser.add_argument('--comments', required=False, default=None)
	parser.add_argument('--nq', '--no-question-number', required=False, default=False, action='store_true', dest='noquestion')
	args = parser.parse_args()

	columns = Columns(args.startcolumn, args.endcolumn, exclude=args.exclude, include=args.include).get()
	fg = FormulaGenerator()
	if args.command == 'total':
		print(fg.generate_total(columns))
	elif args.command == 'summary':
		commentscolumn = None if args.comments is None else Columns.comments_column(args.comments)
		print(fg.generate_summary(columns, questionnumber=(not args.noquestion), commentscolumn=commentscolumn))

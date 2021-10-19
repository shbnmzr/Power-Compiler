import re
from .Lexer import Lexer
from .Code import Code
from .Semanter import Semanter
from .Parser import Parser
import sys
import os
class Power:
	def __init__(self,FileAddr):
		Fh = open(FileAddr)
		self.Code = Code(FileAddr)
		self.Lexer = Lexer(self.Code)
		self.Parser = Parser(self.Lexer,os.path.dirname(os.path.abspath(__file__))+"\..\\data\\ParsingTable.csv")
		self.Semanter = Semanter(open(self.Code.FileAddress))

	def Run(self):
		try:
			if self.Parser.Parse():
				self.Semanter.Evaluator()
			else:
				print("Parsing Process Faild")	
		except ValueError:
			print("Parsing Process Faild")
			sys.exit()
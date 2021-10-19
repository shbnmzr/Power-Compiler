from . import Constants
from .Token import Token
from .Error import LexicalError
from .Code import Code

class Lexer:
	'''
	Lexer Stand alone Class

	Attributes
	----------
		Tokenized : bool
			A boolean attribute that prevents a code from repeatative Tokenization.
		CurrentToken : int
			Current Token id used with "Tokens".
		Tokens : list
			List contains a sort of "Token" class instances. 
		Code : Code
			an instance of Code class from user input



	Methods
	-------
		Tokenizer():
			Extracts language tokens from user's input code and updates "Tokens" attribute.
		GetNextToken():
			Returns instance of Token class for the very next token (None for n+1).
		LastTokenRetrived():
			Returns instance of Token class for last token returned by GetNextToken method.
		ResetTokenPointer():
			Sets CurrentToken attribute to 0.
		SetTokenPointer(n):
			Sets CurrentToken to n.

	'''
	def __init__(self,Code):
		self.Tokenized = False
		self.CurrentToken = 0
		self.LineNumber = 1
		self.Tokens = []
		self.Code = Code

	def Tokenizer(self):
		if self.Tokenized is True:return False
		'''
			Extracts language tokens from user's input code.
			Then updates "Tokens" attribute.

			Parameters:
					Code

			Returns:
					None
		'''
		for Line in self.Code.PowerCode.splitlines():
			if Line.startswith("//"): continue
			for ProbableToken in Line.split(" "):
				if ProbableToken in "\t\n ": continue
				ProbableToken = ProbableToken.strip()
				if ProbableToken == '//': break
				if ProbableToken in Constants.Keywords:
					self.Tokens.append(Token("KEYWORD", ProbableToken))
				elif ProbableToken in Constants.Operators:
					self.Tokens.append(Token("OPERATOR", ProbableToken))
				elif ProbableToken in "[]{}()=,^":
					self.Tokens.append(Token("DELIMITER", ProbableToken))
				elif ProbableToken.isdigit():
					self.Tokens.append(Token("INTEGER", ProbableToken))
				elif ProbableToken.count('.') == 1 and ProbableToken.replace(".","").isdigit():
					self.Tokens.append(Token("FLOAT", ProbableToken))
				elif ProbableToken[0] == '"' and ProbableToken[-1] == '"':
					if len(ProbableToken) == 3:
						self.Tokens.append(Token("CHAR", ProbableToken))
					else:
						self.Tokens.append(Token("STRING", ProbableToken))
				else:
					if ProbableToken.startswith('&'):
						self.Tokens.append(Token("SPECIALCHAR", '&'))
						ProbableToken = ProbableToken[1:]
					if ProbableToken.replace('_','').isalnum() and not ProbableToken[0].isdigit() :
						self.Tokens.append(Token("IDENTIFIER", ProbableToken))
					else:
						#print(LexicalError(self.LineNumber, ProbableToken))
						pass
			self.LineNumber += 1

		self.Tokenized = True

	def GetNextToken(self):
		'''
			Returns instance of Token class for the very next token (None for n+1).

			Parameters:
				None

			Returns:
				self.Tokens[self.CurrentToken - 1]
		'''
		if self.Tokenized is False: self.Tokenizer()
		self.CurrentToken += 1
		if self.CurrentToken <= len(self.Tokens):
			return self.Tokens[self.CurrentToken - 1]
		else:
			return None
			
	def ReturnNextToken(self):
		if self.CurrentToken <= len(self.Tokens):
			return self.Tokens[self.CurrentToken - 1]
		else:
			return None

	def LastTokenRetrived(self):
		return self.Tokens[self.CurrentToken]

	def ResetTokenPointer(self):
		self.CurrentToken = 0

	def SetTokenPointer(self,n):
		if n <= len(self.Tokens): self.CurrentToken = n

	@classmethod
	def LexLine(self, Text):
		LineTokens = []
		Text = Code.TrimLine(Text)
		for ProbableToken in Text.split(" "):
			if ProbableToken in "\t\n ": continue
			ProbableToken = ProbableToken.strip()
			if ProbableToken == '//': break
			if ProbableToken in Constants.Keywords:
				LineTokens.append(Token("KEYWORD", ProbableToken))
			elif ProbableToken in Constants.Operators:
				LineTokens.append(Token("OPERATOR", ProbableToken))
			elif ProbableToken in "[]{}()=,^":
				LineTokens.append(Token("DELIMITER", ProbableToken))
			elif ProbableToken.isdigit():
				LineTokens.append(Token("INTEGER", ProbableToken))
			elif ProbableToken.count('.') == 1 and ProbableToken.replace(".","").isdigit():
				LineTokens.append(Token("FLOAT", ProbableToken))
			elif ProbableToken[0] == '"' and ProbableToken[-1] == '"':
				if len(ProbableToken) == 3:
					LineTokens.append(Token("CHAR", ProbableToken))
				else:
					LineTokens.append(Token("STRING", ProbableToken))
			else:
				if ProbableToken.startswith('&'):
					LineTokens.append(Token("SPECIALCHAR", '&'))
					ProbableToken = ProbableToken[1:]
				if ProbableToken.replace('_','').isalnum() and not ProbableToken[0].isdigit() :
					LineTokens.append(Token("IDENTIFIER", ProbableToken))
				else:
					#print(LexicalError(0, ProbableToken))
					pass
		return LineTokens
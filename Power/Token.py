class Token():
	'''
	Overall Structure of a Simple Token.

	Attributes
	----------
		Type : str
			Type of current token.
		Value : str
			Value of current token.
	'''
	def __init__(self, Type, Value):
		self.Type = Type
		self.Value = Value
	def __str__(self):
		return "({},{})".format(self.Type,self.Value)
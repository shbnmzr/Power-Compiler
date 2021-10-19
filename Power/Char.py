class Char:
	def __init__(self, Character):
		if len(Character) != 1:
			raise Exception("Character - String found instead!")
		self.ascii = ord(Character)
		self.char = Character

	def __str__(self):
		return self.char
	def __repr__(self):
		return self.char
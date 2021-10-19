import re
from .Constants import Exceptions

class Code:
	def __init__(self, FileAddr):
		self.FileAddress = FileAddr
		FileHandle = open(FileAddr,"r")
		self.RawCode = FileHandle.read()
		self.PowerCode = self.RawCode
		FileHandle.close()
		for Excepted in Exceptions:
			self.PowerCode = self.PowerCode.replace(Excepted, " {} ".format(Excepted))
		for ExtractedString in re.findall(r'\"(.+?)\"', self.PowerCode):
		    self.PowerCode = self.PowerCode.replace(ExtractedString, ExtractedString.replace(" ", "<S>"))
	
	@classmethod
	def TrimLine(self,Line):
		Line = str(Line)
		for Excepted in Exceptions:
			Line = Line.replace(Excepted, " {} ".format(Excepted))
		for ExtractedString in re.findall(r'\"(.+?)\"', Line):
		    Line = Line.replace(ExtractedString, ExtractedString.replace(" ", "<S>"))
		return Line

	def __str__(self):
		return "Instance code of {}".format(self.FileAddress)
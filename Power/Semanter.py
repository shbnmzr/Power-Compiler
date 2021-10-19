import re
import sys
from .Code import Code
from .Char import Char
from .Constants import Keywords
from io import StringIO
import contextlib

class Semanter:
	def __init__(self, fh):
		self.Equivalent = {
			"^":"",
			"Jam":"+",
			"Kam":"-",
			"Zarb":"*",
			"Tagsim":"/",
			"Ya":"or",
			"Va":"and",
			"&NM":"!=",
			"&MM": "==",
			"&B":">",
			"&K":"<",
			"Bagimande":"%",
			"Dorost":"True",
			"Qalat":"False",
			"Bemir": "sys.exit()",
			"Bekhab": "time.sleep"
		}
		self.ToBeRemoved = []
		self.DefinedVariables = []
		self.DefinedVariablesTypes = []
		self.Level = 0
		self.ScopeOrder = ["Main"]
		self.PythonLibraries = ["sys"]
		self.fh = fh
	def ListReplace( self,ListToReplace, Replaced , String ):
		for ToReplace in ListToReplace:
			String = String.replace(ToReplace,Replaced)
		return String

	def ExtractVariableName(self,VarDeclarationExp):
		if VarDeclarationExp.find("=") != -1:
			Output = self.ListReplace(["Sahih", "Ashar", "Harf","Reshte", "Bool"],"",VarDeclarationExp[0:VarDeclarationExp.find("=")])
			return Output
		else:
			return VarDeclarationExp

	def BenevisFormatter(self, Line):
		if Line.find("\"") == -1:
			return Line.replace("Benevis","print")
		else:
			OutputLine = Line.replace("Benevis","print")
			OutputLine = re.sub(r"\%(d|f|c|s)", "{}" , OutputLine)
			Rexec = re.findall(r'\"(.+?)\"', OutputLine)
			if OutputLine.replace(Rexec[0],Rexec[0].replace(",",".")).find(",") != -1:
				Args = OutputLine[OutputLine.replace(Rexec[0],Rexec[0].replace(",",".")).find(","):OutputLine.rfind(")")]
				OutputLine = OutputLine.replace(Args, ".format({})".format(Args.replace(",","",1).replace(" ","",1)))
			return OutputLine

	def BegirFormatter(self, Line):
		Output = ""
		InputOrder = re.findall(r"\%(d|f|c|s)", Line)
		Rexec = re.findall(r'\"(.+?)\"', Line)
		Args = Line[Line.replace(Rexec[0],Rexec[0].replace(",",".")).find(","):Line.rfind(")")].replace(",","",1).replace(" ","",1)
		Args = Args.split(",")
		InputCounter = 0
		for Input in InputOrder:
			VarName = Args[InputCounter].replace("&","")
			if VarName not in self.DefinedVariables:
				raise Exception("Undefined Variable Usage!")
				sys.exit()
			if Input == "d":
				Output += "{} = int(input())\n".format(VarName)
			elif Input == "f":
				Output += "{} = float(input())\n".format(VarName)
			elif Input in ("c","s"):
				Output += "{} = input()\n".format(VarName)
			InputCounter += 1
		return Output

	def YekiBalaFormatter(self,Line):
		if Line.find("YekiBala") != -1:
			Output = ""
			Output += Line.replace("YekiBala","") + " += 1"
			return Output
		else:
			return -1

	def YekiPainFormatter(self,Line):
		if Line.find("YekiPain") != -1:
			return Line.replace("YekiPain","") + " -= 1"
		else:
			return -1

	def AgarFormatter(self,Line):
		self.ToBeRemoved.append("]")
		self.ScopeOrder.append("Agar")
		Line = self.ListReplace( ["{","}"] , "" , Line )
		return Line.replace("agar", "if ").replace("[", ":")

	def TaFormatter(self,Line):
		self.ToBeRemoved.append("]")
		self.ScopeOrder.append("Ta")
		Line = self.ListReplace( ["{","}"] , "" , Line )
		return Line.replace("ta", "while ").replace("[", ":")

	def Evaluator(self):
		Code = self.fh.read()
		FinalCode = re.sub(r'\t','',Code)
		FinalCode = re.sub(r'^Main\(\)\[', "", FinalCode)
		FinalCode = re.sub(r']$', "", FinalCode)
		VariablesPrefix = tuple(Keywords[0:5])
		for Replaced in self.Equivalent:
			FinalCode = FinalCode.replace(Replaced, self.Equivalent[Replaced])
		for Line in FinalCode.splitlines():
			if len(self.ToBeRemoved) > 0 and Line.find(self.ToBeRemoved[-1]) != -1 and Line.replace("\t","").startswith(self.ToBeRemoved[-1]):
				FinalCode = FinalCode.replace(self.ToBeRemoved[-1],"",1)
				self.ToBeRemoved.pop()
				self.ScopeOrder.pop()
				self.Level -= 1
			elif Line.replace("\t","").startswith(VariablesPrefix):
				VariableName = self.ListReplace(VariablesPrefix, "",Line)
				VariableName = self.ListReplace(["\t","^"], "" , VariableName).strip()
				if Line.find("=") == -1: # No Value Assigned, Assign Default
					if "Sahih" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = 0".format(VariableName))
					elif "Bool" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = False".format(VariableName))
					elif "Reshte" in Line or "Harf" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = \"\"".format(VariableName))
					elif "Ashar" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = 0.0".format(VariableName))
				else:
					FinalCode = FinalCode.replace(Line, self.Level*"\t"+self.ListReplace(VariablesPrefix,"",Line).lstrip())
				if VariableName not in self.DefinedVariables:
					if VariableName.find("=") != -1:
						VariableName = self.ExtractVariableName(VariableName)
					self.DefinedVariables.append( VariableName.strip() )
					if "Sahih" in Line:
						self.DefinedVariablesTypes.append(int)
					elif "Bool" in Line:
						self.DefinedVariablesTypes.append(bool)
					elif "Ashar" in Line:
						self.DefinedVariablesTypes.append(float)
					elif "Reshte" in Line:
						self.DefinedVariablesTypes.append(str)
					elif "Harf" in Line:
						self.DefinedVariablesTypes.append(Char)
				else:
					raise Exception("Variable Redeclaration!")
					sys.exit()
			elif Line.find( "Begir" ) != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.BegirFormatter(Line))
			elif Line.find( "Benevis" ) != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.BenevisFormatter(Line))
			elif Line.find("YekiPain") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.YekiPainFormatter(Line))
			elif Line.find("YekiBala") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.YekiBalaFormatter(Line))
			elif Line.find("agar") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.AgarFormatter(Line))
				self.Level += 1
			elif Line.find("ta") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.TaFormatter(Line))
				self.Level += 1
			elif Line.find("break") != -1 or Line.find("continue") != -1:
				FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
			elif Line.find("=") != -1:
				if Line.find("+") != -1 or Line.find("/") != -1 or Line.find("*") != -1 or Line.find("-") != -1:
					FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
				elif Line.find("False") != -1:
					FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
				elif (not Line.replace("\t","").startswith(VariablesPrefix)) and Line.find("+") == -1 and Line.find("/") == -1 and Line.find("*") == -1 and Line.find("-") == -1:
					# Defined Variable Value Assignment
					TrimedLine = Line.replace("\t","")
					Value = TrimedLine[TrimedLine.find("=")+1:].strip().replace("^","")
					Name = self.ListReplace(VariablesPrefix,"",TrimedLine[0:TrimedLine.find("=")]).strip()
					VariableNamesExtracted = [self.ExtractVariableName(x).strip() for x in self.DefinedVariables]
					if Name in VariableNamesExtracted and Value in VariableNamesExtracted:
						FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
					# elif not isinstance(Value,self.DefinedVariablesTypes[VariableNamesExtracted.index(Name)]):
					# 	raise Exception("Wrong Variable Manipulation")

						
			elif Line.find("Bemir") != -1:
				FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
			elif Line.find("Bekhab") != -1:
				FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
			elif Line in ("\n", "]","["):
				continue
			else:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+Line.replace("\t","").strip())
		
		ExecutedCode = ""

		for Library in self.PythonLibraries:
			ExecutedCode += "import {}".format(Library)

		FinalCode = FinalCode.replace("\t ", "\t")
		FinalCode = re.sub(r" +", ' ', FinalCode)
		FinalCode = re.sub(r'\n+', '\n', FinalCode)
		FinalCode = re.sub(r'<M', '<=', FinalCode)
		FinalCode = re.sub(r'>M', '>=', FinalCode)
		
		for Line in FinalCode.splitlines():
			ExecutedCode += Line + "\n"
		
		exec(ExecutedCode)

	def ReturnitiveEvaluator(self):
		Code = self.fh.read()
		FinalCode = re.sub(r'\t','',Code)
		FinalCode = re.sub(r'^Main\(\)\[', "", FinalCode)
		FinalCode = re.sub(r']$', "", FinalCode)
		VariablesPrefix = tuple(Keywords[0:5])
		for Replaced in self.Equivalent:
			FinalCode = FinalCode.replace(Replaced, self.Equivalent[Replaced])
		for Line in FinalCode.splitlines():
			if len(self.ToBeRemoved) > 0 and Line.find(self.ToBeRemoved[-1]) != -1 and Line.replace("\t","").startswith(self.ToBeRemoved[-1]):
				FinalCode = FinalCode.replace(self.ToBeRemoved[-1],"",1)
				self.ToBeRemoved.pop()
				self.ScopeOrder.pop()
				self.Level -= 1
			elif Line.replace("\t","").startswith(VariablesPrefix):
				VariableName = self.ListReplace(VariablesPrefix, "",Line)
				VariableName = self.ListReplace(["\t","^"], "" , VariableName).strip()
				if Line.find("=") == -1: # No Value Assigned, Assign Default
					if "Sahih" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = 0".format(VariableName))
					elif "Bool" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = False".format(VariableName))
					elif "Reshte" in Line or "Harf" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = \"\"".format(VariableName))
					elif "Ashar" in Line:
						FinalCode = FinalCode.replace(Line, self.Level*"\t"+"{} = 0.0".format(VariableName))
				else:
					FinalCode = FinalCode.replace(Line, self.Level*"\t"+self.ListReplace(VariablesPrefix,"",Line).lstrip())
				if VariableName not in self.DefinedVariables:
					if VariableName.find("=") != -1:
						VariableName = self.ExtractVariableName(VariableName)
					self.DefinedVariables.append( VariableName.strip() )
					if "Sahih" in Line:
						self.DefinedVariablesTypes.append(int)
					elif "Bool" in Line:
						self.DefinedVariablesTypes.append(bool)
					elif "Ashar" in Line:
						self.DefinedVariablesTypes.append(float)
					elif "Reshte" in Line:
						self.DefinedVariablesTypes.append(str)
					elif "Harf" in Line:
						self.DefinedVariablesTypes.append(Char)
				else:
					raise Exception("Variable Redeclaration!")
					sys.exit()
			elif Line.find( "Begir" ) != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.BegirFormatter(Line))
			elif Line.find( "Benevis" ) != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.BenevisFormatter(Line))
			elif Line.find("YekiPain") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.YekiPainFormatter(Line))
			elif Line.find("YekiBala") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.YekiBalaFormatter(Line))
			elif Line.find("agar") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.AgarFormatter(Line))
				self.Level += 1
			elif Line.find("ta") != -1:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+self.TaFormatter(Line))
				self.Level += 1
			elif Line.find("break") != -1 or Line.find("continue") != -1:
				FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
			elif Line.find("=") != -1:
				if Line.find("+") != -1 or Line.find("/") != -1 or Line.find("*") != -1 or Line.find("-") != -1:
					FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
				elif Line.find("False") != -1:
					FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
				elif (not Line.replace("\t","").startswith(VariablesPrefix)) and Line.find("+") == -1 and Line.find("/") == -1 and Line.find("*") == -1 and Line.find("-") == -1:
					# Defined Variable Value Assignment
					TrimedLine = Line.replace("\t","")
					Value = TrimedLine[TrimedLine.find("=")+1:].strip().replace("^","")
					Name = self.ListReplace(VariablesPrefix,"",TrimedLine[0:TrimedLine.find("=")]).strip()
					VariableNamesExtracted = [self.ExtractVariableName(x).strip() for x in self.DefinedVariables]
					if Name in VariableNamesExtracted and Value in VariableNamesExtracted:
						FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
					# elif not isinstance(Value,self.DefinedVariablesTypes[VariableNamesExtracted.index(Name)]):
					# 	raise Exception("Wrong Variable Manipulation")

						
			elif Line.find("Bemir") != -1:
				FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
			elif Line.find("Bekhab") != -1:
				FinalCode = FinalCode.replace(Line, self.Level * "\t" + Line.strip())
			elif Line in ("\n", "]","["):
				continue
			else:
				FinalCode = FinalCode.replace(Line,self.Level*"\t"+Line.replace("\t","").strip())
		
		ExecutedCode = ""

		for Library in self.PythonLibraries:
			ExecutedCode += "import {}".format(Library)

		FinalCode = FinalCode.replace("\t ", "\t")
		FinalCode = re.sub(r" +", ' ', FinalCode)
		FinalCode = re.sub(r'\n+', '\n', FinalCode)
		FinalCode = re.sub(r'<M', '<=', FinalCode)
		FinalCode = re.sub(r'>M', '>=', FinalCode)
		
		for Line in FinalCode.splitlines():
			ExecutedCode += Line + "\n"
		@contextlib.contextmanager
		def stdoutIO(stdout=None):
		    old = sys.stdout
		    if stdout is None:
		        stdout = StringIO()
		    sys.stdout = stdout
		    yield stdout
		    sys.stdout = old

		with stdoutIO() as s:
		    try:
		        exec(ExecutedCode)
		    except:
		        print("Something wrong with the code")

		return s.getvalue()
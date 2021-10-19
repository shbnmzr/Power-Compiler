import pandas as pd
from collections import deque
from .Token import Token
from .Code import Code
from .Constants import Debug

class Parser():
    def __init__(self, Lexer, ParsingTableFileLocation):
        Lexer.Tokenizer()
        Lexer.Tokens.append(Token("$","$"))
        Lexer.Tokens.reverse()
        self.Lexer = Lexer
        self.Tokens = deque(Lexer.Tokens)
        self.Stack = deque([])
        self.df = None
        self.Variables = []
        self.ParsingTableFileLocation = ParsingTableFileLocation
        self.Stack.append(Token("START","START"))
        self.Stack.append(Token("$","$"))
        self.Stack.reverse()

        # Control Variables
        self.TableLoaded = False
        self.VarsExtracted = False

    def LoadParsingTable(self):
        if self.TableLoaded: return True
        if not self.ParsingTableFileLocation.endswith(".csv"):
            print("[WARNING] Use CSV Files for Best Performance")
        self.TableLoaded = True
        self.df = pd.read_csv(self.ParsingTableFileLocation)
        self.df.fillna("NONE")

    def ExtractVariables(self):
        if self.VarsExtracted: return False
        self.LoadParsingTable()
        for i in self.df.iloc[:,0]:
            self.Variables.append(i)
        self.VarsExtracted = True

    def GetFirstVariableIndex(self, Words):
        for i,Word in enumerate(Words):
            if Word in self.Variables:
                return i

    def Parse(self):
        self.ExtractVariables()
        while True:
            Type = False
            Value = False
            if self.Stack[-1].Type == '$' and self.Tokens[-1].Type == '$':break
            if self.Tokens[-1].Value == '': self.Tokens.pop()
            if Debug:
                print([x.Value for x in self.Stack])
                print([x.Value for x in self.Tokens])
                print("\n\n\n")
            Pop = False
            if self.Tokens[-1].Value == self.Stack[-1].Value and self.Stack[-1].Type == self.Tokens[-1].Type:
                Pop = True
            elif self.Stack[-1].Type=="IDENTIFIER" and self.Stack[-1].Value == self.Tokens[-1].Type:
                Pop = True
            if Pop:
                PopedStack = self.Stack.pop()
                PoppedToken = self.Tokens.pop()
                if Debug:
                    print("POP")
                    print(PopedStack)
                    print(PoppedToken,"\n")
            else: # Should Be Checked
                if self.Tokens[-1].Value in self.df.columns:
                    ColumnToBeCheckedName = self.Tokens[-1].Value
                    Value = True
                elif self.Tokens[-1].Type in self.df.columns:
                    ColumnToBeCheckedName = self.Tokens[-1].Type
                    Type = True
                else:
                    raise Exception("Some Error Was There")
                    return False

                if Debug:
                    print("STACK CHANGE")
                    print(self.Stack[-1])
                    print(self.Tokens[-1],"\n")

                if Type:
                    if self.Stack[-1].Type == "IDENTIFIER":
                        CellValue = self.df.iloc[self.Variables.index(self.Stack[-1].Value), self.df.columns.get_loc(ColumnToBeCheckedName)]
                    else:
                        CellValue = self.df.iloc[self.Variables.index(self.Stack[-1].Type), self.df.columns.get_loc(ColumnToBeCheckedName)]
                elif Value:
                    CellValue = self.df.iloc[self.Variables.index(self.Stack[-1].Value), self.df.columns.get_loc(ColumnToBeCheckedName)]
                else:
                    raise Exception("Some Error Again")
                    return False

                if CellValue == "EMPTY":
                    self.Stack.pop()
                elif CellValue in ("NONE","nan"):
                    raise Exception("Parser Error")
                    return False
                else:
                    self.Stack.pop()
                    # CellValue = self.ParseHelper(Code.TrimLine(CellValue).split(" "))
                    TempTokens = self.Lexer.LexLine(CellValue)
                    TempTokens.reverse()
                    self.Stack += deque(TempTokens)

        return True
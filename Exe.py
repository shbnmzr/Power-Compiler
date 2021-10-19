from Power.Power import *
import os

def main():

	while True:

		print("""
	Enter Option 1,2,3 Or 4:
				1) Factorial + Number Input
				2) Fibonatchi Numbers Series
				3) User Login Simulator
				4) Multiplicants + Without STD Input

				_________________________
""")
		print("\t" * 4 + "=> ", end="")
		Option = int(input())
		if Option in (1,2,3,4): break

	cls()

	if Option == 1:
		Compiler = Power(".\\Data\\Factorial.pwd")
	elif Option == 2:
		Compiler = Power(".\\Data\\Fibonatchi.pwd")
	elif Option == 3:
		Compiler = Power(".\\Data\\Login.pwd")
	elif Option == 4:
		Compiler = Power(".\\Data\\Multiplicant.pwd")

	Compiler.Run()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__": main()
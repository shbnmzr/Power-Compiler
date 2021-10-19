# Power Language Compiler

## Introduction
This README is a description of the Power Language Compiler project, development phases.
This compiler takes an input file with .pwr extension and generates the equivalent Python source code.
There's also a debug mode provided to inspect the code which can be accessed from inside the IDE.
This repository contains all the source code, a designed IDE and a test file. You can clone this repository to your local system.

## Set up Instructions
Following these instructions you should be able to run the test file, and develop you own Power program based on the language syntax.

### Create Project
There are some basic software dependencies to install, after which Power Compiler handles the rest.
Power Compiler is run from within a python virtual environment for your project.
1. Install prerequisite software. The installation methodology will depend up on your operating system:
 - Python
 - Git
 
 2. Clone this project from the repository :

        $ git clone https://github.com/shbnmzr/Power-Compiler.git

3. Run Exe.py file to start up the Power IDE.
### Run Test.pwd File
The Test.pwr file provided in this repository contains the sample code for the power language. Open this file in the IDE and execute it by clicking on the Run button. The program will run in case no error occurs and the result will appear in the console. 

### Develop Your Own Power Program
Now we can start to write code in power language. You're also presumably familiar with the power language syntax.

1. Create a new file with .pwd or .txt extension.
2. Open the file inside the IDE.
3. Click on the run button and corresponding result will appear. Also, Compile-time errors will be detected and an appropriate message will be shown in order to guide you to modify your code and get the desired result.
4. The existing file can also be modified and saved on your local computer.

## Development Phases
This compiler was developed in 4 consecutive phases. The source code of all the phases is provided in the repository.

1. Lexical Analyzer (Scanner):
As the name applies, this phase would analyze the input code lexically and generate a stream of tokens. 
It reads the characters from source program and groups them into lexemes. Each lexeme corresponds to a token. 
It also detects lexical errors (for e.g., erroneous characters), and removes comments and white space.
The scanner has been developed using 2 seperate methods. The source code of the DFA version of the scanner has been provided in the dfa-version branch.

2. Syntax Analyzer (Parser):
Syntax analyzer takes the stream of tokens as input and checks the input code based on the context-free grammar that has been defined for the language. 
The rules of programming are entirely represented in some productions. The input has to be checked whether it is in the desired format or not.
LL(1) Pasing table of the Power Language has been provided.

3. Semantic Analyzer:
Semantic Analysis makes sure that declarations and statements of program are semantically correct.

**Type checking** is an important part of semantic analysis where compiler makes sure that each operator has matching operands.

**Semantic Errors:**  

Errors recognized by semantic analyzer are as follows:

-   Type mismatch

-   Undeclared variables

-   Reserved identifier misuse

4. Code Generator:
This phase generates the equivalent Python code. This is the final stage of compilation.

5. Execution:
This is an arbitary phase that is done by the Python compiler. The input Power program will be translated to the equivalent Python code and run thoroughly.


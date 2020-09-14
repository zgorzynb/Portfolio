## The repository contains the complete compiler code created for my own language.  

The program code in the new language should be placed in the Code.pl file.  
The run.bat file contains a set of commands that allow you to compile and run the program

For Linux, the command set looks like this:

To generate LLVM code:
```
antlr4 -Dlanguage=Python3 PLwypisz.g4
python Main.py > AA_LLCCode.ll
```

To compile LLVM code:
```
llvm-as AA_LLCCode.ll
lli AA_LLCCode.bc
```
or

```
llc AA_LLCCode.ll
clang AA_LLCCode.s
```
### Dependencies:
- Python 3.x
- ANTLR 4.8
- LLVM 10.0

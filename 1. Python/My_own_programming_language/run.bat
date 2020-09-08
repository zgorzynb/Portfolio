del AA_Compiled.exe
del AA_LLCCode.ll
call antlr4 -Dlanguage=Python3 PLwypisz.g4 > nul
python Main.py > AA_LLCCode.ll
if %errorlevel% neq 0 exit /b %errorlevel%
clang AA_LLCCode.ll -o AA_Compiled.exe
AA_Compiled.exe

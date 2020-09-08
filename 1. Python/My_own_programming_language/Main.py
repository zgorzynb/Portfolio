import antlr4
from PLwypiszLexer import PLwypiszLexer
from PLwypiszParser import PLwypiszParser
from LLVMActions import LLVMActions
import sys
from io import StringIO

def main():
    with open ("Code.pl", "r") as myfile:
        # old_stderr = sys.stderr
        # redirected_error = sys.stderr = StringIO()
        data = myfile.read()
        input = antlr4.InputStream(data)
        lexer = PLwypiszLexer(input)
        tokens = antlr4.CommonTokenStream(lexer)
        parser = PLwypiszParser(tokens)
        tree = parser.prog()
        # stderr_val = redirected_error.getvalue()
        # if stderr_val:
        #     old_stderr.write(stderr_val)
        #     raise RuntimeError()
        walker = antlr4.ParseTreeWalker()
        walker.walk(LLVMActions(), tree)


if __name__ == "__main__":
    main()
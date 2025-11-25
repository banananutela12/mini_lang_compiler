# compile.py

import sys
import os

# Add project root so Python can find src/
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.parser import Parser
from src.semantics import SemanticAnalyzer, SemanticError
from src.codegen import TACGenerator

def main():
    if len(sys.argv) < 3:
        print("Usage: python compile.py input.src -o output.tac")
        sys.exit(1)

    input_file = sys.argv[1]
    if sys.argv[2] != "-o" or len(sys.argv) < 4:
        print("Usage: python compile.py input.src -o output.tac")
        sys.exit(1)
    output_file = sys.argv[3]

    with open(input_file, "r") as f:
        source = f.read()

    parser = Parser(source)
    program = parser.parse()

    sem = SemanticAnalyzer()
    try:
        sem.analyze(program)
    except SemanticError as e:
        print(f"Semantic error: {e}")
        sys.exit(1)

    gen = TACGenerator()
    tac = gen.generate(program)

    with open(output_file, "w") as f:
        for instr in tac:
            f.write(instr + "\n")
if __name__ == "__main__":
    main()


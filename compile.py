# compile.py
import sys
from parser import Parser
from semantics import SemanticAnalyzer, SemanticError
from codegen import TACGenerator

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

    # parse
    parser = Parser(source)
    program = parser.parse()

    # semantic analysis
    sem = SemanticAnalyzer()
    try:
        sem.analyze(program)
    except SemanticError as e:
        print(f"Semantic error: {e}")
        sys.exit(1)

    # codegen
    gen = TACGenerator()
    tac = gen.generate(program)

    with open(output_file, "w") as f:
        for instr in tac:
            f.write(instr + "\n")

    print(f"Compiled {input_file} -> {output_file}")

if __name__ == "__main__":
    main()

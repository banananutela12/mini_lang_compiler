# nota: archivo para compilar a TAC

import sys, os

# path del proyecto (para que encuentre los modulos)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.parser import Parser
from src.semantics import SemanticAnalyzer, SemanticError
from src.codegen import TACGenerator


def main():
    # args basicos
    if len(sys.argv) < 3:
        print("Usage: python compile.py input.src -o output.tac")
        sys.exit(1)

    input_file = sys.argv[1]

    # checar flag de salida
    if sys.argv[2] != "-o" or len(sys.argv) < 4:
        print("Usage: python compile.py input.src -o output.tac")
        sys.exit(1)

    output_file = sys.argv[3]

    # leer archivo src
    with open(input_file, "r") as f:
        source = f.read()

    # parser (ast)
    parser = Parser(source)
    program = parser.parse()

    # semantica
    sem = SemanticAnalyzer()
    try:
        sem.analyze(program)
    except SemanticError as e:
        print(f"Semantic error: {e}")   # msg directo
        sys.exit(1)

    # generar tac
    gen = TACGenerator()
    tac = gen.generate(program)

    # guardar salida
    with open(output_file, "w") as f:
        for instr in tac:
            f.write(instr + "\n")


if __name__ == "__main__":
    main()   # compilar

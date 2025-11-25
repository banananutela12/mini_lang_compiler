# script para ejecutar un archivo .tac

import os
import sys

# ruta base del proyecto (para importar el modulo vm)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from src.vm import TACVM

def main():
    # args minimos
    if len(sys.argv) < 2:
        print("Usage: python run_tac.py program.tac")
        sys.exit(1)

    tac_file = sys.argv[1]

    # leer instrucciones tac
    with open(tac_file, "r") as f:
        instructions = [line.rstrip("\n") for line in f]

    # vm: ejecuta el tac linea por linea
    vm = TACVM(instructions)
    vm.run()

if __name__ == "__main__":
    main()   # ejecutar tac

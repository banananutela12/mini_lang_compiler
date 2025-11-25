import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from src.vm import TACVM


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_tac.py program.tac")
        sys.exit(1)

    tac_file = sys.argv[1]
    with open(tac_file, "r") as f:
        instructions = [line.rstrip("\n") for line in f]

    vm = TACVM(instructions)
    vm.run()

if __name__ == "__main__":
    main()

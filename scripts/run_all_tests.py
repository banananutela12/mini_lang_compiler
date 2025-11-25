# script para correr todos los tests (rapido)

import os
import subprocess

# root del proyecto
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT, "tests")

def run(cmd):
    # nota: ejecutar comando y regresar stdout/stderr
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

print("\n=== Running All Tests ===")
print("-------------------------\n")

# recorrer todos los src
for fname in sorted(os.listdir(SRC_DIR)):
    if not fname.endswith(".src"):
        continue
    
    print(f"=== Running {fname} ===")
    
    src_path = os.path.join(SRC_DIR, fname)
    out_tac = os.path.join(SRC_DIR, fname.replace(".src", ".tac"))

    # compilar a tac
    stdout, stderr, code = run(f"python3 scripts/compile.py {src_path} -o {out_tac}")

    if code != 0:
        print("Compiler error:")
        print(stdout)
        print(stderr)
        print()
        continue
    
    # correr tac
    stdout, stderr, code = run(f"python3 scripts/run_tac.py {out_tac}")

    print("[OUTPUT]")
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    print()

print("=== DONE ===")

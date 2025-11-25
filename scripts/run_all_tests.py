import os
import subprocess

TESTS_DIR = "tests"

def run_test(src_file):
    tac_file = src_file.replace(".src", ".tac")

    print(f"\n=== Running {src_file} ===")

    # Compile
    compile_cmd = [
        "python3",
        "scripts/compile.py",
        os.path.join(TESTS_DIR, src_file),
        "-o",
        os.path.join(TESTS_DIR, tac_file),
    ]
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)

    if compile_proc.returncode != 0:
        print(f"[ERROR EXPECTED OR FAIL] {src_file}")
        print(compile_proc.stdout)
        print(compile_proc.stderr)
        return

    # Run TAC
    run_cmd = [
        "python3",
        "scripts/run_tac.py",
        os.path.join(TESTS_DIR, tac_file),
    ]
    run_proc = subprocess.run(run_cmd, capture_output=True, text=True)

    print("[OUTPUT]")
    print(run_proc.stdout)

def main():
    print("=== Running All Tests ===")
    print("-------------------------")

    files = sorted(
        [f for f in os.listdir(TESTS_DIR) if f.endswith(".src")]
    )

    for f in files:
        run_test(f)

    print("\n=== DONE ===")

if __name__ == "__main__":
    main()

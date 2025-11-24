# vm.py
from typing import List, Dict

class TACVM:
    def __init__(self, instructions: List[str]):
        self.instructions = instructions
        self.labels: Dict[str, int] = {}
        self.vars: Dict[str, int] = {}
        self.pc = 0  # program counter
        self._index_labels()

    def _index_labels(self):
        # Map label "L1:" -> instruction index + 1 (next instr)
        idx = 0
        new_instrs = []
        for i, instr in enumerate(self.instructions):
            line = instr.strip()
            if line.endswith(":"):
                label = line[:-1]
                self.labels[label] = len(new_instrs)
            else:
                new_instrs.append(instr)
        self.instructions = new_instrs

    def run(self):
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc].strip()
            self.pc += 1
            if not instr:
                continue
            # print
            if instr.startswith("print "):
                expr = instr[len("print "):].strip()
                val = self.eval_expr(expr)
                print(val)
                continue
            # goto
            if instr.startswith("goto "):
                label = instr[len("goto "):].strip()
                self.pc = self.labels[label]
                continue
            # if cond goto label
            if instr.startswith("if "):
                # format: if X == 0 goto Lx   OR similar
                # we'll split: if <cond> goto <label>
                # we treat cond as expression (before 'goto')
                parts = instr.split("goto")
                cond_part = parts[0][len("if "):].strip()
                label = parts[1].strip()
                cond_val = self.eval_expr(cond_part)
                if cond_val:
                    self.pc = self.labels[label]
                continue
            # assignment: x := expr
            if ":=" in instr:
                left, right = instr.split(":=")
                left = left.strip()
                right = right.strip()
                val = self.eval_expr(right)
                self.vars[left] = val
                continue
            raise RuntimeError(f"Unknown instruction: {instr}")

    def eval_expr(self, expr: str) -> int:
        """
        Evaluator super simple basado en Python eval, pero
        reemplazando variables por sus valores.
        OJO: esto es para un proyecto académico pequeño.
        """
        # replace variables by values in a safe-ish way
        # tokens split by space
        tokens = expr.replace("(", " ( ").replace(")", " ) ").split()
        out_tokens = []
        for t in tokens:
            if t in self.vars:
                out_tokens.append(str(self.vars[t]))
            else:
                out_tokens.append(t)
        safe_expr = " ".join(out_tokens)
        # map logical operators &&, || to Python
        safe_expr = safe_expr.replace("&&", " and ")
        safe_expr = safe_expr.replace("||", " or ")
        # comparisons and arithmetic are same syntax in Python
        # treat != 0 as is
        try:
            val = eval(safe_expr, {"__builtins__": {}}, {})
        except Exception as e:
            raise RuntimeError(f"Error evaluating expression '{expr}' as '{safe_expr}': {e}")
        # convert bools to int 0/1
        if isinstance(val, bool):
            return 1 if val else 0
        return int(val)

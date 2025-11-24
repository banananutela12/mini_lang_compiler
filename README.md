# Mini-Lang Compiler

This project is a simple compiler for a small language called **Mini-Lang**.  
It was created for the *Theory of Computation* course.

The compiler reads a `.src` program, checks it, generates **Three-Address Code (TAC)** and executes it using a small virtual machine (VM).  
Everything is written in **Python**, with no external libraries.

---

## 1. Language Features

Mini-Lang supports:

- **Types:** `int`, `bool`
- **Declarations:** `int x;`
- **Assignments:** `x = 3 + y;`
- **Expressions:**  
  - Arithmetic: `+ - * /`  
  - Relational: `< <= > >= == !=`  
  - Logical: `&& || !`
- **Control flow:**  
  - `if (cond) { ... }`  
  - `if (cond) { ... } else { ... }`  
  - `while (cond) { ... }`
- **Print:** `print(expr);`

Example:

```c
int x;
x = 5;
print(x);

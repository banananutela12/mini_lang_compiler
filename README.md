
# Mini-Lang Compiler

## Overview

Mini-Lang is a small imperative programming language designed for educational purposes in the context of compiler construction. This project implements a complete compilation pipeline in Python, including:

* Lexical analysis
* Parsing
* Semantic analysis
* Intermediate representation generation (Three-Address Code, TAC)
* Execution using a virtual machine

The goal of the project is to demonstrate understanding of key concepts from formal languages, such as regular and context-free grammars, typing rules, and correct code generation.

---

## Language Features

Mini-Lang supports the following language constructs:

### Variable Declarations

```c
int x;
bool ok;
```

### Assignments

```c
x = a + 3;
```

### Expressions

* **Arithmetic:** `+ - * /`
* **Relational:** `< <= > >= == !=`
* **Logical:** `&& || !`
* **Parentheses for grouping**
* **Integer and boolean literals**

### Conditionals

```c
if (x < y) {
    z = 1;
} else {
    z = 0;
}
```

### Loops

```c
while (x < 5) {
    x = x + 1;
}
```

### Output

```c
print(x);
```

---

## Compilation Pipeline

The Mini-Lang compiler follows the stages:

```
Source file (.src)
 → Lexical Analysis
 → Parsing (AST construction)
 → Semantic Analysis
 → Code Generation (TAC)
 → Execution using a virtual machine
```

Each component is implemented as an independent module to ensure modularity and clarity.

---

## Three-Address Code (TAC)

Mini-Lang programs are compiled into a simple intermediate representation similar to assembly. Every computation uses temporary registers, and control flow is represented through explicit labels and jumps.

Example:

Source:

```c
x = a + 3;
```

TAC:

```
t1 := a + 3
x := t1
```

Example with conditional:

```
if (x < y) {
    z = 1;
} else {
    z = 0;
}
```

TAC:

```
if x < y goto L1
z := 0
goto L2
L1:
z := 1
L2:
```

The provided virtual machine executes TAC instructions sequentially.

---

## Project Structure

```
/src
    lexer.py
    parser.py
    semantics.py
    codegen.py
    vm.py

/tests
    *.src           Source files
    *.tac           Expected TAC outputs

/scripts
    run_tac.py
    run_all_tests.py

/docs
    (specification and diagrams)
```

---

## How to Build and Run

### 1. Requirements

* Python 3.8+
* No external libraries required

### 2. Compile a Mini-Lang Program

```
python3 compiler.py input.src -o out.tac
```

### 3. Run TAC

```
python3 run_tac.py out.tac
```

### 4. Run All Test Programs

```
python3 run_all_tests.py
```

---

## Writing Programs

Mini-Lang programs must have:

* Variable declarations before use
* Statements inside the main program block

Example:

```c
int a;
int b;
a = 5;
b = a + 3;
print(b);
```

---

## Error Handling

The compiler detects and reports:

* Undeclared variables
* Duplicate declarations
* Type mismatches in expressions and assignments
* Non-boolean conditions in `if` and `while`

Errors include line and column information when possible.

---

## Testing

The project includes a suite of test programs demonstrating:

* Basic arithmetic and assignments
* Conditionals
* Loop execution
* Error cases (type or undeclared variable)
* Full program integration

Users are encouraged to extend the test suite as needed.

---

## Limitations

Mini-Lang intentionally excludes:

* Functions
* Arrays and complex types
* Floating-point numbers
* Optimizations
* Object-oriented or functional features

These simplifications keep the focus on correctness and clarity of compilation.

---

## Authors and Academic Context

This project was developed as part of the **Theory of Computation** course. Its purpose is to integrate the concepts of lexical analysis, parsing, semantics, and execution into a fully working compiler.

---

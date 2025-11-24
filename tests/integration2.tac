x := 3
t1 := x * 2
y := t1
z := 0
t2 := y > 5
if t2 == 0 goto L2
L1:
t3 := y + 10
z := t3
goto L3
L2:
z := 999
L3:
print z

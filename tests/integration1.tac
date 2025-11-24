a := 1
b := 2
c := 0
L1:
t1 := a < 5
if t1 == 0 goto L3
t2 := c + b
c := t2
t3 := a + 1
a := t3
goto L1
L3:
print c

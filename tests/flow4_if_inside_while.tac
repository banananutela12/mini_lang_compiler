i := 0
L1:
t1 := i < 4
if t1 == 0 goto L3
t2 := i == 2
if t2 == 0 goto L5
print 100
L5:
t3 := i + 1
i := t3
goto L1
L3:

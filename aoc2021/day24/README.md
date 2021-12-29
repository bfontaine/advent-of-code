# Day 24

Decompiled code:
```python
def run(digits):
    stack = []

    pop_indices = {3, 4, 7, 9, 11, 12, 13}

    #                                                A    B   C   D
    #      0    1  2   3    4   5  6     7   8   9  10   11  12  13
    x_n = [12, 12, 12, -9, -9, 14, 14, -10, 15, -2, 11, -15, -9, -3]
    y_n = [ 9,  4,  2,  5,  1,  6, 11,  15,  7, 12, 15,   9, 12, 12]

    for i, digit in enumerate(digits):
        last = stack[-1] if stack else 0

        if i in pop_indices:
            stack.pop()

        if digit != last + x_n[i]:
            stack.append(digit + y_n[i])
```

Unrolled:
```
i=0 S=[]                          -- << d0 + 9
i=1 S=[d0+9]                      -- << d1 + 4
i=2 S=[d0+9 d1+4]                 -- << d2 + 2
i=3 S=[d0+9 d1+4 d2+2]            -- pop()
S=[d0+9 d1+4]                     -- cond: d3 == d2+2+-9 == d2-7
i=4 S=[d0+9 d1+4]                 -- pop()
S=[d0+9]                          -- cond: d4 == d1+4+-9 == d1-5
i=5 S=[d0+9]                      -- << d5 + 6
i=6 S=[d0+9 d5+6]                 -- << d6 + 11
i=7 S=[d0+9 d5+6 d6+11]           -- pop()
S=[d0+9 d5+6]                     -- cond: d7 == d6+11+-10 == d6+1
i=8 S=[d0+9 d5+6]                 -- << d8 + 7
i=9 S=[d0+9 d5+6 d8+7]            -- pop()
S=[d0+9 d5+6]                     -- cond: d9 == d8+7+-2 == d8+5
i=A S=[d0+9 d5+6]                 -- << dA + 15
i=B S=[d0+9 d5+6 dA+15]           -- pop()
S=[d0+9 d5+6]                     -- cond: dB == dA+15+-15 == dA
i=C S=[d0+9 d5+6]                 -- pop()
S=[d0+9]                          -- cond: dC == d5+6+-9 == d5-3
i=D S=[d0+9]                      -- pop()
S=[]                              -- cond: dD == d0+9+-3 == d0+6
```

Conditions:
```
d3  == d2 - 7 --> d2=[8-9] d3=[1-2]
d4  == d1 - 5 --> d1=[6-9] d4=[1-4]
d7  == d6 + 1 --> d6=[1-8] d7=[2-9]
d9  == d8 + 5 --> d8=[1-4] d9=[6-9]
d11 == d10
d12 == d5 - 3 --> d5=[4-9] d12=[1-6]
d13 == d0 + 6 --> d0=[1-3], d13=[7-9]
```

i.e.:
```
d0 : [1-3]
d1 : [6-9]
d2 : [8-9]
d3 : [1-2]
d4 : [1-4]
d5 : [4-9]
d6 : [1-8]
d7 : [2-9]
d8 : [1-4]
d9 : [6-9]
d10 :[1-9]
d11 : d10
d12 : [1-6]
d13 : [7-9]
```

So for my input the max (part 1) is `39924989499969`.
And the min (part 2) is `16811412161117`.
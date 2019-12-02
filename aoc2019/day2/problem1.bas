0010 REM Advent of Code 2019 > Day 2 > Problem 1
0020 REM ---------------------------------------
0030 REM
0040 REM Goal:
0050 REM  Read a comma-separated list of integers, representing the code to feed to
0060 REM  a simple interpreter. That code can override itself.
0070 REM  Instructions:
0080 REM    1 A B C -- take values at positions A and B and store their sum at C
0090 REM    2 A B C -- .............................................. product...
0100 REM   99       -- halt the program
0110 REM
0120 REM  The program starts at position 0, and goes forward by 4 positions at each
0130 REM  step until it arrives at 99, at which point it stops and return the value
0140 REM  at position 0.
0150 REM
0160 REM  After loading the code the interpreter should overwrite position 1 with
0170 REM  the value 12, and position 2 with the value 2.
0180 REM
0190 REM  Limitations:
0191 REM   This only works on inputs with up to 500 slots. The input MUST end
0192 REM   with a newline.
0193 REM  Resources (http://www. +):
0194 REM   vintage-basic.net/downloads/Vintage_BASIC_Users_Guide.html
0195 REM   c64-wiki.com/wiki/Category:BASIC_functions
0196 REM   lemon64.com/manual/
0197 DIM PG(500)
0200 I% = 1
0210 S$ = ""
0220 REM while true
0230 GET C$
0240 IF C$ = "," GOTO 1000
0250 IF ASC(C$) = 13 GOTO 2000
0260 REM digit
0601 S$ = S$ + C$
0602 GOTO 220 : REM continue
1000 REM comma
1010 PG(I%) = VAL(S$)
1020 S$ = ""
1030 I% = I% + 1
1040 GOTO 220 : REM continue
2000 REM end of input
2010 PG(I%) = VAL(S$)
2020 REM initialize the program
2030 PG(2) = 12
2040 PG(3) = 2
2100 REM now the fun can start
2110 CT% = 1
3000 OP% = PG(CT%)
3010 IF OP% = 99 GOTO 5000
3020 P1% = PG(CT% + 1) + 1
3030 P2% = PG(CT% + 2) + 1
3040 P3% = PG(CT% + 3) + 1
3050 A = PG(P1%)
3060 B = PG(P2%)
3080 IF OP% = 1 GOTO 3100
3090 PG(P3%) = A * B : REM op=2 -> mul
3091 GOTO 3101
3100 PG(P3%) = A + B : REM op=1 -> add
3101 REM next op
3120 CT% = CT% + 4
3130 GOTO 3000
5000 REM end
5001 PRINT PG(1)

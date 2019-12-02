0010 REM Advent of Code 2019 > Day 2 > Problem 1
0020 REM ---------------------------------------
0030 REM See problem1.bas for the context.
0040 REM https://adventofcode.com/2019/day/2

0100 DIM MM(500) : REM write-once/read-only memory
0110 I% = 1
0120 S$ = ""
0200 REM while true
0210 GET C$
0220 IF C$ = "," GOTO 500
0230 IF ASC(C$) = 13 GOTO 1000
0240 REM digit
0250 S$ = S$ + C$
0260 GOTO 200 : REM continue
0500 REM comma
0510 MM(I%) = VAL(S$)
0520 S$ = ""
0530 I% = I% + 1
0540 GOTO 200 : REM continue
1000 REM end of input
1010 MM(I%) = VAL(S$)
1020 DIM PG(I%)
1100
1110 FOR NO=0 TO 99
1120 FOR VE=0 TO 99
2010 REM initialize the program
2030 FOR J=1 TO I%
2040 PG(J) = MM(J)
2050 NEXT J
2100 REM set noun & verb
2110 PG(2) = NO
2120 PG(3) = VE
2130 REM run the program (copy/pasted from problem1)
2140 CT% = 1
3000 OP% = PG(CT%)
3010 IF OP% = 99 GOTO 3500
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
3500 REM end
3510 IF PG(1) = 19690720 GOTO 4000
3519 REM
3520 NEXT VE
3530 NEXT NO
4000 PRINT NO*100 + VE

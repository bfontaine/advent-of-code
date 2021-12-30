{
  P[$2] = $5
}
END {
  i = 1
  while (S[1]<1000 && S[2]<1000) {
    dice1 = ++d
    dice2 = ++d
    dice3 = ++d

    P[i] += (dice1 + dice2 + dice3)
    P[i] %= 10
    if (!P[i]) P[i] = 10

    S[i] += P[i]

    # print "Player", i, "rolls", dice1 "+" dice2 "+" dice3, "and moves to", P[i] ", score:", S[i]

    i = i == 1 ? 2 : 1
  }
  print S[i] * d
}

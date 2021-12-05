{
  split($0, s, ",| ")

  x = s[1]
  y = s[2]
  # "->" = s[3]
  x2 = s[4]
  y2 = s[5]

  if (p!=2 && x != x2 && y != y2)
    next

  xn = x2 < x ? -1 : 1
  yn = y2 < y ? -1 : 1

  while (1) {
    if (grid[x "," y]++ == 1)
      n++

    if (x==x2 && y==y2)
      next

    x = x==x2 ? x : x+xn
    y = y==y2 ? y : y+yn
  }
}
END {
  print n
}

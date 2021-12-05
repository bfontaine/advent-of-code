{
  split($1, xy1, ",")
  split($3, xy2, ",")

  x1 = xy1[1]
  y1 = xy1[2]
  x2 = xy2[1]
  y2 = xy2[2]

  # only horizontal / vertical
  if (x1 != x2 && y1 != y2) next;

  xn=x2>=x1?1:-1
  yn=y2>=y1?1:-1

  for (x=x1; x!=(x2+xn); x+=xn) {
    for (y=y1; y!=(y2+yn); y+=yn) {
      if (grid[x "," y] == 1) {
        n++
      }

      grid[x "," y]++
    }
  }
}
END {
  print n
}

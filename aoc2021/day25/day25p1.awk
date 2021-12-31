function print_grid() {
  for (y=1; y<=H; y++) {
    for (x=1; x<=W; x++) {
      xy = x A y
      if (xy in Grid)
        printf Grid[xy] ? ">" : "v"
      else
        printf "."
    }
    print ""
  }
}
{
  #SUBSEP=
  A="@"
  W = split($0, Row, "")
  for (x in Row) {
    c = Row[x]
    if (c!=".")
      Grid[x A NR] = c == ">"
  }
}
# Grid[x@y] = 1 (>) or 0 (v)
END {
  H=NR

  print_grid()

  step = 0
  moved = 1

  while (moved) {
    moved = 0
    for (turn=1; turn>=0; turn--) {
      for (s in Grid) {
        v = Grid[s]
        split(s, C, A)
        x1=x2=C[1]
        y1=y2=C[2]
        if (v) {
          x2++
          if (x2>W) x2 -= W
        } else {
          y2++
          if (y2>H) y2 -= H
        }
        s2 = x2 A y2
        if (v != turn || s2 in Grid) {
          # can't move: not my turn, or there's someone ahead
          s2 = s
        } else {
          moved = 1
        }
        Grid2[s2] = v
      }

      split("", Grid)
      for (s in Grid2) {
        Grid[s] = Grid2[s]
      }
      split("", Grid2)
    }
    step++
    print step
  }
  print step
}

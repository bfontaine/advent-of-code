/,/ {
  Grid[$0] = 1
}
/=/ {
  if (p && ++F > 1) next

  idx = index($0, "=")
  axis = substr($0, idx-1, 1)
  value = int(substr($0, idx+1))

  for (s in Grid) {
    delete Grid[s]
    split(s, xy, ",")
    x = xy[1]
    y = xy[2]

    if (axis == "x" && x > value) {
        x = 2*value - x
    } else if (axis == "y" && y > value) {
        y = 2*value - y
    }
    Grid[x","y] = 1
  }
}
END {
  for (s in Grid) {
    N++
  }
  print N
}

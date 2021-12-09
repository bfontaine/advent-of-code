function is_lowest(x, y) {
  h = grid[x" "y]
  for (y1=y-1; y1<=y+1; y1++) {
    for (x1=x-1; x1<=x+1; x1++) {
      if (x1 < 1 || x1 > l || y1 < 1 || y1 > FNR) continue

      if (x1 == x && y1 == y) continue

      h1 = grid[x1" "y1]
      if (h1 <= h)
        return 0
    }
  }
  return h + 1
}

{
  l = split($0, row, "")
  for (i=1; i<=l; i++) {
    grid[i" "NR] = row[i]
  }
}
END {
  for (y=1; y<=FNR; y++) {
    for (x=1; x<=l; x++) {
      score += is_lowest(x, y)
    }
  }

  print score
}

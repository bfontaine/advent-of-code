{
  Width = split($0, Row, X)
  for (i in Row) {
    Grid[i, NR] = Row[i]
  }
}
END {
  Height = NR
  Size = Height * Width
  while (++step) {
      #for (y=1; y<=Height; y++) {
      #  for (x=1; x<=Width; x++) {
      #    printf Grid[x, y]
      #  }
      #  print ""
      #}
      #print "---"

    for (c in Grid) Grid[c]++


    split("", Flashed, X)
    touched = 1
    prev_flashes = flashes

    while (touched) {
      touched = 0

      for (y=1; y<=Height; y++) {
        for (x=1; x<=Width; x++) {
          c = x SUBSEP y
          if (c in Flashed) continue

          n = Grid[c]
          if (n > 9) {
            flashes++
            touched = 1
            Flashed[c] = 1

            for (y1=y-1; y1<y+2; y1++) {
              for (x1=x-1; x1<x+2; x1++) {
                Grid[x1, y1]++
              }
            }
          }
        }
      }
    }
    for (c in Flashed) {
      Grid[c] = 0
    }

    if (p == 1) {
      if (step==100) break
    } else if (flashes - prev_flashes == Size) {
      print step
      break
    }
  }

  if (p == 1) print flashes
}

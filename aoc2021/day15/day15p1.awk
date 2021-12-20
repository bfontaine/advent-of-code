{
  # State[i] = lowest total risk of any path from the top left to here

  L = split($0, Row, "")

  for (i in Row) {
    if (NR==1 && i==1) risk = 0
    else risk = Row[i]

    left = State[i-1]
    top = State[i]

    if (NR == 1) {
      State[i] = left + risk
      continue
    }

    if (i == 1) {
      State[i] = top + risk
      continue
    }

    lowest = top < left ? top : left
    State[i] = lowest + risk
  }
}
END {
  print State[L]
}

# Grid[x, y]
# Risk[x, y]: raw risk of this position
# State[x, y]: lowest risk to come there from top-left
function setRisk(x, y, risk       , current_state, new_risk) {
  if (risk) {
    current_state = State[x, y]
    new_risk = risk + Risk[x, y]
    if (!current_state || new_risk < current_state) {
      State[x, y] = new_risk
      return 1
    }
  }
}

{
  L = split($0, Row, "")
  for (i in Row) {
    Grid[i, NR] = Row[i]
  }
}
END {
  W = L * 5
  # 1- fill Risk
  for (y=1; y<=W; y++) {
    for (x=1; x<=W; x++) {
      x1 = x % L
      if (!x1) x1 = L

      y1 = y % L
      if (!y1) y1 = L

      offset = 0
      if (x > L) offset += int((x-1)/L)
      if (y > L) offset += int((y-1)/L)

      risk = (Grid[x1, y1] + offset) % 9
      if (!risk) risk = 9

      Risk[x, y] = risk

      # top if we're on the left, else left
      State[x, y] = (x == 1 ? State[x, y-1] : State[x-1, y]) + risk
    }
  }

  # repeatedly reduce the risks testing from all directions
  # it's very inefficient but it works
  touched = 1
  while (touched) {
    touched = 0
    for (y=1; y<=W; y++) {
      for (x=1; x<=W; x++) {
        top = State[x, y-1]
        bottom = State[x, y+1]
        left = State[x-1, y]
        right = State[x+1, y]

        touched += setRisk(x, y, top)
        touched += setRisk(x, y, bottom)
        touched += setRisk(x, y, left)
        touched += setRisk(x, y, right)
      }
    }
  }

  print State[W, W] - Grid[1,1]
}

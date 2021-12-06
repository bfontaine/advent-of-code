{
  split($0,s,",")

  for (i in s) {
    state[s[i]]++
  }

  for (day=0; day<m; day++) {
    new = state[0]
    state[7] += state[0]
    state[0] = 0

    for (i=1;i<=8;i++) {
      state[i-1] = state[i]
      state[i] = 0
    }
    state[8] = new
  }

  for (i in state) {
    total += state[i]
  }
  print total
}

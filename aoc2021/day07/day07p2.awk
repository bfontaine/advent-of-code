{
  split($0, crabs, ",")

  for (i in crabs) {
    x = crabs[i]
    max = x > max ? x : max
  }

  for (x=0; x<=max; x++) {
    score = 0
    for (i in crabs) {
      n = crabs[i] - x
      if (n < 0) n = -n
      score += n * (n+1)
    }
    if (!best_score || score < best_score) {
      best_score = score
    }
  }

  print best_score / 2
}

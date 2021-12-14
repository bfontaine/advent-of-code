{
  if (NR == 1) {
    for (i=1; i<length($0); i++) {
      pair = substr($0, i, 2)
      Pairs[pair]++
    }
  } else if ($0) {
    p1 = substr($0, 1, 1)
    p2 = substr($0, 2, 1)
    res = substr($0, 7)
    Rules[p1 p2] = p1 res "," res p2
  }
}
END {
  S = p == 1 ? 10 : 40
  for (step=1; step<=S; step++) {
    split("", NewPairs, X)

    for (pair in Pairs) {
      n = Pairs[pair]
      rule = Rules[pair]

      if (rule) {
        delete Pairs[pair]

        #print pair, "->", rule

        split(rule, new_pairs, ",")

        NewPairs[new_pairs[1]] += n
        NewPairs[new_pairs[2]] += n
      }
    }
    for (pair in NewPairs) {
      Pairs[pair] += NewPairs[pair]
    }
  }

  for (pair in Pairs) {
    n = Pairs[pair]
    split(pair, pp, "")
    Occurrences[pp[1]] += n
    Occurrences[pp[2]] += n
  }

  for (p in Occurrences) {
    n = Occurrences[p]

    if (n%2 == 1) {
      n = (n - 1)/2 + 1
    } else {
      n /= 2
    }

    if (n > Max) {
      Max = n
    }
    if (!Min || n < Min) {
      Min = n
    }
  }
  print Max - Min
}

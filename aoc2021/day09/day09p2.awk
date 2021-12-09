# Given a grid of N rows of M characters,
# this programs runs in O(N*M) in time and O(M) in memory.
#
# BEGIN { print "<html><body><pre>" }
# NextBassinId = 1
# State : [bassin_id for each column]
# Bassins : {bassin_id: bassin_size}
{
  l = split($0, row, "")
  for (i=1; i<=l; i++) {
    h = row[i]
    if (h == 9) {
      State[i] = 0
      continue
    }

    bassin_left = State[i-1]
    bassin_top = State[i]

    if (bassin_left) {
      if (bassin_top && bassin_top != bassin_left) {
        # merge bassins: top wins
        Bassins[bassin_top] += Bassins[bassin_left]
        delete Bassins[bassin_left]
        Bassins[bassin_top] += 1
        for (j=i;State[j];j--) {
          State[j] = bassin_top
        }
        continue
      }

      # only left: inherit
      State[i] = bassin_left
      Bassins[bassin_left]++
      continue
    }

    if (bassin_top) {
      Bassins[bassin_top]++
      continue
    }

    new_bassin = ++NextBassinId
    State[i] = new_bassin
    Bassins[new_bassin]++
  }

  # for (i=1; i<=l; i++) {
  #   s = State[i]
  #   if (s == 0) {
  #     printf " "
  #   } else {
  #     printf s
  #   }
  # }

  # print ""
}
END {
  asort(Bassins)
  l=length(Bassins)

  # for (i in Bassins) {
  #   print i, Bassins[i]
  # }

  print Bassins[l] * Bassins[l-1] * Bassins[l-2]
}

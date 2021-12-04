{
  split($0, s, "")
  for (i=1; i <= length($0); i++) {
    # 1: +1, 0: -1
    bits[i]+= (s[i] == "1") * 2 - 1;
  }
}
END {
  for (i in bits) {
    g = g * 2 + (bits[i] > 0)
    e = e * 2 + (bits[i] < 0)
  }
  print g * e
}

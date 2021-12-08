{
  for(i=NF-3;i<=NF;i++) {
      l = length($i)
      #     1         7         4         8
      n += (l == 2 || l == 3 || l == 4 || l == 7)
  }
}
END {
  print n
}

{
  split($0,s,",")
  for (day=0; day<80; day++) {
    for (i in s) {
      if (s[i] == 0) {
        s[i] = 6
        s[length(s)+1] = 8
      } else {
        s[i]--
      }
    }
  }
  print length(s)
}

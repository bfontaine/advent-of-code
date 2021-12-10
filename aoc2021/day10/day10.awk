{
  top=0
  Expected["("] = ")"
  Expected["{"] = "}"
  Expected["["] = "]"
  Expected["<"] = ">"

  split($0, line, "")
  for(i in line) {
    c = line[i]
    e = Expected[c]
    if (e) {
      Stack[++top] = e
    } else {
      if (Stack[top--] != c) {
        error_score += c == ")" ? 3 : c == "]" ? 57 : c == "}" ? 1197 : 25137
        next
      }
    }
  }
  s=0
  for (i=top; i>0; i--) {
    e = Stack[i]
    s = s * 5 + (e == ")" ? 1 : e == "]" ? 2 : e == "}" ? 3 : 4)
  }
  Scores[++NextScore] = s
}
END {
  if (p == 1) {
    print error_score
  } else {
    asort(Scores);
    print Scores[(NextScore+1)/2]
  }
}

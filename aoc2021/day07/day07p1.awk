{
  l=split($0, crabs, ",")
  asort(crabs)
  if (l%2) {
    median = crabs[(l+1)/2]
  } else {
    median = (crabs[l/2] + crabs[l/2+1])/2
  }
  for (i in crabs) {
    fuel += sqrt((crabs[i]-median)^2)
  }
  print fuel
}

{
  split($2, parts, "[.,xyz=]+")
  x1 = parts[2]
  x2 = parts[3]
  y1 = parts[4]
  y2 = parts[5]
  z1 = parts[6]
  z2 = parts[7]

  # For the part 2, consider ranges of cubes instead of individual cubes
  # e.g. on  1-2000
  #      off 1-500
  #      = on 501-2000 = 1499 cubes

  on = $1 == "on"
  for (x=x1; x<=x2; x++) {
    if (x < -50 || x > 50) next
    for (y=y1; y<=y2; y++) {
      if (y < -50 || y > 50) next
      for (z=z1; z<=z2; z++) {
        if (z < -50 || z > 50) next
        if (on)
          Cubes[x, y, z] = 1
        else
          delete Cubes[x, y, z]
      }
    }
  }
}
END {
  print length(Cubes)
}

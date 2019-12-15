#!/usr/bin/env awk -f

{
  split($0, line_parts, ")")
  orbited = line_parts[1]
  orbiting = line_parts[2]

  orbits[orbiting] = orbited
}

END {
  direct_orbits_count = length(orbits)

  indirect_orbits_counts["COM"] = -1
  # not efficient but ok enough for our input size: loop over until we cover
  # all elements instead of doing a topological sort. Worst case is O(n^2).
  #
  # this works in 0.1s on my input so it's ok enough for me here.
  covered = 0

  while (!covered) {
    covered = 1

    for (orbiting in orbits) {
      orbited = orbits[orbiting]
      # we don't have the parent -> continue
      if (!(orbited in indirect_orbits_counts)) {
        covered = 0
        continue
      }

      count = indirect_orbits_counts[orbited] + 1
      indirect_orbits_counts[orbiting] = count
    }
  }

  # counter the COM=-1 above
  indirect_orbits_count = 1

  for (el in indirect_orbits_counts) {
    indirect_orbits_count += indirect_orbits_counts[el]
  }

  printf("total = %d + %d = %d\n",
          direct_orbits_count,
          indirect_orbits_count,
          (direct_orbits_count + indirect_orbits_count))
}

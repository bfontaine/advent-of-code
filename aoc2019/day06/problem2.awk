#!/usr/bin/env awk -f

{
  split($0, line_parts, ")")
  orbited = line_parts[1]
  orbiting = line_parts[2]

  if (orbiting == "SAN") {
    santa_orbited = orbited
  } else if (orbiting == "YOU") {
    you_orbited = orbited
  }

  paths[orbited][orbiting] = 1
  paths[orbiting][orbited] = 1
}

END {
    printf("You are orbiting around %s\n", you_orbited)
    printf("Santa is orbiting around %s\n", santa_orbited)

    reach[you_orbited] = 0

    while (!(santa_orbited in reach)) {
        for (reached in reach) {
            for (newly_reached in paths[reached]) {
                if (newly_reached in reach) {
                    continue
                }

                reach[newly_reached] = reach[reached] + 1
            }
        }
    }

    printf("Good trip! You need %d transfers!\n", reach[santa_orbited])
}

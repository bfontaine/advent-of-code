function addEdge(n1, n2) {
  if (Edges[n1]) Edges[n1] = Edges[n1] "," n2
  else Edges[n1] = n2
}

function count_distinct_paths(node, visited, ok2   , next_node, next_nodes, sum) {
  if (node == "end") {
    return 1
  }
  if (Small[node]) {
    visited = visited " " node " "
  }

  sum = 0

  split(Edges[node], next_nodes, ",")
  for (i in next_nodes) {
    next_node = next_nodes[i]

    if (index(visited, " " next_node " ")) {
      if (ok2 == next_node) { ok2 = "" }
      else continue
    }

    sum += count_distinct_paths(next_node, visited, ok2)
  }

  return sum
}

{
  split($0, nodes, "-")
  n1 = nodes[1]
  n2 = nodes[2]

  if (tolower(n1) == n1) {
    Small[n1] = 1
  }
  if (tolower(n2) == n2) {
    Small[n2] = 1
  }

  addEdge(n1, n2)
  addEdge(n2, n1)
}
END {
  # for (n1 in Edges) {
  #   split(Edges[n1], E, ",")
  #   for (i in E) {
  #     print n1 " -> " E[i]
  #   }
  # }

  if (p == 1)
    print count_distinct_paths("start")
  else {
    total = 0
    for (n in Small) {
      if (n != "start" && n != "end")
        # XXX there might be paths that are counted twice; once with ok2=a and
        # once with ok2=a
        # maybe try to do it in one single call to count_distinct_paths
        total += count_distinct_paths("start", X, ok2)
    }
    # total += count_distinct_paths("start")
    print total
  }
}

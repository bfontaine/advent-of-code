function addEdge(n1, n2) {
  if (Edges[n1]) Edges[n1] = Edges[n1] "," n2
  else Edges[n1] = n2
}

function count_distinct_paths(node, visited     , next_node, next_nodes, sum) {
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
      continue
    }

    sum += count_distinct_paths(next_node, visited)
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

  print count_distinct_paths("start")
}

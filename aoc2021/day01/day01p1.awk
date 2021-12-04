{ if ($1 > prev) { inc++ }; prev=$1 }
END { print inc-1 }

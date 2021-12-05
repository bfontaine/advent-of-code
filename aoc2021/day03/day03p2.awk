function get_bit_criteria(numbers, idx, default_,
                       # local
                         i, n) {
  for (i in numbers) {
    # 1: +1, 0: -1
    n += substr(numbers[i], idx, 1) * 2 - 1
  }

  if (n == 0) return default_

  # 1 -> n>0, 0 -> n<0
  return default_ == (n > 0)
}

function select_by_bit(numbers, idx, bit,
                       # local
                       i, size, n) {
  size = length(numbers)
  n = 1

  for (i in numbers) {
    if (substr(numbers[i], idx, 1) == bit) {
      # reuse the same array
      numbers[n] = numbers[i]
      n++
    }
  }

  # delete remaining elements
  for (i=n; i<=size; i++) {
    delete numbers[i];
  }
}

function reduce(numbers, default_, i, bit) {
  i = 1
  while (length(numbers) > 1) {
    bit = get_bit_criteria(numbers, i, default_)
    select_by_bit(numbers, i, bit)
    i++
  }
}

function bin2dec(b, bits, i, d) {
  split(b, bits, "")
  for (i in bits) {
    d = d*2 + bits[i]
  }
  return d
}

{
  co2[i+1] = oxygen[i+1] = $0
  i++
}

END {
  reduce(oxygen, 1)
  reduce(co2, 0)

  print bin2dec(oxygen[1]) * bin2dec(co2[1])
}

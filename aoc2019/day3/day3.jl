#!/usr/bin/env julia

# Resources:
#  https://learnxinyminutes.com/docs/julia/
#  https://en.wikibooks.org/wiki/Introducing_Julia/Dictionaries_and_sets
#  https://en.wikibooks.org/wiki/Introducing_Julia/Arrays_and_tuples#Tuples
#  https://docs.julialang.org/en/v1/manual/types/#Type-Aliases-1

module Wires

const Coordinates = Tuple{Int64, Int64}

const Wire = Array{Coordinates,1}

function parse_direction(direction :: AbstractString)
  len = parse(Int64, direction[2:end])
  letter = direction[1]

  if letter == 'U'
    (0, len)
  elseif letter == 'R'
    (len, 0)
  elseif letter == 'D'
    (0, -len)
  elseif letter == 'L'
    (-len, 0)
  else
    error("Invalid direction '$(direction)'")
  end
end

function gen_range(start :: Int64, offset :: Int64)
  step = offset < 0 ? -1 : 1

  start:step:start+offset
end

function gen_segment(origin :: Coordinates, direction :: Coordinates)
  segment = Wire()

  ox, oy = origin
  px, py = direction

  for x in gen_range(ox, px)
    for y in gen_range(oy, py)
      if x == ox && y == oy
        continue
      end

      push!(segment, (x, y))
    end
  end

  segment
end

function parse_wire(line :: String)
  wire = Wire()
  position :: Coordinates = (0, 0)
  for direction_string = split(line, ",")
    direction = parse_direction(direction_string)

    for coords = gen_segment(position, direction)
      push!(wire, coords)
    end

    position = (position[1]+direction[1], position[2]+direction[2])
  end

  wire
end

function manhattan_distance_to_origin(cell :: Coordinates)
  x, y = cell
  abs(x) + abs(y)
end

function wires_crossing_distance(wire1 :: Wire, wire2 :: Wire)
  crossings = intersect(Set(wire1), Set(wire2))
  minimum(manhattan_distance_to_origin, crossings)
end

function wires_crossing_steps(wire1 :: Wire, wire2 :: Wire)
  best_steps = length(wire1) + length(wire2)

  for (steps1, coords1) in enumerate(wire1)
    if steps1 > best_steps
      break
    end

    for (steps2, coords2) in enumerate(wire2)
      steps = steps1 + steps2
      if steps > best_steps
        break
      end

      if coords1 == coords2 && steps < best_steps
        best_steps = steps
      end
    end
  end

  best_steps
end

function problem1(line1 :: String, line2 :: String)
  wire1 = parse_wire(line1)
  wire2 = parse_wire(line2)

  wires_crossing_distance(wire1, wire2)
end

function problem2(line1 :: String, line2 :: String)
  wire1 = parse_wire(line1)
  wire2 = parse_wire(line2)

  wires_crossing_steps(wire1, wire2)
end

export parse_wire, parse_direction, gen_segment, wires_crossing_distance,
  problem1, problem2

end # end module

if PROGRAM_FILE != "" && realpath(@__FILE__) == realpath(PROGRAM_FILE)
  using Printf

  if isempty(ARGS)
    println("Usage:\n  $(PROGRAM_FILE) 1|2 input.txt")
  else
    using .Wires

    open(ARGS[2]) do f
      line1, line2 = eachline(f)

      if ARGS[1] == "1"
        println(problem1(line1, line2))
      elseif ARGS[1] == "2"
        println(problem2(line1, line2))
      else
        error("Invalid problem number '$(ARGS[1])")
      end
    end
  end
end

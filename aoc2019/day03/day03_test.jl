#!/usr/bin/env julia

using Test

include("day03.jl")
using .Wires: parse_wire, parse_direction, gen_segment, problem1, problem2

@testset "parse_direction" begin
  for direction = ["U0", "L0", "R0", "D0"]
    @test (0,0) == parse_direction(direction)
  end

  @test (1,0) == parse_direction("R1")
  @test (0,1) == parse_direction("U1")
  @test (-1,0) == parse_direction("L1")
  @test (0,-1) == parse_direction("D1")

  @test (45,0) == parse_direction("R45")
  @test (0,10) == parse_direction("U10")
  @test (-3,0) == parse_direction("L3")
  @test (0,-6) == parse_direction("D6")
end

@testset "gen_segment" begin
  origin = (0, 0)
  @test Dict([]) == gen_segment(origin, origin, 1)

  for direction = [(1,0), (0,1), (-1,0), (0,-1)]
    @test Dict(direction => 1) == gen_segment(origin, direction, 1)
  end

  for y = [0, -1, 1, 5]
    @test Dict((1,y)=>1, (2,y)=>2, (3,y)=>3) == gen_segment((0,y), (3,0), 1)
    @test Dict((-1,y)=>1, (-2,y)=>2, (-3,y)=>3) == gen_segment((0,y), (-3,0), 1)
  end

  for x = [0, -1, 1, 5]
    @test Dict((x,1)=>1, (x,2)=>2, (x,3)=>3) == gen_segment((x,0), (0,3), 1)
    @test Dict((x,-1)=>1, (x,-2)=>2, (x,-3)=>3) == gen_segment((x,0), (0,-3), 1)
  end

  @test Dict((1,1)=>1) == gen_segment((0,1), (1,0), 1)
  @test Dict((1,1)=>1) == gen_segment((1,0), (0,1), 1)
end

@testset "parse_wire" begin
  wire = parse_wire("U7")
  @test Dict((0,1)=>1, (0,2)=>2, (0,3)=>3, (0,4)=>4, (0,5)=>5, (0,6)=>6, (0,7)=>7) == wire

  wire = parse_wire("U1,R1")
  @test Dict((0,1)=>1, (1,1)=>2) == wire

  wire = parse_wire("R1,U1")
  @test Dict((1,0)=>1, (1,1)=>2) == wire
end

@testset "problem1" begin
  @test 6 == problem1("R8,U5,L5,D3", "U7,R6,D4,L4")
  @test 159 == problem1("R75,D30,R83,U83,L12,D49,R71,U7,L72",
                        "U62,R66,U55,R34,D71,R55,D58,R83")
  @test 135 == problem1("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                        "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
end

@testset "problem2" begin
  @test 30 == problem2("R8,U5,L5,D3", "U7,R6,D4,L4")
  @test 610 == problem2("R75,D30,R83,U83,L12,D49,R71,U7,L72",
                        "U62,R66,U55,R34,D71,R55,D58,R83")
  @test 410 == problem2("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                        "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
end

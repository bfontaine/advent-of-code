#!/usr/bin/env lua

-- https://www.lua.org/pil/16.1.html

Coords3 = {}

function Coords3:new(x, y, z)
  cx = {
    x = x,
    y = y,
    z = z,
  }
  setmetatable(cx, self)
  self.__index = self
  return cx
end

function Coords3:energy()
  return math.abs(self.x) + math.abs(self.y) + math.abs(self.z)
end


Moon = {}

function Moon:new(x, y, z)
  m = {
    position = Coords3:new(x, y, z),
    velocity = Coords3:new(0, 0, 0),
  }
  setmetatable(m, self)
  self.__index = self
  return m
end

function Moon:apply_velocity()
  -- +=, anyone?
  self.position.x = self.position.x + self.velocity.x
  self.position.y = self.position.y + self.velocity.y
  self.position.z = self.position.z + self.velocity.z
end

AXES = {"x", "y", "z"}

function Moon:apply_gravity(moon)
  -- ipairs(self) doesn't work here, I don't know why
  for _, axis in ipairs(AXES) do
    mine = self.position[axis]
    theirs = moon.position[axis]

    if mine < theirs then
      self.velocity[axis] = self.velocity[axis] + 1
    else
      if mine > theirs then
        self.velocity[axis] = self.velocity[axis] - 1
      end
    end
  end
end

function Moon:potential_energy()
  return self.position:energy()
end

function Moon:kinetic_energy()
  return self.velocity:energy()
end

function Moon:total_energy()
  return self:potential_energy() * self:kinetic_energy()
end

function apply_gravity(moons)
  for i, moon1 in ipairs(moons) do
    for j, moon2 in ipairs(moons) do
      if i ~= j then
        moon1:apply_gravity(moon2)
      end
    end
  end
end

function apply_velocity(moons)
  for _, moon in pairs(moons) do
    moon:apply_velocity()
  end
end

function next_step(moons)
  apply_gravity(moons)
  apply_velocity(moons)
end

function total_energy(moons)
  local energy = 0
  for _, moon in pairs(moons) do
    energy = energy + moon:total_energy()
  end
  return energy
end

-- Return a string describing the situation of all moons on a given axis
function get_situation(moons, axis)
  local situation = {}

  for i, moon in ipairs(moons) do
    situation[i*2 - 1] = moon.position[axis]
    situation[i*2] = moon.velocity[axis]
  end

  return table.concat(situation, "#")
end

function problem1(moons)
  local steps = 1000

  for _=1, steps do
    next_step(moons)
  end

  print(total_energy(moons))
end

function gcd(a, b)
  while b ~= 0 do
    local q = a
    a = b
    b = q % b
  end
  return a
end

function lcm(a, b)
  -- https://en.wikipedia.org/wiki/Least_common_multiple#Calculation
  return math.abs(a*b) / gcd(a, b)
end

function problem2(moons)
  --[[
Intuitions:
* we can't bruteforce, it'd be too long
* axes are independent: what happens on y, z doesn’t affect x, and vice-versa.
  Of course _all_ axes must go back a previous state.
* changes in velocity are a zero-sum game: at any step, the sum of the changes
  in velocity is zero.
* all moons are equal: they all follow the same movement rules, for any
  position and any velocity, all moons would behave the exact same way.
On one axis:
* a one-moon situation never changes state
* a two-moon situation continuously loop between both original states: moon A
  goes from init_A to init_B while moon B goes from init_B to init_A, and again
  and again

One thing that would be great but I'm not sure is true is:
  If any situation goes back to a previous one after some period of time, then
  this is true for each axis, and the revolution of one axis is at most that
  period.
  Each axis has 3 times fewer variables than the situation as a whole so we MAY
  think one axis' revolution period should be significantly shorter than a
  3-axis one.

  That period may be different for each axis. The solution is then to find the
  least common multiple of all periods.

(spoiler from my future me: this intuition was true)
--]]

  local situations = {
    x = {},
    y = {},
    z = {},
  }

  local current_steps = {
    x = 0,
    y = 0,
    z = 0,
  }

  local steps = {}

  while not (steps.x and steps.y and steps.z) do
    for _, axis in ipairs(AXES) do
      -- already matched
      if steps[axis] then
        goto continue
      end

      local situation = get_situation(moons, axis)
      local situation_steps = situations[axis][situation]
      if situations[axis][situation] then
        -- match!
        steps[axis] = current_steps[axis] - situation_steps
        -- cleanup to save memory(?)
        situations[axis] = nil

        print(axis, situation, current_steps[axis], situation_steps)

        goto continue
      end

      -- otherwise mark the situation as seen
      situations[axis][situation] = current_steps[axis]
      current_steps[axis] = current_steps[axis] + 1

      ::continue::
    end

    next_step(moons)
  end

  print("x", steps.x, "y", steps.y, "z", steps.z)

  local total_steps = lcm(lcm(steps.x, steps.y), steps.z)
  print(string.format("%.f", total_steps))
end

function main()
  if #arg ~= 2 then
    print("I need a problem number (1 or 2) and an input.txt!")
    os.exit(1)
  end

  local moons = {}

  local f = io.open(arg[2])
  for line in f:lines() do
    x, y, z = string.match(line, "<x=(-?%d+), y=(-?%d+), z=(-?%d+)>")
    m = Moon:new(tonumber(x), tonumber(y), tonumber(z))
    table.insert(moons, m)
  end
  f:close()

  if arg[1] == "1" then
    problem1(moons)
  else
    if arg[1] == "2" then
      problem2(moons)
    else
      print("Invalid problem number!")
      os.exit(2)
    end
  end
end

main()

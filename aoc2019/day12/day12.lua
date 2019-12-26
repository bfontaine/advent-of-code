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

function Moon:apply_gravity(moon)
  -- ipairs(self) doesn't work here, I don't know why
  for _, axis in ipairs({"x", "y", "z"}) do
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

function step(moons)
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

function main()
  if #arg ~= 1 then
    print("I need an input.txt!")
    os.exit(1)
  end

  local moons = {}
  local steps = 1000

  local f = io.open(arg[1])
  for line in f:lines() do
    x, y, z = string.match(line, "<x=(-?%d+), y=(-?%d+), z=(-?%d+)>")
    m = Moon:new(tonumber(x), tonumber(y), tonumber(z))
    table.insert(moons, m)
  end
  f:close()

  for _=1, steps do
    step(moons)
  end

  print(total_energy(moons))
end

main()

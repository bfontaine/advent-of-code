#!/usr/bin/env crystal

require "../common/intcode"

enum Color
  BLACK
  WHITE

  def to_c
    case self
    when BLACK
      "."
    when WHITE
      "#"
    else
      raise "Unknown color #{self}"
    end
  end
end

enum Turn
  LEFT
  RIGHT
end

alias Position = Tuple(Int32, Int32)

ORIGIN = Position.new(0, 0)

enum Direction
  UP
  RIGHT
  DOWN
  LEFT

  def turn(t)
    increment = case t
                when Turn::LEFT
                  -1
                when Turn::RIGHT
                  +1
                else
                  raise "Unknown turn #{t}"
                end
    Direction.new((self.value + increment) % 4)
  end

  def apply(position : Position)
    x, y = position
    case self
    when UP
      Position.new(x, y-1)
    when DOWN
      Position.new(x, y+1)
    when LEFT
      Position.new(x-1, y)
    when RIGHT
      Position.new(x+1, y)
    else
      raise "Unknown direction #{self}"
    end
  end
end

class Panel
  def initialize
    @positions = {} of Position => Color

    @min_x = 0
    @min_y = 0

    @max_x = 0
    @max_y = 0
  end

  def get(position)
    @positions.fetch(position, Color::BLACK)
  end

  def get(x, y)
    get Position.new(x, y)
  end

  def paint(position, color)
    x, y = position

    if x < @min_x
      @min_x = x
    elsif x > @max_x
      @max_x = x
    end

    if y < @min_y
      @min_y = y
    elsif y > @max_y
      @max_y = y
    end

    @positions[position] = color
  end

  def painted
    @positions.size
  end

  def print
    (@min_y..@max_y).each do |y|
      (@min_x..@max_x).each do |x|
        STDOUT.print get(x, y).to_c
      end
      puts
    end
  end
end

def problem(runner, initial_color = nil)
  panel = Panel.new
  direction = Direction::UP
  position = ORIGIN

  unless initial_color.nil?
    panel.paint(position, initial_color)
  end

  until runner.done?
    # current color
    runner.add_input panel.get(position).value
    runner.run

    # read the new color
    color = Color.new runner.read_output.to_i32
    panel.paint(position, color)

    # read the new direction
    turn = Turn.new runner.read_output.to_i32
    direction = direction.turn turn

    # update the position
    position = direction.apply position
  end

  puts panel.painted
  panel.print
end

if ARGV.size != 2
  puts "Usage: day11 <1|2> <input.txt>"
  exit 1
end

problem = ARGV[0].to_i64

code = File.read(ARGV[1])
instructions = parse_code(code)
runner = IntcodeRunner.new(instructions)

case problem
when 1
  problem(runner)
when 2
  problem(runner, Color::WHITE)
else
  raise "Unkown problem #{problem}"
end

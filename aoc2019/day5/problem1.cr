#!/usr/bin/env crystal

module IntcodeOps
  ADD = 1
  MUL = 2
  HALT = 99
end

class IntcodeRunner
  # Initialize a new runner on the given instructions. Note it modifies its
  # argument.
  def initialize(instructions : Array(Int32))
    @instructions = instructions

    @cursor = 0
    @done = false
  end

  def result : Int32
    @instructions[0]
  end

  def done?
    @done
  end

  def run
    until done?
      run_op
    end
    result
  end

  private def run_op
    op = @instructions[@cursor]

    case op
    when IntcodeOps::ADD
      run_op_ptr2 { |a, b| a + b }
    when IntcodeOps::MUL
      run_op_ptr2 { |a, b| a * b }
    when IntcodeOps::HALT
      @done = true
    end
  end

  private def run_op_ptr2
    pos1, pos2, pos3 = @instructions[@cursor+1..@cursor+3]

    @instructions[pos3] = \
      yield @instructions[pos1], @instructions[pos2]
    @cursor += 4
  end
end

def parse_code(code) : Array(Int32)
  code.chomp.split(",").map(&.to_i)
end

if ARGV.size != 1
  puts "Please give me the input.txt filename!\n"
  exit 1
end

code = File.read(ARGV[0])
instructions = parse_code(code)
instructions[1] = 12
instructions[2] = 2
runner = IntcodeRunner.new(instructions)
puts runner.run

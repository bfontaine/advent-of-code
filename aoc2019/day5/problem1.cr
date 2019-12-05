#!/usr/bin/env crystal

enum IntcodeModes
  POSITION = 0
  IMMEDIATE = 1
end

enum IntcodeOps
  ADD = 1
  MUL = 2
  INPUT = 3
  OUTPUT = 4
  HALT = 99
end

class IntcodeRunner
  # Initialize a new runner on the given instructions. Note it modifies its
  # argument.
  def initialize(instructions : Array(Int32), debug=false)
    @instructions = instructions
    @debug = debug

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
    instruction = @instructions[@cursor]

    modes, op = instruction.divmod(100)

    debug "op=#{op}, modes=#{modes}"

    case op
    when IntcodeOps::ADD.value
      run_op_ptr2(modes) { |a, b| a + b }
    when IntcodeOps::MUL.value
      run_op_ptr2(modes) { |a, b| a * b }
    when IntcodeOps::INPUT.value
      run_op_input
    when IntcodeOps::OUTPUT.value
      run_op_output(modes)
    when IntcodeOps::HALT.value
      @done = true
    else
      raise "Unknown opcode: #{op}"
    end
  end

  private def get_value(offset, modes)
    immediate = @instructions[@cursor+offset+1]
    mode = if modes == 0
             0  # micro-optimization
           else
             # 6789
             # 3210 <- offset
             #
             # offset=2 : 10^2 = 100; 6789/100 = 67; 67 % 10 = 7
             #
             m = (modes / (10 ** (offset))).to_i
             m % 10
           end

    case mode
    when IntcodeModes::IMMEDIATE.value
      debug "val#{offset}: #{immediate}"
      immediate
    when IntcodeModes::POSITION.value
      val = @instructions[immediate]
      debug "val#{offset}: [#{immediate}] = #{val}"
      val
    else
      raise "Unknown mode: #{mode}"
    end
  end

  private def run_op_ptr2(modes)
    # OP, a, b, position
    # position <- block(a, b)

    val1 = get_value(0, modes)
    val2 = get_value(1, modes)

    pos3 = @instructions[@cursor+3]

    res = yield val1, val2

    debug "op2 val1=#{val1} val2=#{val2} pos3=#{pos3} <- #{res}"

    @instructions[pos3] = res
    @cursor += 4
  end

  private def run_op_output(modes)
    # OP, <code>
    output = get_value(0, modes)
    debug "output: #{output}"
    puts output
    @cursor += 2
  end

  private def run_op_input
    # OP, <position>
    # position <- input (always 1 for now)
    position = @instructions[@cursor+1]
    input = 1
    @instructions[position] = input
    debug "input: [#{position}]<- #{input}"

    @cursor += 2
  end

  private def debug(msg)
    return unless @debug
    fragment = @instructions[@cursor..@cursor+4]
    puts "[DEBUG:#{@cursor}: #{fragment.join " "}] #{msg}" if @debug
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
runner = IntcodeRunner.new(instructions)
runner.run

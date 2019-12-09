
enum IntcodeModes
  POSITION = 0
  IMMEDIATE = 1
end

enum IntcodeOps
  ADD = 1
  MUL = 2
  INPUT = 3
  OUTPUT = 4
  JMP_TRUE = 5
  JMP_FALSE = 6
  LT = 7
  EQ = 8
  HALT = 99
end

class IntcodeRunner
  # Initialize a new runner on the given instructions. Note it modifies its
  # argument.
  def initialize(instructions : Array(Int32),
                 debug=false,
                 inputs : Array(Int32)?=nil)
    @instructions = instructions
    @debug = debug
    # without .dup the compiler thinks @inputs can be nil even if it can't
    @inputs = inputs.nil? ? [] of Int32 : inputs.dup

    @outputs = [] of Int32
    @last_output = -1

    @input_position = -1

    @cursor = 0
    @done = false
  end

  # Return the program result
  def result : Int32
    @instructions[0]
  end

  # Return true if the program is done, i.e. it encountered an HALT
  # instruction.
  def done?
    @done
  end

  # Return true if the program needs an input to continue to run.
  def needs_input?
    @input_position >= 0 && @inputs.empty?
  end

  # Return true if the program's last output has yet to be read with
  # .read_output().
  def has_output?
    !@outputs.empty?
  end

  # Run the program until it's done or it needs an input.
  # Return either :done or :needs_input.
  # In the :needs_input case, feed it an input using .add_input(…) and run it
  #  again.
  def run
    until done? || needs_input?
      run_op
    end

    if done?
      :done
    elsif needs_input?
      :needs_input
    end
  end

  # Add an input to the inputs queue.
  def add_input(value : Int32)
    @inputs << value
  end

  # Read the program's last unread output.
  def read_output
    output = @outputs.shift
    @last_output = output
  end

  # Return the last read output
  def last_output
    @last_output
  end

  # -- Private API --

  private def run_op
    instruction = @instructions[@cursor]

    modes, op = instruction.divmod(100)

    debug "op=#{op}, modes=#{modes}"

    case op
    # add/mul
    when IntcodeOps::ADD.value
      run_op2(modes) { |a, b| a + b }
    when IntcodeOps::MUL.value
      run_op2(modes) { |a, b| a * b }

    # I/O
    when IntcodeOps::INPUT.value
      run_op_input
    when IntcodeOps::OUTPUT.value
      run_op_output(modes)

    # Jumps
    when IntcodeOps::JMP_TRUE.value
      run_op_jmp(modes) { |value| value != 0 }
    when IntcodeOps::JMP_FALSE.value
      run_op_jmp(modes) { |value| value == 0 }

    # Comparisons
    when IntcodeOps::LT.value
      run_op2(modes) { |a, b| a < b ? 1 : 0 }
    when IntcodeOps::EQ.value
      run_op2(modes) { |a, b| a == b ? 1 : 0 }

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

  # Run all operations with two parameters and one position for the result
  private def run_op2(modes)
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
    @outputs << output
    @cursor += 2
  end

  private def run_op_input
    # OP, <position>
    # position <- input
    position = @instructions[@cursor+1]

    if @inputs.empty?
      @input_position = position
      return
    end

    @input_position = -1

    input = @inputs.shift
    @instructions[position] = input
    debug "input: [#{position}]<- #{input}"

    @cursor += 2
  end

  private def run_op_jmp(modes)
    val1 = get_value(0, modes)
    ok = yield val1
    unless ok
      @cursor += 3
      return
    end

    @cursor = get_value(1, modes)
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

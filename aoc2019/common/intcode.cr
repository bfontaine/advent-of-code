
enum IntcodeModes
  POSITION = 0
  IMMEDIATE = 1
  RELATIVE = 2
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
  RELATIVE_BASE = 9
  HALT = 99
end

alias IntcodeValue = Int64
alias IntcodePosition = IntcodeValue

# shortcuts
INTCODE_0 = IntcodeValue.new 0
INTCODE_1 = IntcodeValue.new 1


class IntcodeRunner
  @instructions : Hash(IntcodePosition, IntcodeValue)

  @cursor : IntcodePosition
  @relative_base : IntcodePosition
  @input_position : IntcodePosition

  @last_output : IntcodeValue

  # Initialize a new runner on the given instructions.
  def initialize(instructions : Array(IntcodeValue),
                 debug=false,
                 inputs : Array(IntcodeValue|Int32)?=nil)

    positions = (0..instructions.size-1).map(&.to_i64).to_a

    # Use a hash in order to allow arbitrary positions
    @instructions = Hash.zip(positions, instructions)
    @debug = debug
    # without .dup the compiler thinks @inputs can be nil even if it can't
    @inputs = inputs.nil? ? [] of IntcodeValue : inputs.map(&.to_i64)

    @outputs = [] of IntcodeValue
    @last_output = -1

    @cursor = 0
    @relative_base = 0
    @input_position = -1

    @done = false
  end

  # Return the program result
  def result : IntcodeValue
    read 0
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
  def add_input(value : IntcodeValue)
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
    instruction = read @cursor

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
      run_op2(modes) { |a, b| a < b ? INTCODE_1 : INTCODE_0 }
    when IntcodeOps::EQ.value
      run_op2(modes) { |a, b| a == b ? INTCODE_1 : INTCODE_0 }

    # Relative base
    when IntcodeOps::RELATIVE_BASE.value
      run_op_relative_base(modes)

    when IntcodeOps::HALT.value
      @done = true
    else
      raise "Unknown opcode: #{op}"
    end
  end

  private def get_value(offset, modes)
    immediate = read(@cursor+offset+1)
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
      val = read immediate
      debug "val#{offset}: [#{immediate}] = #{val}"
      val
    when IntcodeModes::RELATIVE.value
      position = @relative_base + immediate
      val = read position
      debug "val#{offset}: [#{position}] = #{val}"
      val
    else
      raise "Unknown mode: #{mode}"
    end
  end

  # Run all operations with two parameters and one position for the result
  private def run_op2(modes, &block: IntcodeValue, IntcodeValue -> IntcodeValue)
    # OP, a, b, position
    # position <- block(a, b)

    val1 = get_value(0, modes)
    val2 = get_value(1, modes)

    pos3 = read(@cursor+3)

    res = yield val1, val2

    debug "op2 val1=#{val1} val2=#{val2} pos3=#{pos3} <- #{res}"

    write pos3, res
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
    position = read(@cursor+1)

    if @inputs.empty?
      @input_position = position
      return
    end

    @input_position = -1

    input = @inputs.shift
    write position, input
    debug "input: [#{position}]<- #{input}"

    @cursor += 2
  end

  private def run_op_jmp(modes)
    val1 = get_value(0, modes)
    jump = yield val1
    if jump
      @cursor = get_value(1, modes)
    else
      @cursor += 3
    end
  end

  private def run_op_relative_base(modes)
    val = get_value(0, modes)
    @relative_base += val
    @cursor += 2
  end

  private def write(position : IntcodePosition, value : IntcodeValue)
    @instructions[position] = value
  end

  private def read(position : IntcodePosition)
    @instructions.fetch(position, IntcodeValue.new(0))
  end

  private def debug(msg)
    return unless @debug
    fragment = (@cursor..@cursor+4).map { |i| read i }
    puts "[DEBUG:#{@cursor}: #{fragment.join " "}] #{msg}" if @debug
  end
end

def parse_code(code) : Array(IntcodeValue)
  code.chomp.split(",").map(&.to_i64)
end

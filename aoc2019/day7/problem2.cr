#!/usr/bin/env crystal

require "option_parser"
require "../common/intcode"

if ARGV.size != 1
  puts "I need an input.txt!"
  exit 1
end

def run_loop(instructions, phases)
  amplifiers = phases.map do |phase|
    IntcodeRunner.new instructions, inputs: [phase]
  end

  last_output = -1

  amplifier_a = amplifiers[0]
  amplifier_e = amplifiers[-1]

  amplifier_a.add_input 0

  # run one loop first in order to get to the point where each amplifier needs
  # an input.
  amplifiers.each do |amplifier|
    amplifier.run
  end

  until amplifier_e.done?
    # read each amplifier's output and feed it to the next one
    amplifiers.each_with_index do |amplifier, i|
      next if i == 0

      amplifier.add_input amplifiers[i-1].read_output
      amplifier.run
    end

    # feedback loop: feed the first amplifier with the last's output
    amplifier_a.add_input amplifier_e.read_output
    amplifier_a.run
  end

  amplifier_e.last_output
end

code = File.read(ARGV[0])
instructions = parse_code(code)

highest_output = 0

(5..9).to_a.each_permutation do |phases|
  output = run_loop(instructions, phases)
  highest_output = output if output > highest_output
end

puts highest_output

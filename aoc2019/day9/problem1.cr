#!/usr/bin/env crystal

require "../common/intcode"

if ARGV.size != 1
  puts "I need an input.txt!"
  exit 1
end

code = File.read(ARGV[0])
instructions = parse_code(code)
runner = IntcodeRunner.new(instructions, inputs: [1])
runner.run
while runner.has_output?
  puts runner.read_output
end

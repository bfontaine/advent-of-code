#!/usr/bin/env crystal

require "../common/intcode"

if ARGV.size != 2
  puts "Usage: day9 <1|2> <input.txt>"
  exit 1
end

problem = ARGV[0].to_i64

code = File.read(ARGV[1])
instructions = parse_code(code)
runner = IntcodeRunner.new(instructions, inputs: [problem])
runner.run

while runner.has_output?
  puts runner.read_output
end

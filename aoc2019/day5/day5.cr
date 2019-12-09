#!/usr/bin/env crystal

require "option_parser"
require "../common/intcode"

inputs = [] of Int32
filenames = [] of String

OptionParser.parse do |parser|
  parser.banner = "Usage: day5 [options] <input.txt>"

  parser.unknown_args do |filenames_|
    filenames = filenames_
  end

  parser.on("-i INPUTS", "--inputs=INPUTS",
            "Feed the program with these comma-separated inputs") do |s|
    inputs = parse_code(s)
  end

  parser.on("-h", "--help", "Show this help") { puts parser }
end

if filenames.size != 1
  puts "Please give me one input.txt filename!\n"
  exit 1
end

code = File.read(filenames[0])
instructions = parse_code(code)
runner = IntcodeRunner.new(instructions, inputs: inputs)
runner.run

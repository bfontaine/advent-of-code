#!/usr/bin/env coffee

layer_size = 25 * 6

fewest_zeroes = layer_size + 1
checksum = 0

if process.argv.length < 3
  console.log("Please give me a filename")
  process.exit(1)

input = require('fs').readFileSync process.argv[2], 'utf-8'

layers = input.length / layer_size

layer_digit_count = (layer, digit) ->
  ( digit_ for digit_ in layer when digit_ == digit ).length

layer_checksum = (layer) ->
  layer_digit_count(layer, "1") * layer_digit_count(layer, "2")

for layer_index in [0..layers-1]
  layer = input.slice(layer_index*layer_size, (layer_index+1)*layer_size)

  zeroes = layer_digit_count(layer, "0")

  if zeroes < fewest_zeroes
    fewest_zeroes = zeroes
    checksum = layer_checksum layer

console.log checksum

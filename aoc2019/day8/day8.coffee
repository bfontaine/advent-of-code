#!/usr/bin/env coffee

LAYER_WIDTH = 25
LAYER_HEIGHT = 6
LAYER_SIZE = LAYER_WIDTH * LAYER_HEIGHT

fewest_zeroes = LAYER_SIZE + 1
checksum = 0

if process.argv.length < 3
  console.log("Please give me a filename")
  process.exit(1)

input = require('fs').readFileSync process.argv[2], 'utf-8'

layers = input.length / LAYER_SIZE

layer_digit_count = (layer, digit) ->
  ( digit_ for digit_ in layer when digit_ == digit ).length

layer_checksum = (layer) ->
  layer_digit_count(layer, "1") * layer_digit_count(layer, "2")

for layer_index in [0..layers-1]
  layer = input.slice(layer_index*LAYER_SIZE, (layer_index+1)*LAYER_SIZE)

  zeroes = layer_digit_count(layer, "0")

  if zeroes < fewest_zeroes
    fewest_zeroes = zeroes
    checksum = layer_checksum layer

console.log "Layer checksum:", checksum

max_index = input.length - 1

console.log ("-" for _ in [1..LAYER_WIDTH]).join ""

for y in [0..LAYER_HEIGHT-1]
  for x in [0..LAYER_WIDTH-1]
    pixel_index = y * LAYER_WIDTH + x

    pixel_value = ( input[i] for i in [pixel_index..max_index] by LAYER_SIZE \
                      when input[i] != "2")[0]

    process.stdout.write if pixel_value == "0" then " " else "M"

  process.stdout.write "\n"

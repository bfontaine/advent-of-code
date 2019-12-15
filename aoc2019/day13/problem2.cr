#!/usr/bin/env crystal

require "../common/intcode"

enum Tile : Int64
  EMPTY
  WALL
  BLOCK
  PADDLE
  BALL

  def to_c
    case self
    when EMPTY; " "
    when WALL; "#"
    when BLOCK; "□"
    when PADDLE; "—"
    when BALL; "o"
    else raise "Unknown tile #{self}"
    end
  end
end

class Game
  @score : Int64
  @height : Int64

  @paddle_x : Int64
  @ball_x : Int64

  getter :score

  def initialize(internal_instructions, gui = false, autoplay = false)
    @runner = IntcodeRunner.new internal_instructions
    @gui = gui
    @autoplay = autoplay

    @score = 0
    @height = 0

    @paddle_x = 0

    @ball_x = -1
  end

  def insert_money!
    # "Memory address 0 represents the number of quarters that have been
    #  inserted; set it to 2 to play for free."
    @runner.overwrite 0, 2
  end

  def play!
    # when autoplaying, wait one turn at the beginning to get the ball's
    # direction.
    @runner.add_input 0 if @autoplay

    until @runner.done?
      @runner.run
      while @runner.has_output?
        # Read the position
        x = @runner.read_output
        y = @runner.read_output
        value = @runner.read_output

        if x == -1 && y == 0
          @score = value
          next
        end

        tile = Tile.new value

        # Internal state update
        @height = y if y > @height

        case tile
        when Tile::PADDLE
          @paddle_x = x
        when Tile::BALL
          @ball_x = x
        end

        # GUI
        draw_tile x, y, tile
      end

      if @runner.needs_input?
        if @autoplay
          autoplay_move!
        else
          read_player_input!
        end
      end
    end
  end

  private def autoplay_move!
    @runner.add_input next_autoplay_move
    # sleep so we can see something. Change this to a higher value for a slower
    # game.
    sleep 0.01
  end

  private def next_autoplay_move
    # The ball can hit the side of the paddle, so no need to be perfectly under
    # the ball's hit position.
    if @paddle_x < @ball_x
      # move to right
      1
    elsif @ball_x < @paddle_x
      # move to left
      -1
    else
      # don't move
      0
    end
  end

  private def read_player_input!
    STDOUT.print "\033[#{@height + 2};#{0}Hinput> "
    STDOUT.flush
    @runner.add_input gets.not_nil!.chomp.to_i64
    # erase the input
    puts "\033[#{@height + 2};#{0}H                  "
  end

  private def draw_tile(x, y, tile)
    return unless @gui

    # https://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
    puts "\033[#{y + 2};#{x + 1}H#{tile.to_c}"
  end
end

if ARGV.size != 1
  puts "Usage: problem2 <input.txt>"
  exit 1
end

code = File.read(ARGV[0])
instructions = parse_code(code)

g = Game.new instructions, true, true
g.insert_money!
g.play!
puts g.score

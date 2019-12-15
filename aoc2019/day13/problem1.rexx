#!/usr/bin/env rexx

/* Resources:
 * - Basics:
 *     https://www.tutorialspoint.com/rexx/rexx_basic_syntax.htm
 * - Built-in commands:
 *     https://linux.die.net/man/1/regina
 * - Executing external commands:
 *     https://web.archive.org/web/20170619155444/http://www.nokix.pasjagsm.pl/help/learn_rexx/cmds.htm
 *     http://www.ibiblio.org/pub/micro/pc-stuff/freedos/files/devel/rexx/old/v3.4/regina34.pdf
 *     (page 30)
 *
 * Undeclared variables contain their name as a string (all-caps).
 */

if ARG(1, E) == 0 then do
  say "Usage: problem1.rexx <input.txt>"
  exit
end

inputfile = ARG(1)
input = linein(inputfile)

if input == "" then do
  say inputfile "doesn't exist or is empty."
  exit
end

/* strings are sent directly to the environment (SH, here). */
ADDRESS SYSTEM WITH OUTPUT STEM out.
"../day05/day05" inputfile
ADDRESS


blocks = 0

/* number of output lines: out.0
 * line 1: out.1
 * line 2: out.2
 * etc.
 */
do i = 1 to out.0 by 3
  i1 = i + 1
  i2 = i + 2

  x = out.i
  y = out.i1
  tile = out.i2

  ADDRESS SYSTEM WITH OUTPUT NORMAL
    "tput cup " y+1 x
  ADDRESS

  if tile == 0 then
    say " "
  else if tile == 1 then
    say "#"
  else if tile == 2 then
    do
      say "M"
      blocks += 1
    end
  else if tile == 3 then
    say "-"
  else if tile == 4 then
    say "o"
end

say ""
say blocks

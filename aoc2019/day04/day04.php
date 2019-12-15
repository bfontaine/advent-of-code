#!/usr/bin/env php
<?php

function ok($number, $problem) {
    // 6-digits number: already ok if within the range min-max

    $s = "$number";
    $prev_digit = null;

    $adjacent_digits = false;

    $series = $s[0];
    $series_length = 1;

    for ($i = 1; $i < strlen($s); $i++) {
        $digit = $s[$i];
        $prev_digit = $s[$i-1];

        if ($prev_digit > $digit) {
            return false;
        }

        if ($problem == 2) {
            if ($digit == $series) {
                $series_length += 1;
            } else {
                if ($series_length == 2) {
                    $adjacent_digits = true;
                }
                $series = $digit;
                $series_length = 1;
            }
        }

        if ($problem == 1 && $prev_digit == $digit) {
            $curr_adjacent = true;

            if ($problem == 2 && $prev_prev_digit == $prev_digit) {
                $adjacent_digits = false;
            } else {
                $adjacent_digits = true;
            }
        }
    }
    if ($problem == 2 && $series_length == 2) {
        return true;
    }

    return $adjacent_digits;
}

if ($argv && $argv[0] && realpath($argv[0]) === __FILE__) {
    $problem = $argv[1];
    $input = explode("-", $argv[2], 2);
    $min = intval($input[0]);
    $max = intval($input[1]);

    $count = 0;

    foreach(range($min, $max) as $number) {
        if (ok($number, $problem)) {
            $count++;
        }
    }

    echo "$count\n" ;
}

?>

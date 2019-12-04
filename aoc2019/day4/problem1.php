#!/usr/bin/env php
<?php

function ok($number) {
    // 6-digits number: already ok if within the range min-max

    $s = "$number";
    $prev_digit = null;
    $adjacent_digits = false;

    for ($i = 1; $i < strlen($s); $i++) {
        $digit = $s[$i];
        $prev_digit = $s[$i-1];

        if ($prev_digit > $digit) {
            return false;
        }
        if ($prev_digit == $digit) {
            $adjacent_digits = true;
        }
    }

    return $adjacent_digits;
}

if ($argv && $argv[0] && realpath($argv[0]) === __FILE__) {
    $input = explode("-", $argv[1], 2);
    $min = intval($input[0]);
    $max = intval($input[1]);

    $count = 0;

    foreach(range($min, $max) as $number) {
        if (ok($number)) {
            $count++;
        }
    }

    echo "$count\n" ;
}

?>

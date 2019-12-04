#!/usr/bin/env php
<?php

require_once "./day4.php";

function assert_ok($expected, $number, $problem) {
    if ($expected == ok($number, $problem)) {
        echo "[ OK ] $number, $problem\n";
    } else {
        echo "[FAIL] $number, $problem: expected '$expected'\n";
    }
}

echo "== Problem 1 ==\n";
foreach([122345, 111111] as $number) {
    assert_ok(true, $number, 1);
}

foreach([223450, 123789] as $number) {
    assert_ok(false, $number, 1);
}

echo "== Problem 2 ==\n";
foreach([122345, 112233, 111122, 112222] as $number) {
    assert_ok(true, $number, 2);
}

foreach([223450, 123789, 123444, 111111, 122221] as $number) {
    assert_ok(false, $number, 2);
}

?>

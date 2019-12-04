#!/usr/bin/env php
<?php

require_once "./problem1.php";

function assert_ok($expected, $number) {
    if ($expected == ok($number)) {
        echo "[ OK ] $number\n";
    } else {
        echo "[FAIL] $number: expected '$expected'\n";
    }
}

foreach([122345, 111111] as $number) {
    assert_ok(true, $number);
}

foreach([223450, 123789] as $number) {
    assert_ok(false, $number);
}

?>

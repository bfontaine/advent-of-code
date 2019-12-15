#! /usr/bin/env perl

use strict;
use warnings;

# https://metacpan.org/pod/Algorithm::Permute
use Algorithm::Permute;

my $filename = shift or die "Usage: $0 <input.txt>\n";

my @phases = 0..4;

my $highest_signal = 0;

Algorithm::Permute::permute {
  my $signal = "0";
  for my $phase (@phases) {
    chomp($signal = `../day05/day05 --inputs=$phase,$signal $filename`);
  }
  if ($signal > $highest_signal) {
    $highest_signal = $signal;
  }
  #print "-- $signal\n";
} @phases;

print "Highest signal: $highest_signal";

(ns aoc2018.p02-test
  (:require [clojure.test :refer :all]
            [aoc2018.p02 :as p]))

(deftest box-id-counts
  (are [counts box-id] (= counts (p/box-id-counts box-id))

       [0 0] "abcdef"
       [1 1] "bababc"
       [1 0] "abbcde"
       [0 1] "abcccd"
       [1 0] "aabcdd"
       [1 0] "abcdee"
       [0 1] "ababab"))

(deftest box-ids-checksum
  (is (= 12
         (p/box-ids-checksum
           ["abcdef"
            "bababc"
            "abbcde"
            "abcccd"
            "aabcdd"
            "abcdee"
            "ababab"]))))

(deftest one-letter-removals
  (is (= '("bcdef"
           "acdef"
           "abdef"
           "abcef"
           "abcdf"
           "abcde")
         (p/one-letter-removals "abcdef"))))

(deftest correct-common-letters
  (is (= "fgij"
         (p/correct-common-letters
           ["abcde"
            "fghij"
            "klmno"
            "pqrst"
            "fguij"
            "axcye"
            "wvxyz"]))))

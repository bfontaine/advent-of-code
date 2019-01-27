(ns aoc2018.p05-test
  (:require [clojure.test :refer :all]
            [aoc2018.p05 :as p]))

(deftest scan-polymer
  (are [expected raw] (= expected (p/scan-polymer raw))

       "" "aA"
       "" "abBA"
       "abAB" "abAB"
       "aabAAB" "aabAAB"
       "dabCBAcaDA" "dabAcCaCBAcCcaDA"))

(ns aoc2018.p1-test
  (:require [clojure.test :refer :all]
            [aoc2018.p1 :as p1]))

(deftest get-frequency
  (are [freq changes] (= freq (p1/get-frequency changes))

        3 [+1 -2 +3 +1]
        3 [+1 +1 +1]
        0 [+1 +1 -2]
       -6 [-1 -2 -3]))

(deftest duplicated-frequency
  (are [freq changes] (= freq (p1/get-duplicated-frequency changes))
        0 [+1 -1]
       10 [+3 +3 +4 -2 -4]
        5 [-6 +3 +8 +5 -6]
       14 [+7 +7 -2 -7 -4]))

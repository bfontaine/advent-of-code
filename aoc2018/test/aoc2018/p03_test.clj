(ns aoc2018.p03-test
  (:require [clojure.test :refer :all]
            [aoc2018.p03 :as p]))

(deftest parse-line
  (is (= [123
          [3
           2
           5
           4]]
         (p/parse-line "#123 @ 3,2: 5x4"))))

(deftest overlap-size
  (is (= 0 (p/overlap-size [])))
  (is (= 0 (p/overlap-size [(p/parse-line "#1 @ 1,1: 100x100")])))
  (is (= 4 (p/overlap-size
              (map p/parse-line
                   ["#1 @ 1,3: 4x4"
                    "#2 @ 3,1: 4x4"
                    "#3 @ 5,5: 2x2"])))))

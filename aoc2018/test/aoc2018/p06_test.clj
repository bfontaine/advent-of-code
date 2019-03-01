(ns aoc2018.p06-test
  (:require [clojure.test :refer :all]
            [aoc2018.p06 :as p]))

(deftest closest-coordinates
  (are [expected x y] (= expected (p/closest-coordinates x y [[1 1] [2 2] [3 3]]))

       [1 1] 0 0
       [3 3] 3 3
       [3 3] 3 4
       [3 3] 6 6
       nil   1 2)

  ;   01234
  ; 0 dDdee
  ; 1 ddeEe
  (are [expected x y] (= expected (p/closest-coordinates x y [[1 0] [3 1]]))

       ; D
       [1 0] 0 0
       [1 0] 0 1
       [1 0] 0 2
       [1 0] 1 1
       [1 0] 0 1
       ; E
       [3 1] 3 0
       [3 1] 4 0
       [3 1] 2 1
       [3 1] 3 1
       [3 1] 4 1)

  (is (= [5 5] (p/closest-coordinates 4 6 [[1 1] [1 6] [8 3] [3 4] [5 5] [8 9]]))))

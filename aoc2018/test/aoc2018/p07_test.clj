(ns aoc2018.p07-test
  (:require [clojure.test :refer :all]
            [aoc2018.p07 :as p]))

(deftest example
  (is (= "CABDFE"
         (p/solution1-lines
           ["Step C must be finished before step A can begin."
            "Step C must be finished before step F can begin."
            "Step A must be finished before step B can begin."
            "Step A must be finished before step D can begin."
            "Step B must be finished before step E can begin."
            "Step D must be finished before step E can begin."
            "Step F must be finished before step E can begin."]))))

(ns aoc2018.p04-test
  (:require [clojure.test :refer :all]
            [aoc2018.p04 :as p]))

(deftest parse-line
  (are [expected line] (= expected (p/parse-line line))

       {:date "2018-02-04"
        :hours 19
        :minutes 58
        :action :shift-start
        :guard "42"}
       "[2018-02-04 19:58] Guard #42 begins shift"

       {:date "1518-04-06"
        :hours 0
        :minutes 27
        :action :sleep-end}
       "[1518-04-06 00:27] wakes up"

       {:date "1518-06-03"
        :hours 0
        :minutes 18
        :action :sleep-start}
       "[1518-06-03 00:18] falls asleep"))

(def ^:private
  sample-lines
  (map p/parse-line
       ["[1518-11-01 00:25] wakes up"
        "[1518-11-03 00:05] Guard #10 begins shift"
        "[1518-11-01 00:30] falls asleep"
        "[1518-11-01 00:05] falls asleep"
        "[1518-11-03 00:29] wakes up"
        "[1518-11-04 00:36] falls asleep"
        "[1518-11-03 00:24] falls asleep"
        "[1518-11-05 00:55] wakes up"
        "[1518-11-04 00:46] wakes up"
        "[1518-11-01 23:58] Guard #99 begins shift"
        "[1518-11-01 00:55] wakes up"
        "[1518-11-05 00:45] falls asleep"
        "[1518-11-02 00:50] wakes up"
        "[1518-11-04 00:02] Guard #99 begins shift"
        "[1518-11-01 00:00] Guard #10 begins shift"
        "[1518-11-02 00:40] falls asleep"
        "[1518-11-05 00:03] Guard #99 begins shift"]))

(def ^:private
  sample-shifts
  {"1518-11-01" {:guard "10" :sleeps '(55 30 25 5)}
   "1518-11-02" {:guard "99" :sleeps '(50 40)}
   "1518-11-03" {:guard "10" :sleeps '(29 24)}
   "1518-11-04" {:guard "99" :sleeps '(46 36)}
   "1518-11-05" {:guard "99" :sleeps '(55 45)}})

(deftest build-shifts
  (is (= sample-shifts (p/build-shifts sample-lines)))
  (doseq [_ (range 5)]
    (is (= sample-shifts (p/build-shifts (shuffle sample-lines))))))

(deftest shifts-by-guard
  (is (= {"10" ['(29 24) '(55 30 25 5)]
          "99" ['(46 36) '(50 40) '(55 45)]}

         (p/shifts-by-guard sample-shifts))))

(deftest fill-minutes-map
  (are [minutes-map sleeps] (= minutes-map (p/fill-minutes-map {} sleeps))

       {} '()
       {0 1} '(1 0)
       {0 1, 1 1, 2 1, 10 1, 11 1} '(12 10 3 0)))

(deftest guard-shifts->minutes-map
  ;; 0
  ;; 0123456789
  ;; ###    ###
  ;;   ####
  ;;  ## ## ##
  ;; 123122 221
  (is (= {0 1
          1 2
          2 3
          3 1
          4 2
          5 2
          7 2
          8 2
          9 1}
         (p/guard-shifts->minutes-map ['(10 7 3 0)
                                       '(6 2)
                                       '(9 7 6 4 3 1)]))))

(deftest solution1-lines
  (is (= 240 (p/solution1-lines sample-lines))))

(deftest solution2-lines
  (is (= 4455 (p/solution2-lines sample-lines))))

(ns aoc2018.p2
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn box-id-counts
  [box-id]
  (let [m (set/map-invert (frequencies box-id))]
    [(if (m 2) 1 0)
     (if (m 3) 1 0)]))

(defn box-ids-checksum
  [box-ids]
  (let [counts (map box-id-counts box-ids)]
    (*
     (reduce + (map first counts))
     (reduce + (map second counts)))))

(defn solution1
  [filename]
  (println
    (box-ids-checksum
      (str/split-lines (slurp filename)))))


(defn one-letter-removals
  [s]
  (map (fn [idx]
         (str (subs s 0 idx) (subs s (inc idx))))
       (range (count s))))

(defn correct-common-letters
  [box-ids]
  (loop [seen #{}
         box-ids box-ids]
    (when-not (empty? box-ids)
      (let [box-id (first box-ids)
            removals (one-letter-removals box-id)]
        (if-let [common-letters (some seen removals)]
          common-letters
          (recur (into seen removals)
                 (rest box-ids)))))))

(defn solution2
  [filename]
  (println
    (correct-common-letters
      (str/split-lines (slurp filename)))))

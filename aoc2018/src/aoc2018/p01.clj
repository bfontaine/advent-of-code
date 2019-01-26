(ns aoc2018.p01
  (:require [clojure.string :as str]))

(defn- parse-file
  [filename]
  (->> filename
       slurp
       str/split-lines
       (map #(Long/parseLong %))))


(def get-frequency
  (partial reduce +))

(defn solution1
  [filename]
  (->> filename
       parse-file
       get-frequency
       println))


(defn get-duplicated-frequency
  [changes]
  (loop [seen #{0}
         freq 0
         changes (cycle changes)]
    (let [freq (+ freq (first changes))]
      (if (seen freq)
        freq
        (recur (conj seen freq) freq (rest changes))))))

(defn solution2
  [filename]
  (->> filename
       parse-file
       get-duplicated-frequency
       println))

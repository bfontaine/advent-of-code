(ns aoc2018.p1
  (:require [clojure.string :as str]))

(def get-frequency
  (partial reduce +))

(defn solution
  [filename]
  (->> filename
       slurp
       str/split-lines
       (map #(Long/parseLong %))
       get-frequency
       println))

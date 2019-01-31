(ns aoc2018.p03
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn parse-line
  [line]
  (let [[x y width height]
        (->> (re-matches #"#\d+ @ (\d+),(\d+): (\d+)x(\d+)$" line)
             rest
             (map  #(Long/parseLong %)))]
    [x y width height]))

(defn solution1
  [filename]
  (->> (slurp filename)
       str/split-lines
       (map parse-line)
       ;; {(x, y) -> #
       (reduce (fn [acc [x y width height]] ; elves
                  (reduce (fn [acc x] ; x
                            (reduce (fn [acc y] ; y
                                      (update acc [x y] (fn [n]
                                                           (if n
                                                             (inc n)
                                                             1))))
                                    acc
                                    (range y (+ y height))))

                          acc
                          (range x (+ x width))))
               {})
       (filter (fn [[_ n]] (> n 1)))
       count))

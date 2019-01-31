(ns aoc2018.p03
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn parse-line
  [line]
  (let [[claim x y width height]
        (->> (re-matches #"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$" line)
             rest
             (map  #(Long/parseLong %)))]
    [claim x y width height]))

(defn parse-file
  [filename]
  (->> (slurp filename)
       str/split-lines
       (map parse-line)))

(defn fill-matrix
  [lines]
  ;; {(x, y) -> #
  (reduce (fn [acc [_ x y width height]] ; elves
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
          {}
          lines))

(defn solution1
  [filename]
  (->> (parse-file filename)
       fill-matrix
       (filter (fn [[_ n]] (> n 1)))
       count))

(defn pixels
  [x y width height]
  (for [x (range x (+ x width))
        y (range y (+ y height))]
    [x y]))

(defn matrix-pixels
  [m x y width height]
  (map #(get m %) (pixels x y width height)))

(defn solution2
  [filename]
  (let [claims (parse-file filename)
        matrix (fill-matrix claims)]
    (->> claims
         (filter (fn [[claim x y width height]]
                   (every? #(= 1 %)
                           (matrix-pixels matrix x y width height))))
         (map first))))

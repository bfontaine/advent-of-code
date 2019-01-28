(ns aoc2018.p03
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn parse-line
  [line]
  (let [[claim x y width height]
        (->> (re-matches #"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$" line)
             rest
             (map  #(Long/parseLong %)))]
    [claim [x y width height]]))

(defn parse-file
  [filename]
  (->> (slurp filename)
       str/split-lines
       (map parse-line)))

(defn update-pixels
  [m [x y width height] f]
  (reduce (fn [m x] ; x
            (reduce (fn [m y] ; y
                      (update m [x y] f))
                    m
                    (range y (+ y height))))

          m
          (range x (+ x width))))

(defn fill-matrix
  [lines]
  ;; {(x, y) -> n
  (reduce (fn [acc [_ coords]] ; elves
            (update-pixels acc coords (fn [n] (if n
                                                (inc n)
                                                1))))
          {}
          lines))

(defn pixels
  [[x y width height]]
  (for [x (range x (+ x width))
        y (range y (+ y height))]
    [x y]))

(defn matrix-pixels
  [m coords]
  (map #(get m %) (pixels coords)))

(defn overlap-size
  [claims]
  (->> claims
       fill-matrix
       (filter (fn [[_ n]] (> n 1)))
       count))

(defn solution1
  [filename]
  (overlap-size
    (parse-file filename)))

(defn solution2
  [filename]
  ;; Very inefficient, but it works(TM)
  (let [claims (parse-file filename)
        matrix (fill-matrix claims)]
    (->> claims
         (filter (fn [[claim coords]]
                   (every? #(= 1 %)
                           (matrix-pixels matrix coords))))
         ffirst)))

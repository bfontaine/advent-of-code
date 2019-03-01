(ns aoc2018.p06
  (:require [clojure.string :as str]))

(defn read-file
  [filename]
  (->> (slurp filename)
       str/split-lines
       (map (fn [line]
              (let [[x y] (map #(Long/parseLong %) (str/split line #", "))]
                [x y])))))

(defn manhattan
  [x1 y1 x2 y2]
  (+ (Math/abs (- x1 x2))
     (Math/abs (- y1 y2))))

(defn closest-coordinates
  [x y coords]
  (let [candidates (->> coords
                        (group-by (fn [[x1 x2]] (manhattan x y x1 x2)))
                        sort
                        first
                        second)]
    (if (= 1 (count candidates))
      (first candidates))))

(defn edge?
  [x y max-x max-y]
  (or
    (zero? x)
    (zero? y)
    (= max-x x)
    (= max-y y)))

(defn build-map
  [coords]
  (let [max-x (reduce max 0 (map first coords))
        max-y (reduce max 0 (map second coords))]
    (reduce (fn [m x]
              (reduce (fn [m y]
                        (let [closest (closest-coordinates x y coords)
                              is-edge (edge? x y max-x max-y)]

                          (cond
                            (nil? closest)
                            m

                            is-edge
                            (assoc-in m [closest :ignore] true)

                          ; (:ignore (get m closest))
                          ; m

                            :else
                            (update-in m [closest :count] (fn [cnt]
                                                            (if (nil? cnt)
                                                              1
                                                              (inc cnt)))))))
                      m
                      (range 0 (inc max-y))))
            {}
            (range 0 (inc max-x)))))

(defn solution1
  [filename]
  (->> (read-file filename)
       build-map
       vals
       (remove :ignore)
       (map :count)
       (reduce max)))

(defn solution2
  [filename]
  )

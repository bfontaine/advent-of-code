(ns day11
  (:require [clojure.string :as str]))

(def directions
  [[-1 0]                                                             ; left
   [-1 -1]                                                            ; top-left
   [0 -1]                                                             ; top
   [1 -1]                                                             ; etc.
   [1 0]
   [1 1]
   [0 1]
   [-1 1]])

(defn read-layout
  [filename]
  (->> (slurp filename)
       str/split-lines
       (map-indexed vector)
       (mapcat (fn [[y line]]
                 (->> line
                      (map-indexed (fn [x c]
                                     (if (#{\L \#} c)
                                       [[x y] (= \# c)])))
                      (remove nil?))))
       (into {})))

(defn make-seat-views
  [layout x y]
  (let [width         (reduce max (map first (keys layout)))
        height        (reduce max (map second (keys layout)))
        max-dimension (max width height)]
    (keep (fn [[dx dy]]
            (->> (range max-dimension)
                 next
                 (some (fn [n]
                         (let [cx [(+ x (* n dx))
                                   (+ y (* n dy))]]

                           (when (contains? layout cx)
                             cx))))))
          directions)))

(defn make-views
  [layout]
  (->> layout
       (map (fn [[[x y] _]]
              [[x y] (make-seat-views layout x y)]))
       (into {})))

(defn count-neighbors
  [layout cx views]
  (->> (views cx)
       (filter layout)
       (count)))

(defn next-layout
  [layout views]
  (->> layout
       (mapv (fn [[cx occupied]]
               (let [c (count-neighbors layout cx views)]
                 (cond
                   (and occupied (>= c 5))
                   [cx false]

                   (and (not occupied) (zero? c))
                   [cx true]

                   :else
                   [cx occupied])
                 )))
       (into {})))

(defn count-occupied-seats
  [layout]
  (->> layout
       (filter val)
       count))

(defn problem2
  [layout]
  (let [views (make-views layout)]
    (loop [layout      layout
           prev-layout nil]
      (if (not= layout prev-layout)
        (recur (next-layout layout views)
               layout)
        (println
          (count-occupied-seats layout))))))

(defn -main
  [& _]
  (let [layout (read-layout "../day11/input.txt")]
    (problem2 layout)))
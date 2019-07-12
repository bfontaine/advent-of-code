(ns aoc2018.p07
  (:require [clojure.string :as str]))

(defn read-file
  [filename]
  (->> (slurp filename)
       str/split-lines))

(defn build-graph
  [lines]
  (reduce (fn [m line]
            (let [[_ a b] (re-matches #"Step ([A-Z]).+([A-Z]).+" line)]
              (-> m
                  (update a identity)
                  (update b #(conj % a)))))
          {}
          lines))

(defn solution1-lines
  [lines]
  (loop [steps []
         graph (build-graph lines)]
    (if (empty? graph)
      (str/join "" steps)
      (let [next-step (->> graph
                           (keep (fn [[k v]]
                                   (when (empty? v)
                                     k)))
                           sort
                           first)

            graph (->> (dissoc graph next-step)
                       (reduce-kv (fn [g a xs]
                                    (assoc g a (remove #{next-step} xs)))
                                  {}))]

        (recur (conj steps next-step) graph)

        ))))

(defn solution1
  [filename]
  (->> (read-file filename)
       solution1-lines))

(defn solution2
  [filename]
  )

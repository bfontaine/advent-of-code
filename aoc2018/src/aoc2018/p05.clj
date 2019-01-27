(ns aoc2018.p05
  (:require [clojure.string :as str]))

(defn- scan-polymer-stack
  [text]
  (reduce (fn [stack c]
            (let [p (first stack)]
              (if (and (some? p)
                       (#{-32 32} (- (int p) (int c))))
                (rest stack)
                (cons c stack))))
          nil
          text))

(defn scan-polymer
  [text]
  (->> text
       scan-polymer-stack
       reverse
       (apply str)))

(defn solution1
  [filename]
  (count (scan-polymer (str/trim (slurp filename)))))


(defn shortest-polymer-length
  [polymer]
  (reduce (fn [best unit]
            (let [polymer (remove (fn [c]
                                    (or (= (int c) unit)
                                        (= (int c) (+ 32 unit))))
                                  polymer)]
              (min best (count (scan-polymer-stack polymer)))))
          (count polymer)
          (range (int \A) (inc (int \Z)))))

(defn solution2
  [filename]
  (let [polymer (str/trim (slurp filename))]
    (shortest-polymer-length polymer)))

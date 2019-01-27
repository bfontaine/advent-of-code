(ns aoc2018.p05
  (:require [clojure.string :as str]))

(defn scan-polymer
  [text]
  (->> text
       (reduce (fn [stack c]
                 (let [p (first stack)]
                   (if (and (some? p)
                            (#{-32 32} (- (int p) (int c))))
                     (rest stack)
                     (cons c stack))))
          nil)
       reverse
       (apply str)))

(defn solution1
  [filename]
  (count (scan-polymer (str/trim (slurp filename)))))

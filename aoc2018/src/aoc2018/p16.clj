(ns aoc2018.p16
  (:require [clojure.string :as str]
            [clojure.edn :as edn]))

(defn- parse-register-text
  [text]
  (edn/read-string (last (str/split text #":"))))

(defn- parse-op
  [text]
  (map #(Long/parseLong %) (str/split text #" ")))

(defn parse-problem
  [text]
  (let [[before op after] (str/split-lines text)]
    [(parse-register-text before)
     (parse-op op)
     (parse-register-text after)]))

(defn parse-input
  [text]
  (let [problems-text (first (str/split text #"\n\n\n"))]
    (map parse-problem (str/split problems-text #"\n\n"))))

(defn parse-file
  [filename]
  (parse-input (slurp filename)))

(defn apply-register-op
  [f [a b c] registers]
  (let [result (f (nth registers a) (nth registers b))]
    (assoc registers c result)))

(defn apply-value-op
  [f [a b c] registers]
  (let [result (f (nth registers a) b)]
    (assoc registers c result)))

(defn apply-rr-pred-op
  [pred args registers]
  (apply-register-op
    (fn [a b] (if (pred a b) 1 0)) args registers))

(defn apply-ir-pred-op
  [pred [a b c] registers]
  (let [result (if (pred a (nth registers b)) 1 0)]
    (assoc registers c result)))

(defn apply-ri-pred-op
  [pred args registers]
  (apply-value-op
    (fn [a b] (if (pred a b) 1 0)) args registers))

(def addr (partial apply-register-op +))
(def mulr (partial apply-register-op *))
(def borr (partial apply-register-op bit-or))
(def banr (partial apply-register-op bit-and))

(def setr (partial apply-register-op (fn [a _] a)))
(def seti (fn [[a _ c] registers]
            (assoc registers c a)))

(def gtrr (partial apply-rr-pred-op >))
(def gtir (partial apply-ir-pred-op >))
(def gtri (partial apply-ri-pred-op >))

(def eqrr (partial apply-rr-pred-op =))
(def eqir (partial apply-ir-pred-op =))
(def eqri (partial apply-ri-pred-op =))

(def addi (partial apply-value-op +))
(def muli (partial apply-value-op *))
(def bori (partial apply-value-op bit-or))
(def bani (partial apply-value-op bit-and))

(def ops
  [#'addr
   #'mulr
   #'borr
   #'setr
   #'seti
   #'banr
   #'addi
   #'muli
   #'bori
   #'bani
   #'gtrr
   #'gtir
   #'gtri
   #'eqrr
   #'eqir
   #'eqri])

(defn solve-problem
  [[before [_ a b c] after]]
  (reduce (fn [acc op]
              (if (= (op [a b c] before) after)
                (inc acc)
                acc))
            0
            ops))

(defn solve-problems
  [problems]
  (->> problems
       (filter (fn [problem]
                 (>= (solve-problem problem) 3)))
       count))

(defn solve-input
  [text]
  (solve-problems (parse-input text)))

(defn solve-file
  [filename]
  (solve-input (slurp filename)))

(def solution1 solve-file)

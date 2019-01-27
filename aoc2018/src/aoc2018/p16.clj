(ns aoc2018.p16
  (:require [clojure.string :as str]
            [clojure.set :as set]
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

(defn split-input
  [text]
  (str/split text #"\n\n\n\n"))

(defn parse-problems-input
  [problems-text]
  (map parse-problem (str/split problems-text #"\n\n")))

(defn- mk-op
  [f get-a get-b]
  (fn [[a b c] registers]
    (let [result (f
                  (if (= :r get-a) (nth registers a) a)
                  (if (= :r get-b) (nth registers b) b))]
      (assoc registers c result))))

(defn rr-op [f] (mk-op f :r :r))
(defn ri-op [f] (mk-op f :r :i))
(defn ir-op [f] (mk-op f :i :r))

(defn pred
  [f]
  (fn [a b]
    (if (f a b) 1 0)))

(def addr (rr-op +))
(def mulr (rr-op *))
(def borr (rr-op bit-or))
(def banr (rr-op bit-and))

(def setr (rr-op (fn [a _] a)))
(def seti (ir-op (fn [a _] a)))

(def gtrr (rr-op (pred >)))
(def gtir (ir-op (pred >)))
(def gtri (ri-op (pred >)))

(def eqrr (rr-op (pred =)))
(def eqir (ir-op (pred =)))
(def eqri (ri-op (pred =)))

(def addi (ri-op +))
(def muli (ri-op *))
(def bori (ri-op bit-or))
(def bani (ri-op bit-and))

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

(defn problem-ops
  [[before [_ a b c] after]]
  (filter (fn [op]
            (= (op [a b c] before) after))
          ops))

(defn solve-problems
  [problems]
  (->> problems
       (filter (fn [problem]
                 (>= (count (problem-ops problem)) 3)))
       count))

(defn solution1
  [filename]
  (-> filename slurp split-input first parse-problems-input solve-problems))


(defn guess-ops
  [problems]
  (let [guesses (reduce (fn [guesses problem]
                          (let [[_ [code _ _ _] _] problem
                                ops (into #{} (problem-ops problem))]
                            (update guesses code #(if %
                                                    (set/intersection % ops)
                                                    ops))))
                        {}
                        problems)]

    ;; Note this loops forever if there's no solution
    (loop [found {}
           found-ops #{}
           guesses guesses]
      (if (empty? guesses)
        found
        (let [findings (filter (fn [[_ ops]] (= 1 (count ops))) guesses)
              found (into found (map (fn [[k v]] [k (first v)]) findings))
              found-ops (reduce set/union found-ops (map second findings))
              guesses (reduce-kv (fn [acc n ops]
                                   (if (found n)
                                     acc
                                     (assoc acc n (set/difference
                                                    ops
                                                    found-ops))))
                                 {}
                                 guesses)]
          (recur
            found
            found-ops
            guesses))))))

(defn solution2
  [filename]
  (let [[problems-input ops-input] (-> filename slurp split-input)
        problems (parse-problems-input problems-input)
        ops (->> ops-input str/split-lines (map parse-op))

        fns (guess-ops problems)]

    (first
      (reduce (fn [registers [op & args]]
                ((fns op) args registers))
              [0 0 0 0]
              ops))))

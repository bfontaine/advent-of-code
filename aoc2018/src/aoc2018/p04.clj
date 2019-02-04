(ns aoc2018.p04
  (:require [clojure.string :as str]))

(defn parse-line
  [line]
  (let [[_ date hours minutes action]
        (re-matches #"\[(\d+-\d+-\d+) (\d{2}):(\d{2})\] (.+)" line)

        hours (Long/parseLong hours)
        minutes (Long/parseLong minutes)

        base {:date date :hours hours :minutes minutes}]
    (condp re-matches action
      #"Guard #(\d+) begins shift"
        :>> (fn [[_ guard]]
              (assoc base
                     :action :shift-start
                     :guard guard))

      #"falls asleep"
        (assoc base :action :sleep-start)

      #"wakes up"
        (assoc base :action :sleep-end))))

(defn build-shifts
  [events]
  (->> events
       (sort-by (juxt :date :hours :minutes))
       (reduce (fn [[m last-guard] {:keys [action guard date hours minutes] :as x}]
                 (let [guard (or guard last-guard)
                       m (case action
                           :shift-start
                           (cond-> m
                             ;; New shift starting today. Otherwise, don't do
                             ;; anything and keep the guard for the next day.
                             (zero? hours)
                             (assoc-in [date :guard] guard))

                           :sleep-start
                           (-> m
                               (update-in [date :guard] #(or % guard))
                               (update-in [date :sleeps] (partial cons minutes)))

                           :sleep-end
                           (update-in m [date :sleeps] (partial cons minutes)))]
                   [m guard]))
               [{} nil])
       first))

(defn shifts-by-guard
  [shifts-by-day]
  (->> shifts-by-day
       vals
       (group-by :guard)
       (reduce-kv (fn [m guard day-infos]
                    ;; sort for predictable inputs
                    (assoc m guard (sort-by first (map :sleeps day-infos))))
                  {})))

(defn- fill-minutes-map*
  [m start end]
  (reduce (fn [m minute]
            (update m minute #(inc (or % 0))))
          m
          (range start end)))

(defn fill-minutes-map
  [m sleeps]
  {:pre [(even? (count sleeps))]}
  (->> sleeps
       (partition 2)
       (reduce (fn [minutes-map [end start]]
                 (fill-minutes-map* minutes-map start end))
               m)))

(defn guard-shifts->minutes-map
  [guard-shifts]
  (reduce fill-minutes-map {} guard-shifts))

(defn guards-shifts->guards-minutes-maps
  [shifts-by-guard]
  (reduce-kv (fn [m guard shifts]
               (assoc m guard (guard-shifts->minutes-map shifts)))
             {}
             shifts-by-guard))

(defn lines->guards-minutes-maps
  [lines]
  (->> lines
       build-shifts                       ; shifts
       shifts-by-guard                    ; shifts by guard
       guards-shifts->guards-minutes-maps ; minute maps by guard
       ))

(defn solution1-lines
  [lines]
  (let [minutes-maps (lines->guards-minutes-maps lines)
        [best-guard best-minutes-map] (apply max-key
                                             (fn [[g minutes-map]]
                                               (reduce + (vals minutes-map)))
                                             minutes-maps)
        best-guard-n (Long/parseLong best-guard)
        best-minute (->> best-minutes-map
                         (sort-by val >)
                         first
                         key)]

    (* best-guard-n
       best-minute)))

(defn file-lines
  [filename]
  (->> (slurp filename)
       str/split-lines
       (map parse-line)))                 ; lines

(defn solution1
  [filename]
  (->> filename
       file-lines
       solution1-lines))

(defn solution2-lines
  [lines]
  (let [[best-guard best-minute _]
        (->> lines
             lines->guards-minutes-maps
             (reduce-kv (fn [acc guard minutes-map]
                          (reduce-kv (fn [[best-guard
                                           best-minute
                                           best-n] minute n]

                                       (if (or (nil? best-n) (> n best-n))
                                         [guard minute n]
                                         [best-guard best-minute best-n]))
                                     acc
                                     minutes-map))
                        nil))

        best-guard-n (Long/parseLong best-guard)]
    (* best-guard-n
       best-minute)))

(defn solution2
  [filename]
  (->> filename
       file-lines
       solution2-lines))

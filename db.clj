(require '[clojure.data.priority-map :as pm])

(loop [transactions [(pm/priority-map)]]
  (print ">> ")
  (flush)
  (let [[command & args] (clojure.string/split (read-line) #" ")
        db (peek transactions)]
    (case command
      "END" (println)
      "SET" (recur (conj (pop transactions) (assoc db (first args) (second args))))
      "GET" (do
              (println (or (db (first args)) "NULL"))
              (recur transactions))
      "DELETE" (recur (conj (pop transactions) (dissoc db (first args))))
      "COUNT" (do
                (println (count ((pm/priority->set-of-items db) (first args))))
                (recur transactions))
      "BEGIN" (recur (conj transactions db))
      "ROLLBACK" (recur (if (> (count transactions) 1)
                          (pop transactions)
                          transactions))
      "COMMIT" (recur [db])
      "REPORT" (do
                 (println transactions)
                 (recur transactions))
      (do
        (println "Unknown command")
        (recur transactions)))))

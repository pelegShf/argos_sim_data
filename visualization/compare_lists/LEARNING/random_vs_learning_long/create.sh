./scripts/db/search_db.sh --for-graph selectMethod "time: 30" "experiment_length: 1500"   "robotCount: 40" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning_long/40.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 30" "experiment_length: 1500"   "robotCount: 45" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning_long/45.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 30" "experiment_length: 1500"   "robotCount: 50" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning_long/50.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 30" "experiment_length: 1500"   "robotCount: 55" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning_long/55.txt

# Run from ./argos_sim_data
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning_long/40
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning_long/45
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning_long/50
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning_long/55

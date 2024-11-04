# Run from ./nymbot_simulator
./scripts/db/search_db.sh --for-graph selectMethod "time: 29" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 25" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning/25.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 29" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "robotCount: 30" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning/30.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 29" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL"  "robotCount: 35" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning/35.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 29" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 40" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning/40.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 29" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 45" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning/45.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 29" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 50" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning/50.txt
./scripts/db/search_db.sh --for-graph selectMethod "time: 29" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 55" > ../argos_sim_data/visualization/compare_lists/LEARNING/random_vs_learning/55.txt

# Run from ./argos_sim_data
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning/25
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning/30
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning/35
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning/40
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning/45
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning/50
python3 ./visualization/compare_simple.py -i ./LEARNING/random_vs_learning/55

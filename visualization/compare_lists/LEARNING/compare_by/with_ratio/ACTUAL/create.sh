# Run from ./nymbot_simulator
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 25" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/25.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "robotCount: 30" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/30.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUA L"  "robotCount: 35" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/35.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 40" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/40.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 45" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/45.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 50" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/50.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "robotCount: 55" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/55.txt

./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "differenceReward: NO_APPROXIMATION" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/NO_APPROXIMATION.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "differenceReward: AVG_NONE_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/AVG_NONE_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "differenceReward: AVG_BEST_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/AVG_BEST_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL "  "differenceReward: AVG_WORST_WORST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/with_ratio/ACTUAL/AVG_WORST_WORST.txt

# Run from ./argos_sim_data
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/25
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/30
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/35
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/40
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/45
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/50
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/55


python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/NO_APPROXIMATION
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/AVG_NONE_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/AVG_BEST_BEST
# python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/AVG_NONE_WORST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/with_ratio/ACTUAL/AVG_WORST_WORST
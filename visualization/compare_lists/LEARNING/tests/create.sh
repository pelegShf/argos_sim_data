./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 25" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/25.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "robotCount: 30" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/30.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 35" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/35.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 40" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/40.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 45" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/45.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 50" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/50.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 55" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/55.txt

./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: NO_APPROXIMATION" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/NO_APPROXIMATION.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "differenceReward: AVG_NONE_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/AVG_NONE_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_BEST_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/AVG_BEST_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_NONE_WORST" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/AVG_NONE_WORST.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_WORST_WORST" > ../argos_sim_data/visualization/compare_lists/LEARNING/tests/AVG_WORST_WORST.txt


python3 ./visualization/compare_simple.py -i ./LEARNING/tests/25
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/30
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/35
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/40
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/45
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/50
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/55


python3 ./visualization/compare_simple.py -i ./LEARNING/tests/NO_APPROXIMATION
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/AVG_NONE_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/AVG_BEST_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/AVG_NONE_WORST
python3 ./visualization/compare_simple.py -i ./LEARNING/tests/AVG_WORST_WORST
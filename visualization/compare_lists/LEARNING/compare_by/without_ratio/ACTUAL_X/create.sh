# Run from ./nymbot_simulator
./scripts/db/search_db.sh --for-graph differenceReward "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "robotCount: 25" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/25.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X" "robotCount: 30" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/30.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "robotCount: 35" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/35.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "robotCount: 40" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/40.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "robotCount: 45" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/45.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "robotCount: 50" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/50.txt
./scripts/db/search_db.sh --for-graph differenceReward "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "robotCount: 55" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/55.txt

./scripts/db/search_db.sh --for-graph robotCount "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "differenceReward: NO_APPROXIMATION" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/NO_APPROXIMATION.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X" "differenceReward: AVG_NONE_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/AVG_NONE_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_BEST_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/AVG_BEST_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "time: 28" "experiment_length: 600" "collision_avoidance: 0" "use_update_ratio: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_WORST_WORST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/without_ratio/ACTUAL_X/AVG_WORST_WORST.txt

# Run from ./argos_sim_data
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/25
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/30
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/35
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/40
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/45
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/50
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/55


python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/NO_APPROXIMATION
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/AVG_NONE_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/AVG_BEST_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/without_ratio/ACTUAL_X/AVG_WORST_WORST
# Run from ./nymbot_simulator
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 0" "differenceReward: NO_APPROXIMATION" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/NO_APPROXIMATION.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 1" "differenceReward: NO_APPROXIMATION" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/NO_APPROXIMATION.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 0" "differenceReward: NO_APPROXIMATION" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/NO_APPROXIMATION.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 1" "differenceReward: NO_APPROXIMATION" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/NO_APPROXIMATION.txt


./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 0" "differenceReward: AVG_NONE_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_NONE_BEST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 1" "differenceReward: AVG_NONE_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_NONE_BEST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 0" "differenceReward: AVG_NONE_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_NONE_BEST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 1" "differenceReward: AVG_NONE_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_NONE_BEST.txt


./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 0" "differenceReward: AVG_BEST_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_BEST_BEST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 1" "differenceReward: AVG_BEST_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_BEST_BEST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 0" "differenceReward: AVG_BEST_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_BEST_BEST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 1" "differenceReward: AVG_BEST_BEST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_BEST_BEST.txt

./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 0" "differenceReward: AVG_WORST_WORST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_WORST_WORST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 27" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL " "use_update_ratio: 1" "differenceReward: AVG_WORST_WORST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_WORST_WORST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 0" "differenceReward: AVG_WORST_WORST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_WORST_WORST.txt
./scripts/db/search_db.sh --for-graph distanceType "time: 28" "experiment_length: 600" "collision_avoidance: 0" "distanceType: ACTUAL_X" "use_update_ratio: 1" "differenceReward: AVG_WORST_WORST" "robotCount: 55" >> ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/methods/55/AVG_WORST_WORST.txt


python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/methods/55/NO_APPROXIMATION
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/methods/55/AVG_NONE_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/methods/55/AVG_BEST_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/methods/55/AVG_WORST_WORST
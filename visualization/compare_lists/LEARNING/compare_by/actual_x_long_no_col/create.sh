# ./scripts/db/search_db.sh --for-graph differenceReward "experiment_length: 1200" "collision_avoidance: 1" "distanceType: ACTUAL_X"  "robotCount: 25" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/25.txt
# ./scripts/db/search_db.sh --for-graph differenceReward "experiment_length: 1200" "collision_avoidance: 1" "distanceType: ACTUAL_X" "robotCount: 30" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/30.txt
# ./scripts/db/search_db.sh --for-graph differenceReward "experiment_length: 1200" "collision_avoidance: 1" "distanceType: ACTUAL_X"  "robotCount: 35" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/35.txt
./scripts/db/search_db.sh --for-graph differenceReward "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 40" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/40.txt
./scripts/db/search_db.sh --for-graph differenceReward "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 45" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/45.txt
./scripts/db/search_db.sh --for-graph differenceReward "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 50" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/50.txt
./scripts/db/search_db.sh --for-graph differenceReward "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "robotCount: 55" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/55.txt

./scripts/db/search_db.sh --for-graph robotCount "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: NO_APPROXIMATION" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/NO_APPROXIMATION.txt
./scripts/db/search_db.sh --for-graph robotCount "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X" "differenceReward: AVG_NONE_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/AVG_NONE_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_BEST_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/AVG_BEST_BEST.txt
./scripts/db/search_db.sh --for-graph robotCount "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_NONE_WORST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/AVG_NONE_WORST.txt
./scripts/db/search_db.sh --for-graph robotCount "experiment_length: 1200" "collision_avoidance: 0" "distanceType: ACTUAL_X"  "differenceReward: AVG_WORST_WORST" > ../argos_sim_data/visualization/compare_lists/LEARNING/compare_by/actual_x_long_no_col/AVG_WORST_WORST.txt


# python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/25
# python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/30
# python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/35
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/40
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/45
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/50
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/55


python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/NO_APPROXIMATION
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/AVG_NONE_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/AVG_BEST_BEST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/AVG_NONE_WORST
python3 ./visualization/compare_simple.py -i ./LEARNING/compare_by/actual_x_long_no_col/AVG_WORST_WORST
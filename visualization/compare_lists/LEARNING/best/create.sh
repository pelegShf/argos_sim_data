# Run from ./nymbot_simulator
./scripts/db/search_db.sh --for-graph robotCount "time: 28" "experiment_length: 1500" "collision_avoidance: 0" "distanceType: ACTUAL "  "differenceReward: AVG_BEST_BEST" > ../argos_sim_data/visualization/compare_lists/LEARNING/best/AVG_BEST_BEST.txt


python3 ./visualization/compare_simple.py -i ./LEARNING/best/AVG_BEST_BEST

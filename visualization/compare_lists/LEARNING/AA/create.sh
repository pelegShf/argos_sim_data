# Run from ./nymbot_simulator
./scripts/db/search_db.sh --for-graph robotCount "time: 28" "experiment_length: 600" "model_type: avoidAttract"  > ../argos_sim_data/visualization/compare_lists/LEARNING/AA/avoidAttract.txt


python3 ./visualization/compare_simple.py -i ./LEARNING/AA/avoidAttract

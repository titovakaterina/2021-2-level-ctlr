set -ex

TARGET_SCORE=$(bash config/get_pipeline_target_score.sh)

if [[ ${TARGET_SCORE} == 10 ]]; then
  python pos_frequency_pipeline.py
fi

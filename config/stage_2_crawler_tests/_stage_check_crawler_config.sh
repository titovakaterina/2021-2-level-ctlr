set -ex

echo -e '\n'
echo 'Running crawler config check...'

TARGET_SCORE=$(bash config/get_scrapper_target_score.sh)
echo $TARGET_SCORE

if [[ ${TARGET_SCORE} != 0 ]]; then
  python -m pytest -m "mark10 and stage_2_1_crawler_config_check"
else
  echo "Skipping stage"
fi

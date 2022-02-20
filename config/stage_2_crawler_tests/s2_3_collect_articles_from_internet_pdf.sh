set -ex

echo "Stage: Downloading articles"

echo "Adding $(pwd) to PYTHONPATH"
export PYTHONPATH=$(pwd):$PYTHONPATH

python config/change_pdf_config_launcher.py

echo "Changed config params"

python config/html_with_pdf_parser_launcher.py

echo "Collected dataset"

echo "Checking volume of files"

TARGET_SCORE=$(bash config/get_scrapper_target_score.sh)

if [[ ${TARGET_SCORE} == 4 ]]; then
  echo "Running score four checks"
  python -m pytest -m "mark4 and stage_2_3_dataset_volume_check"
else
  python -m pytest -m "mark10 and stage_2_3_dataset_volume_check"
fi

echo "Volume is correct"

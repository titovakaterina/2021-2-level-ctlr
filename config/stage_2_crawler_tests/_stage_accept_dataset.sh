set -ex

echo -e '\n'
echo "Accepting dataset"

TARGET_SCORE=$(bash config/get_scrapper_target_score.sh)

if [[ ${TARGET_SCORE} != 0 ]]; then
  echo "Crawler is working. Proceed to text processing pipeline."
else
  echo "Skipping stage"
fi

# make the script verbose
set -ex

export TARGET_SCORE=$(head -5 config/target_score.txt | tail -1)
if [[ -z "$TARGET_SCORE" ]]; then
  echo "TARGET_SCORE for pipeline cannot be empty "
  exit 1
fi

echo ${TARGET_SCORE}

set -ex

echo -e '\n'
echo 'Running lint check...'

TARGET_SCORE=$(bash config/get_scrapper_target_score.sh)

#TODO: rework scoring function to actually get score before passing to python script
TARGET_SCORE=$(cat config/target_score.txt)
echo $TARGET_SCORE

lint_output=$(python -m pylint *.py core_utils \
              --rcfile config/stage_1_style_tests/.pylintrc)

python3 config/stage_1_style_tests/lint_level.py \
          --lint-output "$lint_output" \
          --target-score "$TARGET_SCORE"

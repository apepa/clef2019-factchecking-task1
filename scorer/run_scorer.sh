#!/usr/bin/env bash
PROJ_DIR="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"
export PYTHONPATH=${PROJ_DIR}
scorer_tests_path=${PROJ_DIR}'/data/scorer_tests/'
gold_file_task1=${PROJ_DIR}/data/gold/'Task1-English-1st-Presidential.txt'
gold_file_task2=${PROJ_DIR}/data/gold/'Task2-English-1st-Presidential.txt'

echo 'Scoring a random baseline for subtask A'
python3 subtaskA.py --gold_file_path=${gold_file_task1} --pred_file_path=${scorer_tests_path}'subtaskA_random_baseline.txt'
echo '**********'
echo 'Scoring the gold predictions for subtask A'
python3 subtaskA.py --gold_file_path=${gold_file_task1} --pred_file_path=${scorer_tests_path}'subtaskA_gold.txt'
echo '**********'
echo 'Scoring subtask A, where the provided list of line_numbers contains a line_number, which is not in the gold file.'
python3 subtaskA.py --gold_file_path=${gold_file_task1} --pred_file_path=${scorer_tests_path}'subtaskA_other_line_number.txt'
echo '**********'
echo '**********'
echo 'Scoring the gold predictions for subtask B'
python3 subtaskB.py --gold_file_path=${gold_file_task2} --pred_file=${scorer_tests_path}'subtaskB_gold.txt'
echo '**********'
echo 'Scoring a random baseline for subtask B'
python3 subtaskB.py --gold_file_path=${gold_file_task2} --pred_file=${scorer_tests_path}'subtaskB_random_baseline.txt'
echo '**********'
echo 'Scoring a file with predicted labels, which contains a claim_number, which is not present in the gold file.'
python3 subtaskB.py --gold_file_path=${gold_file_task2} --pred_file=${scorer_tests_path}'/subtaskB_other_claim_number.txt'
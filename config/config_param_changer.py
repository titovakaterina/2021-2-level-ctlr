"""
Changes num_article param with random number in range(2, 7)
"""

import argparse
import json
import random


def parser():
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('--config_path',
                        type=str,
                        required=True,
                        help='Full path to the scrapper config file')
    return parser


def change_volume(config: str):
    with open(config) as f:
        reference = json.load(f)

    num_articles = random.randint(2, 7)
    reference["total_articles_to_find_and_parse"] = num_articles

    with open(config, "w", encoding="utf-8") as f:
        json.dump(reference, f)


if __name__ == "__main__":
    args = parser().parse_args()
    change_volume(args.config_path)

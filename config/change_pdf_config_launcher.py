"""
Changes num_article param with random number in range(2, 7)
"""

import json
import random
from config_param_changer import change_volume
from test_params import PDF_ARTICLE_CONFIG


if __name__ == "__main__":
    change_volume(PDF_ARTICLE_CONFIG)

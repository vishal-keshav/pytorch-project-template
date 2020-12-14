#!/usr/bin/env python
"""Runs the train function in the trainer by assembling the model, dataset
logger and configuration. Supports running grid search on a the list of
configurations.
"""

import argparse
import importlib

from utils.generic_utils import get_configurations
from utils.logger_utils import get_logger

def argument_parser():
    parser = argparse.ArgumentParser(description="sample")
    parser.add_argument('--config', default='default', type=str,
                        help='configuration file name')
    parser.add_argument('--trainer', default='default', type=str,
                        help='trainer file name')
    parser.add_argument('--dataset', default='default', type=str,
                        help='dataset file name')
    parser.add_argument('--model', default='default', type=str,
                        help='model file name')
    parser.add_argument('--logger', default=None, type=str,
                        choices=[None, 'print', 'comet'],
                        help='logger choices')
    parser.add_argument('--key', default='', type=str,
                        help='used if logger is set to comet')
    parser.add_argument()
    args = parser.parse_args()
    return args

def main():
    args = argument_parser()
    config_module = importlib.import_module("configs."+args.config)
    model_def = importlib.import_module("model."+args.model).model
    dataset = importlib.import_module("dataset."+args.dataset).dataset
    train = importlib.import_module("trainer."+args.trainer).train
    logger = get_logger(args.logger)

    tried_configs = []
    end = False
    while True:
        importlib.reload(config_module)
        configs = config_module.config
        possible_configs = get_configurations(configs)
        for config_idx, config in enumerate(possible_configs):
            if config_idx == len(possible_configs)-1:
                end = True
            if config in tried_configs:
                continue
            else:
                tried_configs.append(config)
                train(**{'c':config, 'm':model_def, 'd':dataset, 'e':logger})
                break
        if end:
            break

if __name__ == "__main__":
    main()
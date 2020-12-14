import uuid
from comet_ml import Experiment

class logger:
    """logger interface class
    All loggers implements the method of this class
    """
    def __init__(self, **kwargs):
        self.exp_name = kwargs.get('exp_name', uuid.uuid1())

    def log(self, tag, value, **kwargs):
        """Log value with a given tag

        Args:
            tag (str): Tag associated to the value.
            value (any): Value to be logged.
        """
        raise NotImplementedError

class print_logger(logger):
    """A simple print based logger.
    Instead of using prints, use log.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def log(self, tag, value, *kwargs):
        print(tag + ": " + str(value))

class comet_logger(logger):
    """Comel.ml logger.
    Use this logger if experiments are extensively complicated.
    """
    def __init__(self, **kwargs):
        self.exp = Experiment(**kwargs)
        super().__init__(**kwargs)
    
    def log(self, tag, value, **kwargs):
        self.exp.log_metric(tag, value, **kwargs)

def get_logger(args):
    if args.logger is None: return None
    if args.logger == 'print':
        return print_logger()
    if args.logger == 'comet':
        return comet_logger(api_key=args.api_key)
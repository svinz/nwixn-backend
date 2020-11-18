import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime

def init_logging(name):
    # soure for global logger: https://stackoverflow.com/questions/7621897/python-logging-module-globally
    # add a streamhandler to show logs in terminal
    ch = logging.StreamHandler(sys.stdout)
    # format the logs
    #f = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    f = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(module)s %(message)s')
    # setting the format
    ch.setFormatter(f)
    # create a logger
    LOG = logging.getLogger(name)
    LOG.setLevel(logging.DEBUG)
    LOG.addHandler(ch)
    return LOG

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


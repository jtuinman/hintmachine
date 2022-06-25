from collections import OrderedDict
import logging
import datetime
import time


class SoundLoggingHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.last_entries = OrderedDict()

    def emit(self, record):
        msg = self.format(record)
        if len(self.last_entries) > 30:
            self.last_entries.popitem(last=False)
        self.last_entries[datetime.datetime.now()] = msg

    def get_last_entries(self):
        nowsecs = time.time()
        returns = []
        for dateentry in self.last_entries:
            thensecs = time.mktime(dateentry.timetuple())
            diff = thensecs - nowsecs
            diffstring = str(int(diff)) + " secs"
            returns.insert(0, diffstring.ljust(9) + " " + self.last_entries[dateentry])
        return returns





import time
import sys

while True:
    from datetime import datetime

    now = datetime.now()
    print("%s/%s/%s %s:%s:%s" % (now.month, now.day, now.year, now.hour, now.minute, now.second)),
    sys.stdout.flush()
    print("\r"),
    time.sleep(1)

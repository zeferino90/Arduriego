__author__ = 'zeferino'

from datetime import datetime, timedelta
import setupkeeper


conf = setupkeeper()

while 1:
    actualdate = datetime.today()
    conf.updateConf()
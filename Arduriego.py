__author__ = 'zeferino'

from datetime import datetime, timedelta
import setupkeeper


conf = setupkeeper()
rain_check = False #signal to check rain in that day
watering_action = False #signal to perform watering action
watering_postpone = False #signal that means we have to water some plants but the last time we try to do it, we can't for some reasons

while 1:
    actualdate = datetime.today()
    conf.getConf()
    if rainf_check:
        #get rain and update lastwatered time on plants if they need

    elif watering_action:
        #perform watering actions
    elif watering_postpone:
        #some plants have deferred watering actions


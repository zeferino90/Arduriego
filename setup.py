from datetime import timedelta
from datetime import datetime
from datetime import time
import pickle
from plant import plant
from gps import gps

__author__ = 'zeferino'


print "Welcome to the setup program for RaspyRiego, the premier plant-watering application!\n"
print "Your options are:\n"
print "'cycles' or 'c', to receive a summary of, and modify, the available watering cycles currently under this system"
print "'potsize' or 'p', to check and modify the planter sizes\n"
print "'season' or 's', to check and modify seasonal options\n"
print "'thresh' or 't', to check and modify the current rain thresholds depends on size of plants\n"
print "'plants' or 'pl, to check and modify the plants that you have'\n"
print "'gps' or 'g', to update the GPS coordinates"

print "'exit', to get a free* candy bar! (no refunds)\n"
#PREPARATION, initial load and dictionary generation#

fileObject = open("setupconf", "r")

cycles = pickle.load(fileObject)
sizes = pickle.load(fileObject)
seasons = pickle.load(fileObject)
thresholds = pickle.load(fileObject)
plants = pickle.load(fileObject)
coordinates = pickle.load(fileObject)

#EDITING, access to data
command = input("Please input your choice: ")
if command == "cycles" or command == 'c':
    #toca llegir de arxiu
    print ("There are currently 3 watering cycles:")
    print ("1: Short: " + cycles["shortcycle"] + "\n") #toca afegir el que hem llegit del disc
    print ("2: Medium: " + cycles["mediumcycle"] + "\n")
    print ("3: Long: " + cycles["longcycle"] + "\n")
    cycleid = input("Input the number of the cycle you wish to change (0 for none): ")
    if cycleid != 0:
        newvalue = input("Input its new value: ")
        if cycleid == 1:
            cycles["shortcycle"] = timedelta(newvalue)
        elif cycleid == 2:
            cycles["mediumcycle"] = timedelta(newvalue)
        elif cycleid == 3:
            cycles["longcycle"] = timedelta(newvalue)
        else:
            print ("Incorrect Value\n")#check for it?

    print ("Check your watering privilege, gardenlord\n")

elif command == "potsize" or command == 'p':
    print "All available pot sizes are as follows:\n"
    print ("1: Small: " + sizes["small"] + "\n")
    print ("2: Medium: " + sizes["medium"] + "\n")
    print ("3: Large: " + sizes["large"] + "\n")
    potsizeid = input("Input the number of the size you wish to change (0 for none): ")
    if potsizeid != 0:
        newvalue = input("Input its new value: ")
        if potsizeid == 1:
            sizes["small"] = newvalue
            print ("The value has been successfully changed\n")
        elif potsizeid == 2:
            sizes["medium"] = newvalue
            print ("The value has been successfully changed\n")
        elif potsizeid == 3:
            sizes["large"] = newvalue
            print ("The value has been successfully changed\n")
        else:
            print ("Incorrect Value\n")#check for it?

    print ("The only true pot size is 420\n")

elif command == "season" or command == 's':
    print ("Current seasonal watering schedules are:\n")
    #format = 12:10 13:03 (espai al mig)
    #llegir disc
    print ("1: Summer: Plants will be watered from " + seasons["summer"][0] + " to " + seasons["summer"][1])
    print ("2: Winter: Plants will be watered from " + seasons["winter"][0] + " to " + seasons["winter"][1])
    seasonid = input("Input the number of the season you wish to change (0 for none): ")
    if seasonid != 0:
        if seasonid == 1:
            newvalue = input("Input its new starting hour. Format: HH MM ")
            seasons["summer"][0] = time(int(newvalue.split(" ")[0]),int(newvalue.split(" ")[1]))
            newvalue = input("Input its new finishing hour. Format: HH MM ")
            seasons["summer"][1] = time(int(newvalue.split(" ")[0]),int(newvalue.split(" ")[1]))
            print ("The value has been successfully changed\n")#check for it?
        if seasonid == 2:
            newvalue = input("Input its new starting hour. Format: HH MM ")
            seasons["winter"][0] = datetime.time(newvalue.split(" ")[0],newvalue.split(" ")[1])
            newvalue = input("Input its new finishing hour. Format: HH MM ")
            seasons["winter"][1] = datetime.time(newvalue.split(" ")[0],newvalue.split(" ")[1])
            print ("The value has been successfully changed\n")#check for it?

elif command == "thresh" or command == 't':
        print ("Those are the thresholds rigth now:\n")
        print ("1: Threshold for small pot size plant " + str(thresholds['smallthreshold'])+"\n")
        print ("2: Threshold for medium pot size plant " + str(thresholds['mediumthreshold'])+"\n")
        print ("3: Threshold for large pot size plant " + str(thresholds['largethreshold'])+"\n")
        thresholdid = input("Input the number of the threshold you wish to change (0 for none): ")
        if thresholdid != 0:
            newvalue = input("Input its new value: ")
            if thresholdid == 1:
                thresholds['smallthreshold'] = newvalue
                print ("The value has been successfully changed\n")
            elif thresholdid == 2:
                thresholds['mediumthreshold'] = newvalue
                print ("The value has been successfully changed\n")
            elif thresholdid == 3:
                thresholds['largethreshold'] = newvalue
                print ("The value has been successfully changed\n")
            else:
                print ("Incorrect Value\n")

elif command == "plants" or command == 'pl':
    print ("Those are the plants:\n")
    for i in range(0, 3):
        print ("%d: " % (i))
        print plants[i]
        print ("\n\n")
    plantid = input("Input the number of the plant you wish to change (0 for none)")
    if plantid != 0:
        newname = input("Input its new name ")
        plants[plantid].setName(newname)
        newcycle = input("Input its new watering cycle. Format: HH D(number of hours and number of days between watering) ")
        plants[plantid].setCycle(timedelta(days=newcycle.split(" ")[1], hours=newcycle.split(" ")[0]))
        newsize = input("Input its new pot size [small(<=1l), (1l<)medium(<=5l), large(>5l)]")
        plants[plantid].setPotSize(newsize)
        newwateringTime = input("Input its new watering Time if its postpone. Format: MM HH(number of minutes and number of hours until watering if postpone)")
        plants[plantid].setWateringTime(timedelta(hours=newcycle.split(" ")[1], minutes=newcycle.split(" ")[0]))
        newpostpone = input("Input its new postpone value. Format: 'True', 'False'")
        plants[plantid].setPostpone(bool(newpostpone))
        newlastw = input("Do you want to update the last watering time? 'Y' or 'N'")
        if newlastw == 'Y':
            plants[plantid].watered()

elif command == "gps" or command == 'g':
        confirm = input("Do you want to update the gps location? 'Y' or 'N'")
        if confirm == 'Y':
            changed = False
            now = datetime.today()
            timetochange = datetime.today() - now
            gpsmodule = gps()
            while not changed and timetochange.minute <=timedelta(minutes=5):
                print"."
                if gpsmodule.getfix():
                    coordinates = gpsmodule.getcoordinates()
                    changed = True
                    print "\nCorrectly updated\n"
            if not changed:
                print "Fail update. Try again"

else:
    print("Learn to type you neanderthal")


#BA-DUMP-A-DUMP
#Here we write the modified data back into the file
#First, we gotta delete it though! Check how

pickle.dump(cycles, fileObject)
pickle.dump(sizes, fileObject)
pickle.dump(seasons, fileObject)
pickle.dump(thresholds, fileObject)
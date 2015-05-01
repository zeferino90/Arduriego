from datetime import timedelta
from datetime import datetime
from datetime import time
import pickle

__author__ = 'zeferino'


'''Añadir plantas con todos sus campos
    añadir lat, long del gps'''

print "ola k ase\n"
print "Welcome to the setup program for ZefeRiego, the premier plant-watering application!\n"
print "Your options are:\n"
print "'cycles' or 'c', to receive a summary of, and modify, the available watering cycles currently under this system"
print "'potsize' or 'p', to check and modify the planter sizes\n"
print "'season' or 's', to check and modify seasonal options\n"
print "'thresh' or 't', to check and modify the current rain thresholds depends on size of plants"
print "'plants' or 'pl'"
print "'exit', to get a free* candy bar! (no refunds)\n"
#PREPARATION, initial load and dictionary generation#

fileObject = open("setup.txt", "wb")

cycles = pickle.load(fileObject)
sizes = pickle.load(fileObject)
seasons = pickle.load(fileObject)
thresholds = pickle.load(fileObject)
plants = pickle.load(fileObject)

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
    print ("THose are the plants:\n")
    for i in range(0, 3):
        print ("%d: " % (i))
        print plants[i]
        print ("\n\n")
    plantid = input("")

else:
    print("Learn to type you neanderthal")


#BA-DUMP-A-DUMP
#Here we write the modified data back into the file
#First, we gotta delete it though! Check how

pickle.dump(cycles, fileObject)
pickle.dump(sizes, fileObject)
pickle.dump(seasons, fileObject)
pickle.dump(thresholds, fileObject)
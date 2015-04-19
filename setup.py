__author__ = 'zeferino'

print "ola k ase\n"
print "Welcome to the setup program for ZefeRiego, the premier plant-watering application!\n"
print "Your options are:\n"
print "'check', to receive a summary of the plants currently under this system"
print "'mod', to modify any characteristic of the plants\n"
print "'season', to check and modify seasonal options\n"
print "'exit', to get a free candy bar! (no refunds)\n"

command = input("Please input your choice: ")
if command == "check":
    #toca llegir de arxiu

else if command == "mod":
    print "Which plant do you want to modify?\n"
    plantselect = input()
    #llegir de disc la planta amb id plantselect
    plantname = "cardo"
    plantschedule = "200"
    potsize = "xboxhueg"
    lastwater = "9 Sep, 1999"
    print ("--------------------------------\n")
    print ("Plant selected: " + str(plantname) + " (with id " + str(plantselect) + ")\n")
    print ("Current watering schedule: every " + str(plantschedule) + " days\n")
    print ("This plant is inside a " + str(potsize) + " pot\n")
    print ("The last time this plant was watered is " + str(lastwater) )
    print ("--------------------------------\n\n")
    print ("What do you wish to change? Choices: name, sched, size, time\n")
    #command = input()
    if command == "time":
        print("Do you ")
    print ("What is the ")

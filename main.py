# First Name: Ronnie Kaito
# Last Name: Imagawa
# Student ID: 010235636

import csv
import datetime

# Class to create a hashmap data structure
class CreateHashmap:
    # Constructor
    def __init__(self, arraySize=10):
        self.arraySize = arraySize
        self.array = [None] * arraySize

    #Hash function: (sum of ASCII value of each character) % size of the array
    def hasher(self, key):
        sum = 0
        for char in str(key):
            sum += ord(char)
        return sum % self.arraySize

    # Insert a key-value pair to the hashmap
    def addKVPair(self, key, value):
        hash = self.hasher(key)
        keyValue = [key, value]

        if self.array[hash] is None:
            self.array[hash] = list([keyValue])
        # If there is a key-value pair within the key hash, chain the pairs by appending
        else:
            self.array[hash].append(keyValue)

    # Return a value given a key
    def searchKey(self, key):
        hash = self.hasher(key)
        # Iterates over each pair if they are chained
        for KVPair in self.array[hash]:
            if key == KVPair[0]:
                return KVPair[1]
        return None

# Class to describe a package object
class Package:
    # Constructor
    def __init__(self, pkgID, pkgAddress, pkgCity, pkgState, pkgZip, pkgDeadline, pkgWeight, pkgStatus):
        self.pkgID = pkgID
        self.pkgAddress = pkgAddress
        self.pkgCity = pkgCity
        self.pkgState = pkgState
        self.pkgZip = pkgZip
        self.pkgDeadline = pkgDeadline
        self.pkgWeight = pkgWeight
        self.pkgStatus = pkgStatus
        self.timeDelivery = None
        self.timeDepart = None

    # Prints attributes of the package
    def __str__(self):
        print(f"{self.pkgID:^10}{self.pkgAddress:^40}{self.pkgCity:^20}{self.pkgState:^10}{self.pkgZip:^10}{self.pkgWeight:^10}{str(self.timeDepart):^15}{str(self.pkgStatus):^15}{str(self.timeDelivery):^20}{self.pkgDeadline:^10}", end = "  ")
        return ""

    # Given a time, check the status of the package
    def checkStatus(self, deltaTime):
        # Mark as delivered if the time of delivery is before the current time
        if self.timeDelivery < deltaTime:
            self.pkgStatus = "Delivered!"
        # Mark as en route if the time of departure is before the current time
        elif deltaTime > self.timeDepart:
            self.pkgStatus = "En route!"
        else: 
            self.pkgStatus = "At the hub!"

# Class to describe a truck object               
class Truck:
    # Constructor
    def __init__(self, speed, mileage, pkgInventory,currentAddress, timeDepart):
        self.speed = speed
        self.mileage = mileage
        self.pkgInventory = pkgInventory
        self.currentAddress = currentAddress
        self.timeDepart = timeDepart
        self.timeCurrent = self.timeDepart
       

# Loads data from the distance table file into a list
with open("traveling-salesman\Data\WGUPS Distance Table.csv") as distanceInfo:
    distanceCSV = csv.reader(distanceInfo)
    distanceCSV = list(distanceCSV)

# Loads data from the address file into a list
with open("traveling-salesman\Data\Address_File.csv") as addressInfo:
    addressCSV = csv.reader(addressInfo)
    addressCSV = list(addressCSV)

# Loads data from the package file into a list
with open("traveling-salesman\Data\WGUPS Package File.csv") as packageInfo:
    packageCSV = csv.reader(packageInfo)
    packageCSV = list(packageCSV)

# Extracts attributes from each package to create a Package object
def loadPackageData(pkgHashmap):
        for package in packageCSV:
            pkgID = int(package[0])
            pkgAddress = package[1]
            pkgCity = package[2]
            pkgState = package[3]
            pkgZip = package[4]
            pkgDeadline = package[5]
            pkgWeight = package[6]
            pkgStatus = None

            pkg = Package(pkgID, pkgAddress, pkgCity, pkgState, pkgZip, pkgDeadline, pkgWeight, pkgStatus)

            # Adds the package into the hashmap 
            pkgHashmap.addKVPair(pkgID, pkg)

# Creates the adjacency table from the distance list
distanceData = []
def loadDistanceData(distanceData):
    for distance in distanceCSV:
        distanceData.append(distance)

# Creates a list to store address indexes
addressData = []
def loadAddressData(addressData):
    for address in addressCSV:
        addressData.append(address[2])

# Given a string of an address, returns its index
def getAddress(givenAddress):
    for address in addressData:
        if givenAddress == address:
            return addressData.index(address)
            
# Calculates the distance between address x and address y
def distanceBetween(x, y):
    distance = distanceData[x][y]
    if distance == '':
        distance = distanceData[y][x]
    return float(distance)

# Calculates the closest address to a given address
def minDistanceFrom(fromAddress, truckPackages):
    minDistance = (distanceBetween(fromAddress, getAddress(pkgHashmap.searchKey(truckPackages[0]).pkgAddress)))
    for package in truckPackages:
        toAddress = getAddress(pkgHashmap.searchKey(package).pkgAddress)
        distance = distanceBetween(fromAddress, toAddress)
        if (distance < minDistance):
            minDistance = distance
            minAddress = toAddress
    return minAddress

# Uses the nearest neighbor algorithm to deliver a truck's packages
def truckDeliverPackages(truck: Truck):
    print(f"truck departs on {truck.timeDepart}")
    # Creates a list of unvisited packages
    unvisited = []

    # Populates the unvisited list with Package objects
    for packageID in truck.pkgInventory:
        pkg = pkgHashmap.searchKey(packageID)
        unvisited.append(pkg)

    truck.pkgInventory.clear()


    while len(unvisited) > 0:
        nextAddressTime = 5000
        nextPackage = None

        # Determines the closes package to the truck's current address
        for package in unvisited:
            if distanceBetween(getAddress(truck.currentAddress), getAddress(package.pkgAddress)) <= nextAddressTime:
                nextAddressTime = distanceBetween(getAddress(truck.currentAddress), getAddress(package.pkgAddress))
                nextPackage = package
        
        # Add nearest package ID to the delivery queue
        truck.pkgInventory.append(nextPackage.pkgID)
        
        # Removes nearest package from the unvisited list
        unvisited.remove(nextPackage)
        
        # Add to truck's total mileage
        truck.mileage += nextAddressTime
        
        # Truck drives to the next address. Replace current address with the next address.
        truck.currentAddress = nextPackage.pkgAddress
        
        # Keeps track of delivery and departure times of the truck
        truck.timeCurrent += datetime.timedelta(hours=nextAddressTime / 18) #18mph speed
        nextPackage.timeDelivery = truck.timeCurrent
        nextPackage.timeDepart = truck.timeDepart
        print(f"Package {nextPackage.pkgID} delivered on {truck.timeCurrent} at {nextPackage.pkgAddress}") #DEBUG
    print(f"packages for truck = {truck.pkgInventory}")

# Displays menu
def menu():
    print("\n1. Display total mileage and all of the packages' status")
    print("2. Search a package status by timestamp")
    print("3. Search all package status by timestamp ")
    print("4. Exit")

# Displays headers for the package attributes
def printHeaders():
    print("=" * 160)
    print(f"{'|ID|':^10}{'|Address|':^40}{'|City|':^20}{'|State|':^10}{'|Zip|':^10}{'|Weight|':^10}{'|Time Departed|':^15}{'|Status|':^15}{'|Time of Delivery|':^20}{'|Deadline|':^10}")
    print("=" * 160)

# Creates the package hashmap for the 40 packages      
pkgHashmap = CreateHashmap(40)

# Load all of the data from the csv files
loadPackageData(pkgHashmap)
loadDistanceData(distanceData)
loadAddressData(addressData)

# Instantiates the Truck objects. Trucks are loaded manually.
truck1 = Truck(18, 0, [15,14,13,16,20,19,17,29,30,31,34,37], '4001 South 700 East', datetime.timedelta(hours=8))
truck2 = Truck(18, 0, [2,3,4,5,7,8,9,10,11,12,18,21,22,23,24,36,38], '4001 South 700 East', datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(18, 0, [1,6,25,26,27,28,32,33,35,39,40], '4001 South 700 East', datetime.timedelta(hours=9, minutes=5)) # some packages dont arrive until 0905

# Runs the delivery algorithm for each truck to deliver all of the packages
truckDeliverPackages(truck1)
truckDeliverPackages(truck3)
truckDeliverPackages(truck2)

selection = 0
# Command line interface keeps running until user exits by inputting 4
while selection != '4':
    menu()
    selection = input("Select an option: ")
    # Displays total mileage and all of the packages' status"
    if selection == '1':
        print(f"Total mileage for the route: {truck1.mileage + truck2.mileage + truck3.mileage}")
        printHeaders()
        # End of day time is 5PM
        timeEOD = datetime.timedelta(hours=17)

        # Prints out the attributes for all packages
        for packageID in range(1,41):
            pkg = pkgHashmap.searchKey(packageID)
            # Checks the status of each package at the end of the day
            pkg.checkStatus(timeEOD)
            print(pkg)
    # Search a package status by timestamp
    elif selection == '2':
        # Prompts a time to search
        time = input("Please enter time in HH:MM:SS format: ")
        (h, m, s) = time.split(":")
        time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        
        # Prompts a package to search
        pkgID = input("Please enter a package ID: ")
        package = pkgHashmap.searchKey(int(pkgID))
        # Checks the status of each package at the given time
        package.checkStatus(time)

        print("")
        printHeaders()
        print(package)
    # Search all package status by timestamp
    elif selection == '3': 
        # Prompts a time to search
        time = input("Please enter time in HH:MM:SS format: ")
        (h, m, s) = time.split(":")
        time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        printHeaders()
        # Iterates through each package and displays its status during a given time
        for packageID in range(1,41):
            pkg = pkgHashmap.searchKey(packageID)
            pkg.checkStatus(time)  
            print(pkg)
    # Exit
    elif selection == '4':
        print("Exiting program.")
        exit()




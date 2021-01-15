# Alex Irvine
# C950 submission
# WGU Student # 000955107
# Date = 2020/7/15

from datetime import datetime, timedelta
from Hash_Table import HashTable
from Package import Package 
from Truck import Truck
import re

# Creates the global variables for this project (Hash Table, Time, Trucks)
receiveing = HashTable()
global_time = datetime(2020,1,1,8,00)
truck1 = Truck(receiveing.handload_truck_1(), datetime(2020,1,1,9,5), 1, receiveing)
truck2 = Truck(receiveing.handload_truck_2(), datetime(2020,1,1,8,00), 2, receiveing)
truck3 = Truck(receiveing.handload_truck_3(), datetime(2020,1,1,23,59), 3, receiveing)


def run_deliveries(delivery_time = datetime(2020,1,1,23,59)):
    '''
    Runs the deliveries of all 3 trucks until global time matches delivery time.  
    Starts trucks at the appropriate times, including truck 3 which will leave when another comes back.
    Stops running deliveries once every package is delivered and all trucks returned to hub.  
    Also updates package 9 at appropriate time.

    Space-time complexity = O(N)
    '''
    global global_time

    while global_time < delivery_time:

        # Starts truck 3 once another truck comes back to hub
        if truck3.status == 'AT HUB, START OF DAY' and truck2.status == 'Deliveries complete' or truck1.status == 'Deliveries complete':
            truck3.time = global_time

        # Update package 9 at 10:20 AM
        if global_time == datetime(2020,1,1,10,20):
            receiveing.update_package_nine()

        # Moves each truck 0.1 miles & 20 seconds if there are more deliveries for it to make.  
        # (Time does not increment for truck if there is no more miles to drive)
        if global_time == truck1.time:
            truck1.tick()
        if global_time == truck2.time:
            truck2.tick()
        if global_time == truck3.time:
            truck3.tick()

        # If all deliveries are completed, exit while loop
        if truck1.status == 'Deliveries complete' and truck2.status == 'Deliveries complete' and truck3.status == 'Deliveries complete':
            break

        # Increments global time by 20 seconds (the time it takes to drive 0.1 miles)
        global_time  += timedelta(0, 20)

    # Sets Global time to equal deliver time, 
    #  needed in case the delivery time exceeds time needed to deliver packages
    global_time = delivery_time

def deliver_packages_to_time():
    '''
    Prompts user to enter a time and runs the method run_deliveries to that time.  
    If no time is entered, or an invalid time is entered, then run_deliveries will default to EOD.  

    Space-time complexity = O(N)
    '''
    # Prompts user to enter time and uses regular expression pattern to find the numbers in the answer given
    input_time = input("Please enter a time in hours (24 hour format) and minutes [hh:mm]\nOr press <enter> to set time to EOD - ")
    match = re.match(r'(\d+)\D+(\d+)', input_time)

    # If 2 matches are found (hours & minutes), run the method run_deliveries using the prompted time as argument
    if match and match.lastindex == 2:
        hour = int(match.group(1))
        minute = int(match.group(2))
        run_deliveries(datetime(2020,1,1,hour,minute))

    # If 2 matches are not found, run the run_deliveries method which will default to EOD
    else:
        run_deliveries()

def create_new_package():
    '''
    Prompts user for new package attributes and creates a package based on them.  
    The method will also dynamically assign package & address ID to the package.  
    If there is room in the hash table, the package is then inserted into it.  
    If there is no room in the hash table, a bucket is created for the package to be inserted.

    Space-time complexity = O(N)
    '''
    global receiveing
    package_id = -1
    address_id = -1

    # Find empty bucket in Hash Table and sets it's index to package id
    # This is valid because we are using a direct hash table
    for i in range(len(receiveing.package_table)):
        if type(receiveing.package_table[i]) != Package:
            package_id = i
            break

    # If no empty bucket was found, then hash table full.  
    # Append an empty bucket to the hash table and make it's index the package id
    if package_id == -1:
        receiveing.package_table.append(None)
        package_id = len(receiveing.package_table) - 1


    # Prompts user to enter package details.  
    print("Please enter package details below.\n")
    address = input("Address: ")
    city = input("City: ")
    state = input("State: ")
    zip_code = input("Zip: ")
    weight = input("Weight: ")
    deadline = input("Deadline: ")
    instructions = input("Instructions: ")

    # Checks if address already exists in hash table.
    # If yes, set address_id to matching address_id. 
    # If no, create a new address_id not already usedl
    if receiveing.lookup_packages('address', address):
        address_id = receiveing.lookup_packages('address', address)[0].address_id
    else:
        address_id = receiveing.num_addresses

    # Create package with attributes entered by user
    package = Package(package_id)
    package.address_id = address_id
    package.address = address
    package.city = city
    package.state = state
    package.zip_code = zip_code
    package.weight = weight
    package.deadline = deadline
    package.instructions = instructions

    # Inserts package into hash table
    receiveing.insert_package(package)

def print_status():
    '''
    Prints status of trucks & hash table.

    Space-time complexity = O(1)
    '''

    # Prints everything
    print(receiveing)
    print(truck1)
    print(truck2)
    print(truck3)
    print(f'\nTotal miles driven = {round(truck1.millage + truck2.millage + truck3.millage, 1)}')
    print(f'Current time = {global_time.time()}')

    # Waits for user to press enter before moving on
    input('\nPress enter to continue...')

def main():
    '''
    Main controller of the program, controls the UI.  
    Prompts the user with options for program and runs each method accordingly.
    '''
    
    # Prints welcome screen in ASCII art.  
    print(f'''
        ******************************************************************************************************************************
        * __          _______ _    _ _____   _____    _____           _                       _____       _ _                        *
        * \ \        / / ____| |  | |  __ \ / ____|  |  __ \         | |                     |  __ \     | (_)                       *
        *  \ \  /\  / / |  __| |  | | |__) | (___    | |__) |_ _  ___| | ____ _  __ _  ___   | |  | | ___| |___   _____ _ __ _   _   *
        *   \ \/  \/ /| | |_ | |  | |  ___/ \___ \   |  ___/ _` |/ __| |/ / _` |/ _` |/ _ \  | |  | |/ _ \ | \ \ / / _ \ '__| | | |  *
        *    \  /\  / | |__| | |__| | |     ____) |  | |  | (_| | (__|   < (_| | (_| |  __/  | |__| |  __/ | |\ V /  __/ |  | |_| |  *
        *     \/  \/   \_____|\____/|_|    |_____/   |_|   \__,_|\___|_|\_\__,_|\__, |\___|  |_____/ \___|_|_| \_/ \___|_|   \__, |  *
        *                                                                        __/ |                                        __/ |  *
        *                                                                       |___/                                        |___/   *
        *                                                                                                                            *
        ******************************************************************************************************************************                                                                    
    ''')

    # Main loop.  Prompts user for actions until exit is chosen. 
    while True:
        print(f''' 
        Current time = {global_time.hour}:{global_time.minute:>02}

        1) Set time of day
        2) Print current package & truck status
        3) Insert new package
        4) Lookup package based on address
        5) Lookup package based on city
        6) Lookup package based on zip code
        7) Lookup package based on weight
        8) Lookup package based on deadline
        9) Lookup package based on status
        0) Exit program
        ''')

        selection = input('Please select an option: ').strip()

        # 1) Set time of day
        if selection == '1':
            deliver_packages_to_time()
        
        # 2) Print current package & truck status
        elif selection == '2':
            print_status()
        
        # 3) Insert new package
        elif selection == '3':
            create_new_package()
        
        # 4) Lookup package based on address
        elif selection == '4':
            address = input('Enter the address you would like to lookup: ')
            addresses = receiveing.lookup_packages('address', address)
        
            print(f'Packages with Address: {address}\n----------------------')
            for p in addresses:
                print(str(p))

            input()

        # 5) Lookup package based on city
        elif selection == '5':
            city = input('Enter the city you would like to lookup: ')
            cities = receiveing.lookup_packages('city', city)

            print(f'Packages with City: {city}\n-------------------')
            for p in cities:
                print(str(p))

            input()
        
        # 6) Lookup package based on zip code
        elif selection == '6':
            zip_code = input('Enter the zip you would like to lookup: ')
            zips = receiveing.lookup_packages('zip_code', zip_code)

            print(f'Packages with Zip: {zip_code}\n------------------')
            for p in zips:
                print(str(p))

            input()
        
        # 7) Lookup package based on weight
        elif selection == '7':
            weight = input('Enter the weight you would like to lookup: ')
            weights = receiveing.lookup_packages('weight', weight)

            print(f'Packages with Weight: {weight}\n---------------------')
            for p in weights:
                print(str(p))

            input()

        # 8) Lookup package based on deadline
        elif selection == '8':
            deadline = input('Enter the deadline you would like to lookup: ')
            deadlines = receiveing.lookup_packages('deadline', deadline)

            print(f'Packages with deadline: {deadline}\n-----------------------')
            for p in deadlines:
                print(str(p))

            input()
        
        # 9) Lookup package based on status
        elif selection == '9':
            status = input('Enter the status you would like to lookup: ')
            statuses = receiveing.lookup_packages('status', status)

            print(f'Packages with status: {status}\n---------------------')
            for p in statuses:
                print(str(p))

            input()
        
        # 0) Exit program
        elif selection == '0':
            input('Thank you for choosing WGUPS!\nGoodbye....')
            exit()

        # Invalid input
        else:
            input('Invalid input, please try again')

if __name__ == "__main__":
    main()
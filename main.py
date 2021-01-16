from datetime import datetime, timedelta
from Hash_Table import HashTable
from Package import Package 
from Truck import Truck
import re

# Creates the global variables for this project (Hash Table, Time, Trucks)
receiveing = HashTable()
global_time = datetime(2021,1,10,8,00)
truck1 = Truck(receiveing.handload_truck_1(), datetime(2021,1,10,9,5), 1, receiveing)
truck2 = Truck(receiveing.handload_truck_2(), datetime(2021,1,10,8,00), 2, receiveing)
truck3 = Truck(receiveing.handload_truck_3(), datetime(2021,1,10,23,59), 3, receiveing)


def run_deliveries(delivery_time = datetime(2021,1,10,23,59)):
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
        if global_time == datetime(2021,1,10,10,20):
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
        run_deliveries(datetime(2021,1,10,hour,minute))

    # If 2 matches are not found, run the run_deliveries method which will default to EOD
    else:
        run_deliveries()

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

    # Main loop.  Prompts user for actions until exit is chosen. 
    while True:
        print(f''' 
        Current time = {global_time.hour}:{global_time.minute:>02}

        1) Set time of day
        2) Print current package & truck status
        3) Lookup package by ID
        0) Exit program
        ''')

        selection = input('Please select an option: ').strip()

        # 1) Set time of day
        if selection == '1':
            deliver_packages_to_time()
        
        # 2) Print current package & truck status
        elif selection == '2':
            print_status()

        # 3) Lookup package based on ID
        elif selection == '3':
            packageId = input('Enter the package ID: ')
            package = receiveing.retrieve_package(int(packageId))
            package = str(package.__init__)
            id = re.search("package_id=(.+?),", package).group(1)
            address = re.search(", address='(.+?)',", package).group(1)
            city = re.search(", city='(.+?)',", package).group(1)
            zip_code = re.search(" zip_code='(.+?)',", package).group(1)
            deadline = re.search(" deadline='(.+?)',", package).group(1)
            status = re.search(", status='(.+?)',", package).group(1)
            try:
                instructions = re.search(", instructions='(.+?)'", package).group(1)
            except AttributeError:
                instructions = '-' 
            
            idstring = "ID"
            addressstring = "ADDRESS"
            citystring = "CITY"
            zipstring = "ZIP"
            deadlinestring = "DEADLINE"
            statusstring = "STATUS"
            instructionstring = "INSTRUCTIONS" 
            return_string = '---------------------------------------------------------------------------------------------------------------------------------------------------------------\n'
            return_string += f'{idstring:^10}|{addressstring:^42}|{citystring:^20}|{zipstring:^10}|{deadlinestring:^10}|{statusstring:^35}|{instructionstring:^20}\n'
            return_string += '---------------------------------------------------------------------------------------------------------------------------------------------------------------\n'
            return_string += f'{id:^10}|{address:^42}|{city:^20}|{zip_code:^10}|{deadline:^10}|{status:^35}| {instructions:^20}\n'
            print(package)
            print(return_string)            
            input()

        # 0) Exit program
        elif selection == '0':
            exit()

        # Invalid input
        else:
            input('Invalid input, please try again')

if __name__ == "__main__":
    main()
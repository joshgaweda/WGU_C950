from dataclasses import dataclass

@dataclass
class Package:
    '''
    Holds data on packages.  
    '''

    package_id: int
    address_id: int = None
    address: str = None
    deadline: str = None
    city: str = None
    state: str = None
    zip_code: str = None    
    weight: float = None
    status: str = ' At Hub'
    instructions: str = None

    def __str__(self):
        '''
        Returns a string of the package attributes.
        Primarily used in other functions for printing a table.

        Space-time complexity = O(1)
        '''
        return f'ID = {self.package_id:>02}\t\tAddress = [{self.address_id:>02}] {self.address:>39} {self.city:>16},{self.state:<2} {self.zip_code:<15}Weight = {self.weight:<3}\t\tInstruction = {self.instructions:<40}\t\tStatus = {self.status}'

    def __eq__(self, other):
        '''
        Method used to compare the equality of two packages.
        Equality for packages is based on package_id.

        Space-time complexity = O(1)
        '''
        return self.package_id == other.package_id
    
import csv

DEBUG = True

class CSVLoader:
    def __init__(self, data_file:str):
        persons=[]

        with open(data_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                persons.append(row)
        
        self.persons = persons

    def users(self, count:int=None):
        
        if count is None:
            return self.persons
        else:
            return self.persons[:count]

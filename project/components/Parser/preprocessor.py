import csv

DEBUG = True

class Preprocessor():
    def __init__(self):
        self.linkedins = []
        self.fields = []

    def load_data(self, file:str):
        result = []
        headers = None
        
        with open(file, 'r') as form:
            reader  = csv.DictReader(form)
            
            for row in reader:
                if not headers:
                    headers = list(row.keys())

                result.append({k: v for k, v in row.items()})
        
        self.load_data = result
        
        if DEBUG:
            for entry in self.load_data:
                print(f"Row of type {type(entry)}: {entry}")
                
                for key, value in entry:
                    print(f"{key}: {value}")

        return result

    def clean_data():
        pass

    def set_columns(self, columns):

        # for key, value in self.load_data:
        #     print(f"Key: {key} - Value: {value}")

        return None
                


if DEBUG:
    preprocessor = Preprocessor()
    preprocessor.load_data("data/lunch_submissions.csv")
    columns = ['name', 'uni', 'studies', 'sph', 'experiences', 'biggest_achievment', 'biggest_failure', 'success_definition', 'hobbies']
    preprocessor.set_columns(columns)


#Clean up and syntheetically generates empty columns?
def remove_empty_fields(file: str):
    """Removes all the empty fields from the provided file."""
    with open(file, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader if row]

def preprocessor(linkedins, fields):
    """Generates the users table by scraping all the linkedins and populating a table with the provided columns."""
    pass

linkedins = [
    "https://www.linkedin.com/in/john-doe-1234567890/"
]

fields = [
    "Name",
    "Location",
    "Industry",
    "Company",
    "Position",
    "Seniority",
    "LinkedIn"
]

# preprocessor(linkedins, fields)




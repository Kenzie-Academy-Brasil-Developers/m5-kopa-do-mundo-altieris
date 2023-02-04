from datetime import datetime, timedelta
from rest_framework.views import Response

class NegativeTitlesError(Exception):
    def __init__(self, message):
        self.message = message
        
class InvalidYearCupError(NegativeTitlesError):
    def __init__(self, message):
        self.message = message
        
class ImpossibleTitlesError(NegativeTitlesError):
    def __init__(self, message):
        self.message = message
             
def data_processing(data: dict):
    if data["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative") 
    
    list_cups = []

    for i in range(1930, 2023, 4):
        list_cups.append(i)
    
    date_cup = data["first_cup"]
    
    date_object = datetime.strptime(date_cup, "%Y-%m-%d")
    
    year = date_object.strftime("%Y")

    count = 0

    for i in list_cups:
        if i == int(year):
            count += 1

    if count == 0:
        raise InvalidYearCupError("there was no world cup this year")
    
    list_cups_possible = 0
    
    for i in range(int(year), 2023, 4):
        list_cups_possible += 1
    
    if list_cups_possible < data["titles"]:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")

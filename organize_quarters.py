"""Organize and list unique quarters"""
from os import name
import re

def distinct_print(_to_print):
    """Helper method to have a distinct print in the console"""
    print("***********" + _to_print + "***********\n")

def mysplit(string, delim=None):
    """Helper function"""
    return [x for x in re.split(delim, string) if x]

def sort_by(quarter_list, index):
    """Helper function to sort on a specific element"""
    return quarter_list[index].lower()

def sort_quarters_by_state(_quarters_list):
    """Helps sort the quarters by state names"""
    _quarters_list.sort(key = lambda current_quarter: sort_by(current_quarter, 0))
    return _quarters_list

def full_sort_quarters(_state_sorted_quarters):
    """Sorts the quarters fully (by year) after sorted by state"""
    final_list = []
    temp_list = []
    while _state_sorted_quarters:
        current_quarter = _state_sorted_quarters.pop(0)
        next_quarter = current_quarter
        if _state_sorted_quarters:
            next_quarter = _state_sorted_quarters[0].copy()
            next_quarter[0] = next_quarter[0].lower()
        temp_list.append(current_quarter)
        while _state_sorted_quarters and current_quarter[0].lower() == next_quarter[0].lower():
            temp_list.append(_state_sorted_quarters.pop(0))
            if _state_sorted_quarters:
                next_quarter = _state_sorted_quarters[0].copy()
                next_quarter[0] = next_quarter[0].lower()
        temp_list.sort(key = lambda x: sort_by(x, 1))
        temp_list = prepare_flatten(temp_list)
        final_list.extend(temp_list)
        temp_list.clear()
    return final_list

def recapitalize_specific(_word):
    """Recapitalizes words or special abbreviations as needed"""
    if (not _word.isalpha()) and not _word.__contains__("'") and not _word.__contains__("’"):
        # "'" not in _word and "’" not in _word:
        return _word.upper()
    return _word.capitalize()

def recapitalize_quarters(_quarters):
    """Returns quarters with names capitalized as needed"""
    completed_quarters_list = []
    for quarter in _quarters:
        completed_quarters_list.append(recapitalize_quarter(quarter))
    return completed_quarters_list

def recapitalize_quarter(_quarter):
    """Helps capitalize the names of Quarters"""
    avoid_words = get_capitalize_list()
    quarter_name = _quarter[0].split()
    quarter_name[0] = recapitalize_specific(quarter_name[0])
    for index in range(1, len(quarter_name)):
        if index == len(quarter_name) - 1:
            quarter_name[index] = recapitalize_specific(quarter_name[index])
        elif quarter_name[index] not in avoid_words:
            quarter_name[index] = recapitalize_specific(quarter_name[index])
    _quarter[0] = recombine_quarter_name(quarter_name).pop()
    return _quarter

def flatten_list(_2d_list):
    """Helper function to flatten list in the end"""
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        quarter = element[0] + element[1]
        flat_list.append(quarter)
    return flat_list

def prepare_flatten(_list_to_flatten):
    "Prepares the string of the quarters before flattening"
    flattened_list = []
    for quarter in _list_to_flatten:
        quarter[1] = " " + quarter[1]
        flattened_list.append(quarter)
    return flattened_list

def recombine_quarter_name(_quarter_name):
    """Helper method to recombine names after a split by spaces"""
    while len(_quarter_name) > 1:
        _quarter_name[0] = _quarter_name[0] + " " + _quarter_name.pop(1)
    return _quarter_name

def get_viable_quarter(_quarter_string):
    """This will return the viable quarter"""
    _quarter_string = _quarter_string.strip()
    if _quarter_string and _quarter_string != "":
        quarter_list = mysplit(_quarter_string, DELIM_CONST)
        # This checks if its in the form <INT>. <Quarter Name> <Year>
        if len(quarter_list) == 3:
            # Popping off the number in front
            quarter_list.pop(0)
        elif len(quarter_list) > 2:
            return None
        elif not quarter_list[-1].isnumeric():
            return None
        # Split off all spaces in the string
        quarter_name = quarter_list[0].split()
        if "." in quarter_name[0]:
            # Pop off the dot in the beginning
            quarter_name.pop(0)
        # Recombines the quarter name without trailing or big spaces
        quarter_name = recombine_quarter_name(quarter_name)
        quarter_list[0] = quarter_name.pop().lower()
        quarter_list[1] = quarter_list[1].strip()
        return quarter_list
    return None


def get_main_quarters():
    """Opens the main quarters file and appends each quarter to a list"""
    main_quarters = []
    faulty_quarters = []
    duplicate_quarters = []
    with open('Quarters.txt', 'r' , encoding='utf-8') as quarters_file:
        for line in quarters_file:
            line = line.strip()
            #A viable quarter from the main list either has the form <INT, Quarter Name, Year>
            #Or it could be <Quarter Name, Year>
            quarter = get_viable_quarter(line)
            if quarter:
                if quarter in main_quarters:
                    if quarter not in duplicate_quarters:
                        duplicate_quarters.append(quarter)
                else:
                    main_quarters.append(quarter)
            else:
                faulty_quarters.append(line)
    if duplicate_quarters:
        distinct_print("Duplicate Quarters Found")
        print(recapitalize_quarters(sort_quarters_by_state(duplicate_quarters)))
    if faulty_quarters:
        distinct_print("Cannot Organize the Following Quarters")
        print(faulty_quarters)
    return main_quarters


def get_new_quarters(main_quarters_list):
    """Opens the new list of quarters and appends new quarters to the main list if not present"""
    duplicate_quarters = []
    faulty_quarters = []
    new_quarters_list = []
    with open("NewQuarters.txt", 'r', encoding='utf-8') as new_quarters_file:
        for line in new_quarters_file:
            quarter = get_viable_quarter(line)
            if quarter:
                if quarter in main_quarters_list:
                    if quarter not in duplicate_quarters:
                        duplicate_quarters.append(quarter)
                else:
                    new_quarters_list.append(quarter)
                    main_quarters_list.append(quarter)
            elif line.strip() != "":
                faulty_quarters.append(line.strip())
    if new_quarters_list:
        distinct_print("New Quarters Added")
        print(recapitalize_quarters(sort_quarters_by_state(new_quarters_list)))
    if faulty_quarters:
        distinct_print("Faulty Quarters")
        print(faulty_quarters)
    if duplicate_quarters:
        distinct_print("Duplicates Found")
        print(recapitalize_quarters(sort_quarters_by_state(duplicate_quarters)))
    return main_quarters_list

def write_to_main_list(sorted_quarters):
    """Writes all sorted quarters to a file"""
    with open("OrganizedQuarters.txt", 'w', encoding='utf-8') as organzied_quarters_file:
        for quarter in sorted_quarters:
            organzied_quarters_file.write(quarter + "\n")

def get_capitalize_list():
    """Gets the words NOT to capitalized and returned as a list"""
    capitalize_list = []
    with open("CapitalizeList.txt", 'r', encoding='utf-8') as capitalize_list_file:
        for word in capitalize_list_file:
            capitalize_list.append(word.strip())
    return capitalize_list


DELIM_CONST = '(\\d+)'

print("This program assumes that all quarters (new or old) follows the format <Quarter Name, Year>")
print("If any quarter has any integer within its 'Quarter Name' field, then it is skipped")

# Gets the main list of quarters from Quarters.txt
print("Getting quarters from Quarters.txt")
quarters_list = get_main_quarters().copy()

#Get the new quarters and add them to the main list and return it
print("Getting the new quarters from NewQuarters.txt")
quarters_list = get_new_quarters(quarters_list.copy())

#Sort the quarters list by 'Quarter Name'
print("Sorting quarters by state...")
state_sorted_list = sort_quarters_by_state(quarters_list)

#Now sort the quarters by 'Year' but keeping the 'Quarter Names' together
print("Sorting quarters by year that share the same name...")
fully_sorted_quarters = full_sort_quarters(state_sorted_list)

#print(fully_sorted_quarters)

#Recapitalize words as needed
print("Recapitalizing words as needed...")
completed_quarters = recapitalize_quarters(fully_sorted_quarters)

#print(completed_quarters)

#Write fully sorted quarters to the 'OrganizedQuarters.txt file
print("Writing fully sorted quarters to OrganizedQuarters.txt")
write_to_main_list(flatten_list(completed_quarters))

class Quarter:
    def __init__(self, name, year):
        self.name = name
        self.year = year
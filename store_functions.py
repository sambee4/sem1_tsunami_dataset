
import csv

def print_welcome():
    separator = "-"*75
    print(separator)
    print("Welcome to the Tsunami and Earthquake DataSet!")
    print("You can search through historical data from 1800 - 2021. How neat!\n\
Use this to search for historical tsunami data and related earthquakes.\n\
Credit to 'Ram Jas - Historical Data of Tsunamis (1800-2021)' from kaggle.com for data.")
    print("Please note: Some information may be missing in older records due to lack of widespread and/or available technology.")
    print(separator)

#get user input, open file, filter choices
def search_and_filter_user_choice(csv_file_path):
    #prompt user to enter a choice between 1 or 2
    separator = ("-" * 75)

    user_input = input("\nChoose a following search method:\n1 - Search by Year\n2 - Search by Country\n\
Type 'Done' to quit the program.\nEnter choice (1 or 2): ")
    
    #loop until valid input from user
    while user_input.lower() not in ['1','2','done']:
        print("Invalid choice. Please choose '1' for 'Year' or '2' for 'Country'.")
        user_input = input("\nChoose a following search method:\n\
1. Year\n2. Country\nType 'Done' to quit the program.\nEnter choice (1 or 2): ")

    #check if user entered correct choice and assign column index to search year or country
    if user_input == '1':
        while True:
            try:
                data_type = int(input("Enter the year (1800-2021): "))
                if 1800 <= data_type <= 2021:
                    break #breaks out of loop and assigns column index to 0 outside of loop (search by year[0] in csv file)
                else:
                    print("Invalid year. Enter a value between 1800-2021.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        column_index = 0 #assigns the search index (column_index being searched) to 0 (Year)
    elif user_input == '2':
        valid_country_names = set()  #sets variable to add valid country names from csv file before user inputs country name
        with open(csv_file_path, "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            valid_country_names.update(row[10] for row in csv_reader) #stores country names into set() function before prompting user for country name
        while True:
            try:
                data_type = input("Enter the country: ").upper() #converts users choice to upper to match CSV value lettercase
                if data_type in valid_country_names:
                    break
                else:
                    print("Country not found in file. Please check spelling and try again.")
            except ValueError:
                print("Invalid value entered.")
        column_index = 10 #assigns the search index (column_index being searched) to 10 (Country)
    elif user_input.lower() == 'done':
        exit() #closes program
    else:
        print("~WEE WOO WEE WOO!~ You have entered an invalid input.")

    #open csv file as unfiltered data
    with open(csv_file_path, "r") as unfiltered_data:
        csv_reader = csv.reader(unfiltered_data)
        header = next(csv_reader) #skips header row
    #stores list of header values chosen from csv that will be used for filtering data and outputting info to user
        output_columns = [header[i] for i in [0, 1, 2, 7, 10, 11, 8, 14]]
        for i in range(len(output_columns)):
            if i == 1:
                output_columns[i] = "Month" #changes [1] in csv header from "Mn" to "Month" for user display
            elif i == 2:
                output_columns[i] = "Day" #changes [2] in csv header from "Dy" to "Day" for user display
            elif i == 6:
                output_columns[i] = "EQ Magnitude" #changes [6] in csv header from "Earthquake Magnitude" to "EQ Magnitude" for smaller display

    #store filtered data that contains the data_type the user entered into list
        filtered_data = []
        for row in csv_reader: #iterate through each row in unfiltered data that contains data_type chosen and sorts into filtered_data list
            if row[column_index] == str(data_type): #converts data_type to string because choice can be either int(yr) or str(country)
                selected_row = [row[i] for i in [0, 1, 2, 7, 10, 11, 8, 14]] #iterates through each row and gathers indexed values (matching header values)
                filtered_data.append(selected_row) #stores selected_rows that contain the data_type into the filtered_data list

    # #if user input is a year, how to sum up largest tsunamis and earthquakes by country below
    if user_input == '1':
        country_counts = {}  # Dictionary to store the count of tsunamis per country
        max_tsunami = 0  # variable to store size of largest tsunami
        max_tsunami_country = []  # list to store countries with the largest number of tsunamis per chosen year
        max_tsunami_cities = [] # list stores city or cities associated with the largest tsunami(s)

        max_earthquake_magnitude = 0  # variable set to store the intensity of largest earthquake
        max_earthquake_country = []  # list to store countries with the most earthquakes
        max_earthquake_cities = [] #list used to store cities with largest earthquakes
        #iterate through each row in filtered data to count tsunami and earthquake totals per country and calculate max intensity of each
        for row in filtered_data:
            try:
                country = row[4] #country is 4th index in each row
                tsunami_count = country_counts.get(country, 0) + 1 #count tsunamis per country as it iterates through rows
                country_counts[country] = tsunami_count #stores country and count of tsunamis in country

                # Check for the largest tsunami
                tsunami_value = float(row[7]) if row[7] != "" else 0
                if tsunami_value > max_tsunami:
                    max_tsunami = tsunami_value
                    max_tsunami_country = [country]
                    max_tsunami_cities = [row[5]]
                elif tsunami_value == max_tsunami:
                    max_tsunami_country.append(country)
                    max_tsunami_cities.append(row[5])

                # Check for the largest earthquake
                earthquake_value = float(row[6]) if row[6] != "" else 0
                if earthquake_value > max_earthquake_magnitude: #if earthquake value larger than current max_earthquake
                    max_earthquake_magnitude = earthquake_value #new maximum is the earthquake value
                    max_earthquake_country = [country] #assigns current country to max_eq_country list
                    max_earthquake_cities = [row[5]] #assigns city to city with largest earthquake list
                elif earthquake_value == max_earthquake_magnitude:
                    max_earthquake_country.append(country)
                    max_earthquake_cities.append(row[5])

            except ValueError as e:
                print(f"Error: {e}. Skipping row in data processing.")
            except Exception as e:
                print(f"Unexpected error: {e}. Skipping row in data processing.")

        most_tsunamis_count = max(country_counts.values()) #gets the highest value of counted tsunamis in country_counts dict
        #iterates through country_counts, country or countries w/ most tsunamis appends to list
        most_tsunamis_countries = [country for country, count in country_counts.items() if count == most_tsunamis_count]
        print(separator)
        print(f"Statistics for the year {data_type}:")

        # check for multiple countries being tied for tsunami amounts
        if len(most_tsunamis_countries) == 1:
            most_tsunamis_country = most_tsunamis_countries[0]
            print(f"Country with the most tsunamis: {most_tsunamis_country} - {most_tsunamis_count} tsunami(s)")
        else:
            print(f"Tie for the most tsunamis among countries: {', '.join(most_tsunamis_countries)} - {most_tsunamis_count} tsunami(s)")

        # check for ties in the largest tsunami intensity
        if len(max_tsunami_country) == 1:
            print(f"Largest Tsunami: {max_tsunami} meters in {', '.join(map(str, max_tsunami_cities))}, {max_tsunami_country[0]}")
        else:
            print(f"Tie for the largest tsunami among countries: {', '.join(map(str, max_tsunami_country))} ({max_tsunami} meters)")

        # Check for ties in largest earthquake intensity and amount
        if max_earthquake_magnitude > 0:
            if len(max_earthquake_country) == 1:
                print(f"Largest Earthquake: Magnitude {max_earthquake_magnitude} in {', '.join(map(str, max_earthquake_cities))}, {max_earthquake_country[0]}")
            else:
                print(f"Tie for the largest earthquake among countries: {', '.join(map(str, max_earthquake_country))} (Magnitude {max_earthquake_magnitude})")
        else:
            print(f"No recorded earthquakes found during search.")
        print(separator)

    elif user_input == '2':
        country_counts = {}  # stores count of tsunamis and the year
        max_tsunami = 0  # variable set for the largest tsunami
        max_tsunami_year = 0 #variable to store year largest tsunami occurred
        max_tsunami_year_country = [] #stores the year and tsunami size in a list incase of a tie in tsunami size
        max_tsunami_cities = [] 

        max_earthquake_magnitude = 0  # variable set to store the largest earthquake
        max_earthquake_year = 0 #stores the year of the largest earthquake
        max_earthquake_year_country = [] #stores year of the largest earthquake
        max_earthquake_cities = []
        # iterate through each row in filtered data to count tsunami and earthquake totals per country and calculate max intensity of each
        for row in filtered_data:
            try:
                country = row[4]
                tsunami_count = country_counts.get(country, 0) + 1
                country_counts[country] = tsunami_count

                # Check for the largest tsunami
                tsunami_value = float(row[7]) if row[7] != "" else 0
                if tsunami_value > max_tsunami:
                    max_tsunami = tsunami_value 
                    max_tsunami_year = int(row[0]) 
                    max_tsunami_year_country = [country]
                    max_tsunami_cities = [row[5]] 
                elif tsunami_value == max_tsunami:
                    if int(row[0]) > max_tsunami_year:
                        max_tsunami_year = int(row[0])
                        max_tsunami_year_country = [country]
                        max_tsunami_cities = [row[5]] 
                    elif int(row[0]) == max_tsunami_year:
                        max_tsunami_year_country.append(country)
                        max_tsunami_cities.append(row[5])
                # Check for the largest earthquake
                earthquake_value = float(row[6]) if row[6] != "" else 0
                if earthquake_value > max_earthquake_magnitude:
                    max_earthquake_magnitude = earthquake_value
                    max_earthquake_year = int(row[0])
                    max_earthquake_year_country = [country]
                    max_earthquake_cities = [row[5]]
                elif earthquake_value == max_earthquake_magnitude:
                    if int(row[0]) > max_earthquake_year:
                        max_earthquake_year = int(row[0])
                        max_earthquake_year_country = [country]
                        max_earthquake_cities = [row[5]]
                    elif int(row[0]) == max_earthquake_year:
                        max_earthquake_year_country.append(country)
                        max_earthquake_cities.append(row[5])
            except ValueError as e: 
                print(f"Error: {e}. Skipping row in data processing.")
            except Exception as e: 
                print(f"Unexpected error: {e}. Skipping row in data processing.")

        print("-" * 75)
        # check for multiple years being tied for tsunami amounts
        if len(max_tsunami_year_country) == 1:
            print(f"Statistics for {data_type}:")
            print(f"Largest Tsunami: {max_tsunami} meters in {', '.join(map(str, max_tsunami_cities))}, {max_tsunami_year_country[0]} in {max_tsunami_year}")
        else:
            print(f"Statistics for {data_type}:")
            print(f"Tie for the largest tsunami among years: {', '.join(map(str, max_tsunami_year_country))} ({max_tsunami} meters) during the years {max_tsunami_year}")
        if max_earthquake_magnitude > 0:
        # check for multiple years being tied for earthquake magnitudes
            if len(max_earthquake_year_country) == 1:
                print(f"Largest Earthquake: Magnitude {max_earthquake_magnitude} in {', '.join(map(str, max_earthquake_cities))}, {max_earthquake_year_country[0]} in {max_earthquake_year}")
            else:
                print(f"Tie for the largest earthquake among years: {', '.join(map(str, max_earthquake_year_country))} (Magnitude {max_earthquake_magnitude}) during the years {max_earthquake_year}")
        else:
            print(f"No recorded earthquakes found in this search.")
    #count length of filtered_data list (records found)
    total_records = len(filtered_data)
    print(f"Search results: Found {total_records} records for {data_type}.")
    #return header(output_columns) and filtered_data (data from rows that contained information from header column selected by user)
    return output_columns, filtered_data

#format month from being a number to the alphabetical abbreviation
def month_dic(month_number):
    # Create a dictionary mapping month numbers to month name, replaces month# with the name
    month_mapping = {
        '1': 'Jan',
        '2': 'Feb',
        '3': 'Mar',
        '4': 'Apr',
        '5': 'May',
        '6': 'Jun',
        '7': 'Jul',
        '8': 'Aug',
        '9': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    #return corresponding month to the number, stays the same if not found (no month) 
    return month_mapping.get(month_number, month_number)

def tsunami_cause_dict(cause_code):
    # Create a dictionary to map Tsunami Cause Codes to definitions for easier user 
    cause_map = {
        '0': '0 - Unknown',
        '1': '1 - Earthquake(EQ)',
        '2': '2 - Questionable EQ',
        '3': '3 - EQ and LS',
        '4': '4 - Volcano and EQ',
        '5': '5 - Volcano, EQ & LS',
        '6': '6 - Volcano',
        '7': '7 - Volcano and LS',
        '8': '8 - Landslide(LS)',
        '9': '9 - Meteorological',
        '10': '10 - Explosion',
        '11': '11 - Astronomical Tide'
    }
    #return corresponding number and code description, if not found, will stay empty
    return cause_map.get(cause_code, cause_code)

    #format columns and row widths for output to user
def format_output(output_columns, result):
    # combine the header and rows into a single list for formatting
    combined_list = [output_columns] + result

    # calculate the maximum width for each column depending on the max size of output from entire
    column_widths = [max(len(str(value)) for value in column) for column in zip(*combined_list)]

    #format and print the header
    header_str = "|".join(f"{column.ljust(width)}" for column, width in zip(output_columns, column_widths))

    # print separator line and dashes between header and content for the width of the columns
    separator_line = "|".join("-" * (width) for width in column_widths)
    print(separator_line)
    print(header_str)
    print(separator_line)

    #print a pipe line between each value in each row, lining up with the width of the header columns
    for row in combined_list[1:]:  #skip first row (header row)
        row[1] = month_dic(row[1]) #row index 1 is month, call on the month_dict function to replace # with string
        row[3] = tsunami_cause_dict(row[3]) #row index 3 in combined list is tsunami cause code
        row_str = "|".join(f"{str(value).ljust(width)}" for value, width in zip(row, column_widths))
        print(row_str)


This program opens and reads a small CSV file that contains tsunami and earthquake data from 1800-2021.
The user is prompted to choose "1" or "2" to search by Year(1) or Country(2). The user is then prompted to enter the specific year or country they want data for.
The data is stored into a list as unfiltered data, with certain columns in each row extracted using the indexes, and returns the data to the user as a formatted output in the terminal.
Depending on the data type chosen to search (year or country), statistics on the largest tsunami, earthquake, country, city, and year are output to the user, along with the magnitude size (earthquake),
and maximum wave height in metres (tsunami). 
If there are multiple countries or years that have an equal amount of tsunamis or earthquakes depending on their search option, the relevant countries and/or years is output to the user.
Underneath the statistics is a formatted list of all records found. The output to the user includes the year, month, day, tsunami cause code (possible cause of tsunami), country, city, earthquake magnitude and maximum tsunami height in metres.
After the program formats and outputs the information and statistics to the user, the filtered data can be saved as a new csv file.
The user has the choice to save the filtered but unformatted data as a new csv file.
Once finished, the program restarts with the prompt to search by year or country, until the user types "done".

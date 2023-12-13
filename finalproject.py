#date: dec 7 2023
#name: samantha best
#course: logic and programming
#program: data reader - final assignment

from store_functions import print_welcome, search_and_filter_user_choice, format_output
import csv
#save the filtered data in a separate list and display number of records found and summary statistics
def main():
    #path to file
    csv_file_path = ("tsunami historical data from 1800 to 2021.csv")
    #introduced program to user with types of options to choose from.
    print_welcome()
    while True:
        try:
        #prompt user and search data, return filtered results
            output_columns, result = search_and_filter_user_choice(csv_file_path)
        except FileNotFoundError:
            print("File not found. Closing program.")
            exit()

    #take output columns and results, format them with '-' and '|' lines for terminal output to user
        format_output(output_columns, result)
        record_count = len(result)
        print(f"\nTotal records found in search result: {record_count}")

        while True:
            try:
                write_new_file_choice = input("Enter 'M' to continue to Main Menu or 'S' to Save Results....\n---->('M' or 'S'): ")
                if write_new_file_choice.lower() == 'm':
                    print("\nWARNING: Your progress will NOT be saved as a new csv file.")
                    double_check = input("Enter 'Y' to confirm and start a new search, 'N' to go back to save menu....\n---->('Y' or 'N'): ")
                    if double_check.lower() == 'y':
                        break #breaks out of loop and back to line 18, prompting user to start a new search
                    elif double_check.lower() == 'n':
                        continue #continue will loop back to the user choosing Main Menu or Save Results
                    else:
                        print("Invalid selection. Please try again.")
                elif write_new_file_choice.lower() == 's':
                        output_csv_file = input("Enter name of new CSV file...\n----> ")
                        confirm_file_name = input(f"You have chosen {output_csv_file}.csv as file name.\nConfirm (Y/N): ")
                        if confirm_file_name.lower() == 'y':
                            output_path = f"{output_csv_file}.csv"
                            with open (output_path, "w", newline='') as new_file:
                                csv_writer = csv.writer(new_file)
                                csv_writer.writerow(output_columns)
                                csv_writer.writerows(result)
                            print(f"File SUCCESSFULLY saved as {output_csv_file}.")
                            break #once file is saved, breaks out of this loop and back beginning of program
                        elif confirm_file_name.lower() == 'n':
                            print(f"\n\n***File NOT saved as {output_csv_file}.csv.***\nReturning to SELECT Menu.")
                            continue #if user does not save file after confirming the file name, goes back to beginning of Main/Save input loop
                        else:
                            print("\nInvalid selection. File NOT saved. Returning to SELECT Menu.")
                elif write_new_file_choice.lower() == 'done':
                    print("Program closing.")
                    exit() #if user types 'done', closes program before restarting when prompted to choose a search method
                else:
                    print("Invalid selection. Please enter a valid choice.")
            except FileExistsError:
                print("This file already exists and will not be overwritten.")
if __name__ == "__main__":
    main()
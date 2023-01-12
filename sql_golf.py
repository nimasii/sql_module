'''
Imports for the program.
sqlite for managing the database and creating queries.
pandas, numpy, and altair to create visualizations for data.
Connects to the database and creates a global variable
'''
import sqlite3 as sql
import pandas as pd
import numpy as np
import altair as alt
database = sql.connect('golf.sqlite')
cursor = database.cursor()


'''
Main function for the program.
Connects to the database and runs a for loop that controls the program.
Disconnects from the database when finished.
'''
def main():
    # Establish a connection to the database
    print('\nWelcome to your SQL golf stats database!')

    # Main loop for the program
    quit = False
    while not quit:
        action = get_action()
        if action == '1':
            new_row()
        elif action == '2':
            basic_stats()
        elif action == '3':
            custom_stats()
        else:
            print('ERROR: Invalid input')
        
        # Let user end program if they are done
        done = input('\nWould you like to end the program? (Y/N):\n')
        done.lower()
        if done == 'n':
            quit = False
        else:
            quit = True
    
    # Ends connection to the database and closes the program
    print('\nEnding connection to database.\nHave a great day!')
    database.commit()
    cursor.close()
    database.close()
    exit()

'''
Asks the user which function of the program they would like to use.
Returns the selcted option
'''
def get_action():
    # Gets the user input of what action they would like to preform
    print('\nWhat would you like to do? (Enter # of desired action):')
    action = input('1) Add a new round to the database\n2) View some basic stats\n3) Create a query to view custom stats\n')

    # Returns the value of the selected action
    return action


'''
Asks the user for information about their round.
Creates and insert query and executes it to the table with the user input
'''
def new_row():
    # Gets user input for their round information
    score = int(input('What was your score? '))
    par = int(input('What was the par on the course? '))
    putts = int(input('How many putts did you take? '))
    penalties = int(input('How many penalty strokes did you take? '))
    gir = float(input('What percentage of greens in regulation did you hit? (50% = 50) '))
    fir = float(input('What percentage of fairways in regulation did you hit? (50% = 50) '))
    
    # Creates the insert query
    insert_query = '''INSERT INTO golf
                        (score, par, putts, penalties, gir, fir, over_under)
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?);'''
    
    # Executes the query and applies the user input
    cursor.execute(insert_query, (score, par, putts, penalties, gir, fir, (score - par)))


# TODO: Show average score, putts, penalties, gir, and fir
# TODO: Show mins and maxes for stats
def basic_stats():
    print('2')


# TODO: Allow user to create charts to view data
# TODO: Select chart type, x and y axis and any filters
def custom_stats():
    print('3')


if __name__ == '__main__':
    main()
'''
Imports for the program.
sqlite for managing the database and creating queries
pandas, numpy, and altair to create visualizations for data
Connects to the database and creates a global variable
'''
import sqlite3 as sql
import pandas as pd
import altair as alt
import webbrowser
database = sql.connect('golf.sqlite')
cursor = database.cursor()


'''
Main function for the program
Connects to the database and runs a for loop that controls the program
Disconnects from the database when finished
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
            create_graph()
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
Asks the user which function of the program they would like to use
Returns the selcted option
'''
def get_action():
    # Gets the user input of what action they would like to preform
    print('\nWhat would you like to do? (Enter # of desired action):')
    action = input('1) Add a new round to the database\n2) View some basic stats\n3) Create a graph to compare stats\n')

    # Returns the value of the selected action
    return action


'''
Runs SQL queries to get all the basic stats needed for the program
Converts those queries to pandas dataframes
Returns an array containing all of the basic stats
'''
def get_stats():
    # SQL queries for average stats
    avg_score =         '''SELECT AVG(score) AS 'Average Score'
                            FROM golf'''
    avg_putts =         '''SELECT AVG(putts) AS 'Average Putts'
                            FROM golf'''
    avg_penalties =     '''SELECT AVG(penalties) AS 'Average Penalties'
                            FROM golf'''
    avg_gir =           '''SELECT AVG(gir) AS 'Average GIR'
                            FROM golf'''
    avg_fir =           '''SELECT AVG(fir) AS 'Average FIR'
                            FROM golf'''
    avg_over_under =    '''SELECT AVG(over_under) AS 'Average Over/Under'
                            FROM golf'''

    # SQL queries for Min and Max stats
    best_score =         '''SELECT MIN(score) AS 'Low Score'
                            FROM golf'''
    best_putts =         '''SELECT MIN(putts) AS 'Low Putts'
                            FROM golf'''
    best_gir =           '''SELECT MAX(gir) AS 'High GIR'
                            FROM golf'''
    best_fir =           '''SELECT MAX(fir) AS 'High FIR'
                            FROM golf'''
    best_over_under =    '''SELECT MIN(over_under) AS 'Low Over/Under'
                            FROM golf'''

    # Converting AVG queries into dataframes
    avg_score = pd.read_sql_query(avg_score, database)
    avg_putts = pd.read_sql_query(avg_putts, database)
    avg_penalties = pd.read_sql_query(avg_penalties, database)
    avg_gir = pd.read_sql_query(avg_gir, database)
    avg_fir = pd.read_sql_query(avg_fir, database)
    avg_over_under = pd.read_sql_query(avg_over_under, database)

    # Converting MIN and MAX queries into dataframes
    best_score = pd.read_sql_query(best_score, database)
    best_putts = pd.read_sql_query(best_putts, database)
    best_gir = pd.read_sql_query(best_gir, database)
    best_fir = pd.read_sql_query(best_fir, database)
    best_over_under = pd.read_sql_query(best_over_under, database)

    # Returning array of all statistical dataframes
    return [[avg_score, avg_putts, avg_penalties, avg_gir, avg_fir, avg_over_under], [best_score, best_putts, best_gir, best_fir, best_over_under]]


'''
Asks the user for information about their round
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
    insert_query =  '''INSERT INTO golf
                        (score, par, putts, penalties, gir, fir, over_under)
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?);'''
    
    # Executes the query and applies the user input
    cursor.execute(insert_query, (score, par, putts, penalties, gir, fir, score - par))


'''
Gets array of stats from get_stats function
Prints out all average stats
Prints out all Min and Max stats
'''
def basic_stats():
    # Getting the array of stats from the function
    stats = get_stats()

    # Prints out all of the averages rounded to 2 decimal points
    print('\nYour Averages:')
    print(f'Average Score: {round(stats[0][0].loc[0][0], 2)}')
    print(f'Average Putts: {round(stats[0][1].loc[0][0], 2)}')
    print(f'Average Penalties: {round(stats[0][2].loc[0][0], 2)}')
    print(f'Average GIR: {round(stats[0][3].loc[0][0], 2)}%')
    print(f'Average FIR: {round(stats[0][4].loc[0][0], 2)}%')
    print(f'Average Over/Under: {round(stats[0][5].loc[0][0], 2)}')
   
    # Prints out all of the personal best stats
    print('\nPersonal Best:')
    print(f'Lowerst Score: {int(stats[1][0].loc[0][0])}')
    print(f'Lowerst Putts: {int(stats[1][1].loc[0][0])}')
    print(f'Highest GIR: {round(stats[1][2].loc[0][0], 2)}')
    print(f'Highest FIR: {round(stats[1][3].loc[0][0], 2)}')
    print(f'Lowerst Over/Under: {int(stats[1][4].loc[0][0])}')


'''
Lets user pick two columns from the data to compare in a scatter plot
Sets the rows based on he user input
Creates the chart, saves it, and opens it in a web browser
'''
def create_graph():
    # Gets user input for which stats they would like on each axis
    print('Which stat would you like on the X axis?')
    x = input('1) Scores\n2) Putts\n3) Penalties\n4) GIR\n5) FIR\n6) Over/Under\n')

    print('Which stat would you like on the Y axis?')
    y = input('1) Scores\n2) Putts\n3) Penalties\n4) GIR\n5) FIR\n6) Over/Under\n')

    # Sets the user input equal to the cooresponding column in the data
    if x == '1':
        x = 'score'
    elif x == '2':
        x = 'putts'
    elif x == '3':
        x = 'penalties'
    elif x == '4':
        x = 'gir'
    elif x == '5':
        x = 'fir'
    elif x == '6':
        x = 'over_under'
    else:
        print('ERROR: Invalid Input')
        main()

    if y == '1':
        y = 'score'
    elif y == '2':
        y = 'putts'
    elif y == '3':
        y = 'penalties'
    elif y == '4':
        y = 'gir'
    elif y == '5':
        y = 'fir'
    elif y == '6':
        y = 'over_under'
    else:
        print('ERROR: Invalid Input')
        main()

    # Creates and saves a scatter plot using the two selected columns
    query = '''SELECT * FROM golf'''
    chart = alt.Chart(pd.read_sql_query(query, database)).mark_point().encode(
        x=x,
        y=y
    )
    chart.save('chart.png')
    
    # Opens the chart in a web browser
    webbrowser.open('chart.png')



if __name__ == '__main__':
    main()
import time
import calendar
import pandas as pd
import numpy as np
from datetime import datetime


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#test

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze to get filters to analize.

    Args:
        a (str): input city
        b (str): input month
        c (str): input day

    Returns:
        str: filters to be used to analyze
    """
    #def filters(city)
    while True:
        city = input("What is the city that you want to analyze? ").lower()
        if city in CITY_DATA:
            break
        print("Try again - this database is only for Chicago, New York City, and Washington DC.")
     
    #def filters(month)
    calendar_month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    month = None
    while True:
        month = input("What month do you want to analyze? or type 'all' to include every month ").lower()
        if month != 'all':
            if month in calendar_month:
                break
            print("Try again - input a month name.")
        else:
            break
     
    #def filters(day)    
    day_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = None
    while True:
        day = input("Day of the week you want to analyze? or type 'all' to include the entire week ").lower()
        if day != 'all':
            if day in day_week:
                break
            print("Try again - input the weekday.")
        else:
            break
            
    return(city,month,day)

def load_data(city, month, day):   
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        a filters(city, month, day)

    Returns:
        DataFrame: loaded data based on the filters and raw data
    """
    # load data file into a dataframe
    df=pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
     # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]
    
    #prompt user if wants to see raw data. If yes print 5 lines of raw data. Continue iterating and display#
    #the next 5 lines until users says no
    show_raw_data = True  # Flag variable to track if raw data should be displayed
    while True:
        if show_raw_data:
            raw = input("Do you want to see lines of raw data? (yes/no) ").lower()
        else:
            raw = 'no'  # Skip asking for raw data if flag is False
    
        if raw == 'yes':
            # Print the first 5 lines of raw data
            for index, row in df.head().iterrows():
                print(row)
        
            # Continue iterating and display the next 5 lines until the user says no
            index = 0
            while True:
                continue_input = input('\nWould you like to see the next 5 rows of raw data? (yes/no) ').lower()
            
                if continue_input == 'yes':
                    # Print the next 5 lines of raw data
                    for index, row in df.iloc[index+1:index+6].iterrows():
                        print(row)
                elif continue_input == 'no':
                    show_raw_data = False  # Set flag to False to skip asking for raw data
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
        elif raw == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    return df

def time_stats(df):
    """
    calculates for the specified city and filters the most common hour, month, and day if applicable.

    Args:
        DataFrame: hour
        Dataframe analysis from loaded DataFrame

    Returns:
        Datetime: stats on common hour, month, day 
    """
    print('\nCalculating Time Stats...\n')
    start_time = time.time()

    if df.empty:
        print('No data available for the selected filters.')
    else:
        # extract hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour

        # find the most common hour, month, and day (from 0 to 23)
        popular_hour = df['hour'].mode()
        if len(popular_hour) > 0:
            popular_hour = popular_hour[0]
        else:
            popular_hour = None

        popular_month = df['month'].mode()
        if len(popular_month) > 0:
            popular_month = popular_month[0]
            month = calendar.month_name[popular_month]
        else:
            month = None

        popular_day = df['day'].mode()
        if len(popular_day) > 0:
            popular_day = popular_day[0]
            day = calendar.day_name[popular_day]
        else:
            day = None

        print("Most Popular Hour:", popular_hour)
        print("Most Popular Month:", month)
        print("Most Popular Day:", day)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        Df: DataFrame from filtered Df

    Returns:
        str: most popular station to start, end, and combination
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print('No data available for the selected filters.')
    else:
        # display most commonly used start station
        popular_start = df['Start Station'].mode()
        if len(popular_start) > 0:
            popular_start = popular_start[0]
        else:
            popular_start = None

        # display most commonly used end station
        popular_end = df['End Station'].mode()
        if len(popular_end) > 0:
            popular_end = popular_end[0]
        else:
            popular_end = None

        # display most frequent combination of start station and end station trip
        combine_start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()

        print('Popular Start Station:', popular_start)
        print('Popular End Station:', popular_end)
        print('Combination of Start Station and End Station:', combine_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Calculates and displays statistics on the total and average trip duration

    Args:
        Df: DataFrame from filtered Df

    Returns:
        Datetime: travel time statistics for total travel and meand travel
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Handle missing or invalid data
    df['Trip Duration'].fillna(0, inplace=True)  # Replace missing values with 0
    df['Trip Duration'] = df['Trip Duration'].astype(int)  # Convert to integer type

    # Calculate total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time/3600

    # Calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_minutes = mean_travel_time/60
    
    print("Total travel time:", total_travel_time, "-- Total travel time in hours:", total_travel_time_hours)
    print("Mean travel time:", mean_travel_time, "-- Mean travel time in minutes:", mean_travel_time_minutes)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    Calculates and displays statistics on the Bikeshare users like the type of subscriber, birthyear
    Args:
        df: DataFrame from filtered df
    Returns:
        None
    """
    print('\nCalculating User Stats on the bikeshare users...\n')
    start_time = time.time()
    
    if 'Birth Year' not in df.columns:
        print('The column "Birth Year" does not exist in the dataframe.')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
        return
    
    if df.empty or df['Birth Year'].isnull().all():
        print('No data available for the selected filters.')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
        return
    
    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    # Displays counts of gender
    gender_types = df['Gender'].value_counts()

    # Displays earliest, most recent, and most common year of birth
    sorted_bday = df['Birth Year'].dropna().sort_values()
    earliest_bday = sorted_bday.iloc[0] if len(sorted_bday) > 0 else None
    most_recent_bday = sorted_bday.iloc[-1] if len(sorted_bday) > 0 else None
    most_common_bday = df['Birth Year'].mode()[0]
    
    print(user_types, "\n")
    print(gender_types, "\n")
    print("Earliest Birthday in database: ", earliest_bday)
    print("Most Recent Birthday in database: ", most_recent_bday)
    print("Most Common Birthday: ", most_common_bday)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    
def main():
    """
    Executes the main program to analyze bikeshare information based on filters by users

    Args:
        Df: DataFrame from filtered Df and others

    Returns:
        full analysis with raw data
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
print('Hello! Let\'s explore some US bikeshare data!,\n')
if __name__ == "__main__":
	main()
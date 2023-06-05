import time
import pandas as pd
import numpy as np

filename_chicago = "chicago.csv"
filename_newyork = "new_york_city.csv"
filename_washington = "washington.csv"

CITY_DATA = { 'chicago': filename_chicago,
              'new york city': filename_newyork,
              'washington': filename_washington }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city_number =  int(input('Would you like to see the data for 1-Chicago, 2-New York City, or 3-Washington? (Please enter the number corresponding to the city of interest (1-3): '))
            if city_number > 0 and city_number <= 3:
                city = cities[city_number-1]
                break 
            else:
                print('\nThat is not a valid city option! Please try again.\n')
        except:
            print('\nThat is not a valid format for the city! Please try again.\n')
    # get user input for month (all, january, february, ... , june)
    while True:
        try:        
            month_number =  int(input('Enter the number corresponding to the month (1-6) to filter by, or 0 to apply no month filter: '))
            if month_number <= 6:
                if month_number > 0:
                    month = months[month_number -1]
                else:
                    month = 'all'
                break
            else:
                print('\nThat is not a valid month option! Please try again.\n')
        except:
            print('\nThat is not a valid format for the month! Please try again.\n')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            weekday_number =  int(input('Enter number of the weekday (1:Mon-7:Sun) to filter by, or 0 to apply no day filter: '))
            if weekday_number <= 7:
                if weekday_number > 0:
                    weekday = weekdays[weekday_number -1]
                else:
                    weekday = "all"
                break
            else:
                print('\nThat is not a valid day option! Please try again.\n')
        except:
            print('\nThat is not a valid format for the day of the week! Please try again.\n')
        
    print('-'*40)
    return city, month, weekday


def load_data(city, month, weekday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    ###Columns required: Start Time
    ###Columns created: month, day_of_week.    
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if weekday != 'all':
        # use the index of the weekdays list to get the corresponding int
        weekday = weekdays.index(weekday) + 1  
        # filter by day of week to create the new dataframe    
        df = df[df['day_of_week'] == weekday]

    return df


def time_stats(df,city,month,day):
    """
    Displays statistics on the most frequent times of travel for the specified city, month and day if applicable.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day.
             Columns required: Start Time
             Columns created: hour.
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        -
    Prints:
        most common day
        most common month
        most common start hour
    """

    full_count = df['Start Time'].count()
    print('\nCalculating The Most Frequent Times of Travel in {}...\n Filters: Month = {}, Day = {}\n Full count = {}\n'.format(city.title(), month.title(), day.title(), full_count) )
    start_time = time.time()


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month == 'all':
        # extract month from the Start Time column to create a month column
        df['month'] = df['Start Time'].dt.month
        # find the most common month (from 0 to 12)
        popular_month = df['month'].mode()[0] 
        count_popular_month = df.groupby(['month'])['month'].count()[popular_month]
        # display the most common month
        print('The most common month to travel is: {} - Count {}.'.format(months[popular_month-1].title(),count_popular_month))  
    
    if day == 'all':
        # extract day from the Start Time column to create a 'day of week' column
        df['day_of_week'] = df['Start Time'].dt.weekday
        # find the most common hour (from 1 to 7)
        popular_day = df['day_of_week'].mode()[0]
        count_popular_day = df.groupby(['day_of_week'])['day_of_week'].count()[popular_day]
        # display the most common day of week
        print('The most common day of the week to travel is: {} - Count {}.'.format( weekdays[popular_day-1].title(),count_popular_day))

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    count_popular_hour = round(df.groupby(['hour'])['hour'].count()[popular_hour],1)
    # display the most common start hour 
    print('The most common start hour to travel is: {} - Count {}.'.format(popular_hour, count_popular_hour))


    print("\nThis calculation took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*40)


def station_stats(df,city,month,day):
    """
    Displays statistics on the most popular stations and trip for the specified city, month and day if applicable.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day.
             Columns required: Start Time
             Columns created: hour.
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        -
    Prints:
        most common start station
        most common end station
        most common combinationn of start and end stations trip
    """

    full_count = df['Start Station'].count()
    print('\nCalculating The Most Popular Stations and Trip in {}...\n Filters: Month = {}, Day = {}\n Full count = {}\n'.format(city.title(), month.title(), day.title(),full_count) )
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count_popular_start_station = df.groupby(['Start Station'])['Start Station'].count()[popular_start_station]
    print('The most common start station is:', popular_start_station, '- Count: ', count_popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count_popular_end_station = df.groupby(['End Station'])['End Station'].count()[popular_end_station]
    print('The most common end station is:', popular_end_station, '- Count: ', count_popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    count_popular_trip = df.groupby(['trip'])['trip'].count()[popular_trip]
    print('The most common combination of start station and end station trip is:', popular_trip, '- Count: ', count_popular_trip)

    print("\nThis calculation took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*40)


def trip_duration_stats(df,city,month,day):
    """
    Displays statistics on the total and average trip duration for the specified city, month and day if applicable.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day.
             Columns required: Start time, End Time
             Columns created: travel time.
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        -
    Prints:
        total travel time
        mean travel time
    """

    full_count = df['Start Time'].count()
    print('\nCalculating Trip Duration in {}...\n Filters: Month = {}, Day = {}\n Full count = {}\n'.format(city.title(), month.title(), day.title(),full_count))
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['travel time'] = df['End Time'] - df['Start Time']

    # display total travel time
    total_travel_time_days, total_travel_time_seconds = df['travel time'].sum().days, df['travel time'].sum().seconds
    total_travel_time_hours = total_travel_time_seconds // 3600
    total_travel_time_mins = (total_travel_time_seconds % 3600) // 60
    total_travel_time_secs = total_travel_time_seconds %60

    print('The total travel time among users is:{} days, {} hours, {} minutes and {} seconds'.format(total_travel_time_days,total_travel_time_hours,total_travel_time_mins,total_travel_time_secs))

    # display mean travel time
    mean_travel_time_days, mean_travel_time_seconds = df['travel time'].mean().days , df['travel time'].mean().seconds
    mean_travel_time_hours = mean_travel_time_seconds // 3600
    mean_travel_time_mins = (mean_travel_time_seconds % 3600) // 60
    mean_travel_time_secs = mean_travel_time_seconds %60
    print('The mean travel time among users is: {} days, {} hours, {} minutes and {} seconds'.format(mean_travel_time_days, mean_travel_time_hours, mean_travel_time_mins, mean_travel_time_secs))

    print("\nThis calculation took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*40)


def user_stats(df,city,month,day,column_names):
    """
    Displays statistics on bikeshare users for the specified city, month and day if applicable.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day.
             Columns required: User Type, Gender and Birth Year
             Columns created: -
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        -
    Prints:
        counts of user types
        count by users
        earliest, most recent, and most common year of birth
    """

    full_count = df['User Type'].count()
    print('\nCalculating User Statistics in {}...\n Filters: Month = {}, Day = {}\nFull count = {}\n'.format(city.title(), month.title(), day.title(),full_count))
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in column_names:
        type_count = df.groupby(['User Type'])['User Type'].count()
        print('Count by users\' type:\n', type_count)
    else:
        print('\nUnfortunately the data is incomplete and the User Type stats for {} cannot be completed.\n'.format(city.title()))

    # Display counts of gender
    if 'Gender' in column_names:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print('\nCount by users\' gender:\n', gender_count)
    else:
        print('\nUnfortunately the data is incomplete and the Gender stats for {} cannot be completed.\n'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in column_names:
        earliest_year_of_birth = int(df['Birth Year'].min())
        print('\nThe earliest users\' year of birth is:', earliest_year_of_birth)
        last_year_of_birth = int(df['Birth Year'].max())
        print('The most recent users\' year of birth is:', last_year_of_birth)
        popular_year_of_birth = int(df['Birth Year'].mode()[0])
        print('The most common users\' year of birth is:', popular_year_of_birth)
    else:
        print('\nUnfortunately the data is incomplete and the Birth Year stats for {} cannot be completed.'.format(city.title()))

    print("\nThis calculation took %s seconds." % (round(time.time() - start_time,2)))
    print('-'*40)

def print_raw_data(df, city):
    df_raw = pd.read_csv(CITY_DATA[city])
    i = 0
    while True:
        raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if raw.lower() == 'no':
            break
        elif raw.lower() == 'yes':
            print(df_raw[i:i+5])
            i += 5
        else:
            print('\nThat is not a valid option! Please try again.\n')   
        
    i = 0
    while True:
        raw = input('\nWould you like to see 5 lines of filtered data? Enter yes or no.\n')
        if raw.lower() == 'no':
            break
        elif raw.lower() == 'yes':             
            print(df[i:i+5])
            i += 5
        else:
            print('\nThat is not a valid option! Please try again.\n')       


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        column_names = df.columns[1:]
        
        full_count = df['Start Time'].count()

        if full_count != 0:
            if 'Start Time' in column_names and 'End Time' in column_names:
                time_stats(df,city,month,day) #Columns required: Start Time
                trip_duration_stats(df,city,month,day) #Columns required: Start time, End Time
            else:
                print('\nUnfortunately the data is incomplete and the time stats and trip duration stats analysis cannot be completed')
            if 'Start Station' in column_names and 'End Station' in column_names:
                station_stats(df,city,month,day) #Columns required: Start Station, End Station
            else:
                print('\nUnfortunately the data is incomplete and the station stats analysis cannot be completed')
            user_stats(df,city,month,day,column_names) #Columns required: User Type, Gender and Birth Year
        else:
            print('\n There are no data of trips in {} that took place on {} - {}.\n'.format(city.title(), day.title(), month.title()))
 
        print_raw_data(df,city)   
        
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes' or restart.lower() == 'no':
                break
            else:
                print('\nThat is not a valid option! Please try again.\n')
        
        if restart.lower() == 'no':       
            break 

if __name__ == "__main__":
	main()

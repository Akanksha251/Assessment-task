#!/usr/bin/env python
# coding: utf-8

# # Question 1: Distance Matrix Calculation

# Create a function named calculate_distance_matrix that takes the dataset-3.csv as input and generates a DataFrame representing distances between IDs.
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A).

# In[2]:


import pandas as pd
import numpy as np

def calculate_distance_matrix(df):
    # Create a pivot table to get distances between toll locations
    distance_pivot = df.pivot_table(index='id_start', columns='id_end', values='distance', aggfunc=np.sum, fill_value=0)

    # Ensure the matrix is symmetric
    distance_matrix = distance_pivot + distance_pivot.T

    # Set diagonal values to 0
    np.fill_diagonal(distance_matrix.values, 0)

    # Convert the NumPy array to a DataFrame
    result_df = pd.DataFrame(distance_matrix, index=distance_matrix.index, columns=distance_matrix.columns)

    return result_df

# Load the dataset-3.csv into a DataFrame
df = pd.read_csv("C:/Users/more akanksha/Downloads/dataset-3.csv")

# Call the function and get the resulting distance matrix
result_distance_matrix = calculate_distance_matrix(df)

# Print the resulting distance matrix
print(result_distance_matrix)


# # Question 2: Unroll Distance Matrix

# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[4]:


import pandas as pd
import numpy as np

def unroll_distance_matrix(distance_matrix):
    # Reset the index to access the columns as regular columns
    distance_matrix_reset = distance_matrix.reset_index()

    # Melt the DataFrame to convert columns into rows
    melted_df = pd.melt(distance_matrix_reset, id_vars=distance_matrix_reset.columns[0], var_name='id_end', value_name='distance')

    # Rename columns to match the expected output
    melted_df = melted_df.rename(columns={distance_matrix_reset.columns[0]: 'id_start'})

    # Filter out rows where id_start is equal to id_end
    result_df = melted_df[melted_df['id_start'] != melted_df['id_end']]

    return result_df

# Assuming result_distance_matrix is the DataFrame obtained from the previous question
# Call the function and get the resulting unrolled DataFrame
result_unrolled_df = unroll_distance_matrix(result_distance_matrix)

# Print the resulting unrolled DataFrame
print(result_unrolled_df)


# # Question 3: Finding IDs within Percentage Threshold

# Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 2 and a reference value from the id_start column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[24]:


import pandas as pd
import numpy as np

# Assuming DataFrame structure similar to the result_unrolled_df from Question 2
data = {
    'id_start': [101, 102, 103, 101, 104, 102, 105],
    'id_end': [201, 202, 203, 204, 205, 206, 207],
    'distance': [15.3, 18.2, 22.5, 14.8, 19.7, 21.0, 17.3],
    'start_time': pd.to_datetime(['2023-01-01 08:30:00', '2023-01-02 12:45:00', '2023-01-03 15:20:00', '2023-01-04 09:10:00', '2023-01-05 14:30:00', '2023-01-06 11:15:00', '2023-01-07 19:45:00']),
    'end_time': pd.to_datetime(['2023-01-01 09:45:00', '2023-01-02 14:30:00', '2023-01-03 17:45:00', '2023-01-04 10:30:00', '2023-01-05 16:45:00', '2023-01-06 13:00:00', '2023-01-07 21:30:00'])
}

result_unrolled_df = pd.DataFrame(data)

def find_ids_within_ten_percentage_threshold(df, reference_value):
    # Calculate the average distance for the reference value
    reference_average = df[df['id_start'] == reference_value]['distance'].mean()

    # Calculate the threshold values (10% of the reference average)
    lower_threshold = reference_average * 0.9
    upper_threshold = reference_average * 1.1

    # Filter the DataFrame based on the threshold values
    filtered_df = df[(df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]

    # Get the sorted list of unique values from the 'id_start' column
    sorted_ids_within_threshold = sorted(filtered_df['id_start'].unique())

    return sorted_ids_within_threshold

# Choose a reference value (replace 101 with your desired reference value)
#reference_value = 101

# Call the function and get the sorted list of values within 10% threshold
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_df, reference_value)

# Print the resulting list
print(result_within_threshold)


# # Question 4: Calculate Toll Rate

# Create a function calculate_toll_rate that takes the DataFrame created in Question 2 as input and calculates toll rates based on vehicle types.
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:
# 
# 0.8 for moto
# 1.2 for car
# 1.5 for rv
# 2.2 for bus
# 3.6 for truck

# In[25]:


import pandas as pd


result_unrolled_df = pd.DataFrame(result_unrolled_df)

def calculate_toll_rate(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Add new columns for each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

# Call the function and get the resulting DataFrame with toll rates
result_with_toll_rates = calculate_toll_rate(result_unrolled_df)

# Print the resulting DataFrame
print(result_with_toll_rates)


# # Question 5: Calculate Time-Based Toll Rates

# Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day.
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# start_time and end_time must be of type datetime.time() with the values from time range given below.
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# Weekends (Saturday and Sunday):
# 
# Apply a constant discount factor of 0.7 for all times.
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[29]:


import pandas as pd
import numpy as np

# Assuming DataFrame structure similar to the result_distance_matrix from Question 3
data = {
   'id_start': [101, 102, 103, 101, 104, 102, 105],
    'id_end': [201, 202, 203, 204, 205, 206, 207],
    'distance': [15.3, 18.2, 22.5, 14.8, 19.7, 21.0, 17.3],
    'start_time': pd.to_datetime(['2023-01-01 08:30:00', '2023-01-02 12:45:00', '2023-01-03 15:20:00', '2023-01-04 09:10:00', '2023-01-05 14:30:00', '2023-01-06 11:15:00', '2023-01-07 19:45:00']),
    'end_time': pd.to_datetime(['2023-01-01 09:45:00', '2023-01-02 14:30:00', '2023-01-03 17:45:00', '2023-01-04 10:30:00', '2023-01-05 16:45:00', '2023-01-06 13:00:00', '2023-01-07 21:30:00'])
}

result_distance_matrix = pd.DataFrame(data)

def calculate_time_based_toll_rates(df):
    # Define time ranges and discount factors
    weekday_time_ranges = [(pd.to_datetime('00:00:00').time(), pd.to_datetime('10:00:00').time()),
                           (pd.to_datetime('10:00:00').time(), pd.to_datetime('18:00:00').time()),
                           (pd.to_datetime('18:00:00').time(), pd.to_datetime('23:59:59').time())]

    weekend_discount_factor = 0.7

    # Add new columns for start_day, start_time, end_day, end_time
    df['start_day'] = df['start_time'].dt.day_name()
    df['end_day'] = df['end_time'].dt.day_name()

    # Create new columns for each vehicle type
    vehicle_types = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle_type in vehicle_types:
        df[vehicle_type] = 0.0

    # Loop through each time range and apply discount factors
    for start_time, end_time in weekday_time_ranges:
        mask = (df['start_time'].dt.time >= start_time) & (df['start_time'].dt.time < end_time)
        df.loc[mask, vehicle_types] *= 0.8

        mask = (df['end_time'].dt.time >= start_time) & (df['end_time'].dt.time < end_time)
        df.loc[mask, vehicle_types] *= 0.8

    # Apply weekend discount factor
    weekend_mask = df['start_time'].dt.dayofweek >= 5
    df.loc[weekend_mask, vehicle_types] *= weekend_discount_factor

    return df

# Call the function and get the resulting DataFrame with time-based toll rates
result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_distance_matrix)

# Print the resulting DataFrame
print(result_with_time_based_toll_rates)


# In[ ]:





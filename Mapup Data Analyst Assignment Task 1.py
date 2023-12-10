#!/usr/bin/env python
# coding: utf-8

# # Question 1: Car Matrix Generation

# Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
# 
# values from id_2 as columns
# values from id_1 as index
# dataframe should have values from car column
# diagonal values should be 0.

# In[1]:


import pandas as pd

def generate_car_matrix(df):
    # Pivot the DataFrame to create a matrix
    matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    for col in matrix.columns:
        matrix.at[col, col] = 0

    return matrix

# Load the dataset-1.csv into a DataFrame
df = pd.read_csv("C:/Users/more akanksha/Downloads/dataset-1.csv")

# Call the function and get the resulting DataFrame
result_matrix = generate_car_matrix(df)

# Print the resulting matrix
print(result_matrix)


# # Question 2: Car Type Count Calculation

# Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
# 
# low for values less than or equal to 15,
# medium for values greater than 15 and less than or equal to 25,
# high for values greater than 25.
# Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.
# 
# 

# In[2]:


import pandas as pd

def get_type_count(df):
    # Add a new categorical column 'car_type' based on values of the 'car' column
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]

    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=choices, right=False)

    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))

    return type_counts

# Load the dataset-1.csv into a DataFrame
df = pd.read_csv("C:/Users/more akanksha/Downloads/dataset-1.csv")

# Call the function and get the resulting dictionary
result_dict = get_type_count(df)

# Print the resulting dictionary
print(result_dict)


# # Question 3: Bus Count Index Retrieval

# Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.

# In[3]:


import pandas as pd

def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where the 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Load the dataset-1.csv into a DataFrame
df = pd.read_csv("C:/Users/more akanksha/Downloads/dataset-1.csv")

# Call the function and get the resulting list of indices
result_indexes = get_bus_indexes(df)

# Print the resulting list of indices
print(result_indexes)


# # Question 4: Route Filtering

# Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

# In[4]:


import pandas as pd

def filter_routes(df):
    # Group by 'route' and calculate the average of the 'truck' column
    avg_truck_by_route = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column is greater than 7
    selected_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

# Load the dataset-1.csv into a DataFrame
df = pd.read_csv("C:/Users/more akanksha/Downloads/dataset-1.csv")

# Call the function and get the resulting sorted list of routes
result_routes = filter_routes(df)

# Print the resulting list of routes
print(result_routes)


# # Question 5: Matrix Value Modification

# Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# 
# If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# If a value is 20 or less, multiply those values by 1.25.
# The function should return the modified DataFrame which has values rounded to 1 decimal place.

# In[6]:


import pandas as pd

def multiply_matrix(matrix_df):
    # Apply the specified logic to modify values in the DataFrame
    modified_df = matrix_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df

# Assuming `result_matrix` is the DataFrame obtained from generate_car_matrix
# You can call the function like this:
result_matrix = generate_car_matrix(df)  # Make sure to generate the matrix first
modified_matrix = multiply_matrix(result_matrix)
print(modified_matrix)


# # Question 6: Time Check

# You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[8]:


import pandas as pd
from datetime import datetime, timedelta

def verify_time_completeness(df):
    # Combine date and time columns to create datetime objects
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Create a boolean mask for each condition
    full_24_hour_mask = (df['end_datetime'] - df['start_datetime']) == timedelta(days=1)
    spans_7_days_mask = (df['start_datetime'].dt.dayofweek.min() == 0) and                         (df['end_datetime'].dt.dayofweek.max() == 6)

    # Apply the conditions to the DataFrame and create a boolean series
    result_series = df.groupby(['id', 'id_2']).apply(
        lambda x: full_24_hour_mask[x.index] and spans_7_days_mask[x.index].all()
    )

    return result_series

# Load the dataset-2.csv into a DataFrame
df = pd.read_csv("C:/Users/more akanksha/Downloads/dataset-2.csv")

# Call the function and get the resulting boolean series
result_boolean_series = verify_time_completeness(df)

# Print the resulting boolean series
print(result_boolean_series)


# In[ ]:





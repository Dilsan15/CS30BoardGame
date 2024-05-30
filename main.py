import os
import warnings
import pandas as pd
from datetime import datetime

grade_map = {'A+': 15, 'A': 14, 'A-': 13, 'B+': 12, 'B': 11, 'B-': 10,
             'C+': 9, 'C': 8, 'C-': 7, 'D+': 6, 'D': 5, 'D-': 4, 'F+': 3, 'F': 2, 'F-': 1}

# Output ----------------------------------------------------------------------

# Function to save the DataFrame to a CSV file with a unique timestamp in the filename
def save_csv(df):
    df = df.replace({'%': '', '#': '', ',': '', '\$': ''}, regex=True)
    df = df.replace(grade_map, regex=True)
    df = df.astype({
        # List of columns and data types repeated from earlier conversion
    })
    dt_string = datetime.now().strftime("%d%m%H%M")
    df.to_csv(f"data/sorted_data{dt_string}.csv", index=False)
    print("Data has been saved to a CSV file.")

# Processing -------------------------------------------------------------
# Binary search function for numerical columns
def num_binary_search(df, target, col):
    df = df.sort_values(by=col)
    target = int(target)
    left = 0
    right = len(df) - 1
    while left <= right:
        mid = left + (right - left) // 2
        mid_val = df.iloc[mid][col]
        if mid_val == target:
            return df.iloc[mid]
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Recursive quick sort function
def quick_sort(df, col):
    if len(df) <= 1:
        return df
    else:
        pivot = df[col].iloc[len(df) // 2]
        left = df[df[col] < pivot]
        middle = df[df[col] == pivot]
        right = df[df[col] > pivot]
        return pd.concat([quick_sort(left, col), middle, quick_sort(right, col)], axis=0)

# Iterative selection sort function
def selection_sort(df, col):
    for i in range(len(df)):
        min_idx = i
        for j in range(i + 1, len(df)):
            if df[col].iloc[min_idx] > df[col].iloc[j]:
                min_idx = j
        df.iloc[i], df.iloc[min_idx] = df.iloc[min_idx], df.iloc[i]
    return df

# Recursive merge sort function
def merge_sort(df, col):
    if len(df) <= 1:
        return df
    else:
        mid = len(df) // 2
        left = merge_sort(df[:mid], col)
        right = merge_sort(df[mid:], col)
        return merge(left, right, col)

# Helper function to merge two sorted halves
def merge(left, right, col):
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left
    if left[col].iloc[0] < right[col].iloc[0]:
        return pd.concat([left.iloc[:1], merge(left.iloc[1:], right, col)], axis=0)
    return pd.concat([right.iloc[:1], merge(left, right.iloc[1:], col)], axis=0)



if __name__ == "__main__":

    # INPUT -------------------------------------------------------------------------------

    # Load the neighborhood data from a CSV file into a pandas DataFrame
    raw_neigh_df = pd.read_csv("data/neigh_data_Feb15_2023.csv")

    # Set pandas options to not silently downcast data types
    pd.set_option('future.no_silent_downcasting', True)

    # Suppress future warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Clean the DataFrame by removing rows with NaN values and duplicates
    clean_neigh_df = raw_neigh_df.dropna().drop_duplicates()

    # Create a copy of the cleaned DataFrame to apply transformations
    coded_neigh_df = clean_neigh_df.copy()

    # Remove percentage signs, hash symbols, commas, and dollar signs from all string fields
    coded_neigh_df.replace({'%': '', '#': '', ',': '', '\$': ''}, regex=True, inplace=True)

    # Filter out rows where any column has zero values
    coded_neigh_df = coded_neigh_df[(clean_neigh_df != 0).all(1)]

    # Define a mapping from letter grades to numerical scores

    # Apply grade mapping to the DataFrame
    coded_neigh_df.replace(grade_map, regex=True, inplace=True)

    # Convert data types for specific columns to integer or float as required
    coded_neigh_df = coded_neigh_df.astype({
        "total_liv_score": "int64", "edmonton_rank": "int64",
        "alberta_rank": "int64", "percent_rank": "int64", "ammenities_grade": "int64",
        "cost_of_living_percent": "int64", "crime_rate": "int64",
        "median_income": "int64",
        "in_labor_force": "int64", "unemployment_rate": "int64",
        "median_house_val": "int64",
        "home_owner_percent": "int64", "high_school_percent": "int64",
        "bach_degree": "int64",
        "test_scores": "int64", "area_pop": "int64", "pop_dense": "int64",
        "med_age": "int64",
        "marri_coup": "int64", "fam_w_kids": "int64", "eng_only": "float",
        "french_only": "float"})


    # Main program starts here: prompt user for action
    print("\nWelcome to the Edmonton Neighborhoods Data Sorting/Searching Program")
    print("The following columns are available for sorting: \n")

    # Print available columns for user reference
    for col in clean_neigh_df.columns:
        print(f"{col} ({clean_neigh_df[col].dtype})")

    print("\n*Please do not use any sort algo non-quantitative data types*")


    # PROCESSING --------------------------------------------------------------------

    while True:
        user_choice = input("Would you like to sort or search the data? (sort/search/print/exit): ")
        input_df = coded_neigh_df.copy()

        if user_choice == "sort":
            sort_choice = input("Enter the column name you would like to sort by: ")
            sort_type = input("Enter the sorting algorithm you would like to use (quick/merge/selection): ")

            # Process sorting based on user-selected algorithm and column
            if sort_type == "quick":
                sorted_df = quick_sort(input_df, sort_choice)
            elif sort_type == "merge":
                sorted_df = merge_sort(input_df, sort_choice)
            elif sort_type == "selection":
                sorted_df = selection_sort(input_df, sort_choice)
            else:
                print("Invalid sorting algorithm choice. Please try again.")
                continue

            print(f"Data has been sorted by {sort_choice} using the {sort_type} sort algorithm. It has now been saved to a CSV file.")
            save_csv(sorted_df)

        elif user_choice == "search":
            # Process search based on user input
            found_search_df = pd.DataFrame(columns=clean_neigh_df.columns)
            search_choice = input("Enter the column name you would like to search by: ")
            search_target = input("Enter the target value you would like to search for: ")

            if search_choice == "neigh_name":
                for val in coded_neigh_df["neigh_name"]:
                    if val == search_target:
                        found_search_df = coded_neigh_df.loc[input_df["neigh_name"] == search_target]
                        save_csv(found_search_df)
                        print(f"Data has been searched by neigh_name for the value {search_target}. The results have been saved to a CSV file.")
            else:
                while True:
                    search_value = num_binary_search(input_df, search_target, search_choice)
                    if type(search_value) == int:
                        dt_string = datetime.now().strftime("%d%m%Y%H%M")
                        if len(found_search_df) > 0:
                            print(f"Data has been searched by {search_choice} for the value {search_target}. The results have been saved to a CSV file.")
                            save_csv(found_search_df)
                            break
                        print("No more results found.")
                    else:
                        found_search_df = found_search_df._append(search_value)
                        input_df.drop(search_value.name, inplace=True)

        elif user_choice == "print":
            all_files = []

            # Collect all CSV files from the specified directories

            all_files.extend([os.path.join("data", f) for f in os.listdir("data") if f.endswith(".csv")])

            if not all_files:
                print("No CSV files available for printing. Please choose another option")
                continue


            print("The following CSV files are available for printing:\n")
            for idx, file in enumerate(all_files, 1):
                print(str(idx) + "." + file.split('\\')[-1])

            file_index = int(input("Enter the number of the file you wish to print: ")) - 1
            p_df = pd.read_csv(all_files[file_index])

            print("\n")
            print(
                f"{'Neighborhood Name':50}",
                f"{'Total Living Score':35}",
                f"{'Edmonton Rank':25}",
                f"{'Alberta Rank':25}",
                f"{'Percent Rank':30}",
                f"{'Amenities Grade':25}",
                f"{'Cost of Living Percent':35}",
                f"{'Crime Rate':20}",
                f"{'Median Income':30}",
                f"{'In Labor Force':25}",
                f"{'Unemployment Rate':30}",
                f"{'Median House Value':30}",
                f"{'Homeowner Percent':30}",
                f"{'High School Grad Percent':35}",
                f"{'Bachelor Degree':25}",
                f"{'Test Scores':25}",
                f"{'Area Population':25}",
                f"{'Population Density':25}",
                f"{'Median Age':20}",
                f"{'Married Couples':25}",
                f"{'Families with Kids':25}",
                f"{'English Only Speakers':25}",
                f"{'French Only Speakers':25}"
            )

            # OUTPUT -----------------------------------------------------------------------------
            for index, row in p_df.iterrows():
                print(
                    f"{row['neigh_name']:30}",
                    f"{row['total_liv_score']:30}",
                    f"{row['edmonton_rank']:30}",
                    f"{row['alberta_rank']:25}",
                    f"{row['percent_rank']:25}",
                    f"{row['ammenities_grade']:30}",
                    f"{row['cost_of_living_percent']:35}",
                    f"{row['crime_rate']:25}",
                    f"{row['median_income']:30}",
                    f"{row['in_labor_force']:25}",
                    f"{row['unemployment_rate']:30}",
                    f"{row['median_house_val']:30}",
                    f"{row['home_owner_percent']:30}",
                    f"{row['high_school_percent']:35}",
                    f"{row['bach_degree']:25}",
                    f"{row['test_scores']:25}",
                    f"{row['area_pop']:25}",
                    f"{row['pop_dense']:25}",
                    f"{row['med_age']:20}",
                    f"{row['marri_coup']:25}",
                    f"{row['fam_w_kids']:25}",
                    f"{row['eng_only']:25}",
                    f"{row['french_only']:25}"
                )

        elif user_choice == "exit":
            print("\nThank you for using the Edmonton Neighborhoods Data Sorting/Searching Program. Goodbye.")
            break

        else:
            print("Invalid choice. Please try again.")

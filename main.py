import warnings

import pandas as pd
from datetime import datetime

raw_neigh_df = pd.read_csv("data/neigh_data_Feb15_2023.csv")
pd.set_option('future.no_silent_downcasting', True)
warnings.simplefilter(action='ignore', category=FutureWarning)

clean_neigh_df = raw_neigh_df.dropna().drop_duplicates()

coded_neigh_df = clean_neigh_df.copy()
coded_neigh_df.replace({'%': '', '#': '', ',': '', '\$': ''}, regex=True, inplace=True)

coded_neigh_df = coded_neigh_df[(clean_neigh_df != 0).all(1)]

grade_map = {'A+': 15, 'A': 14, 'A-': 13, 'B+': 12, 'B': 11, 'B-': 10,
             'C+': 9, 'C': 8, 'C-': 7, 'D+': 6, 'D': 5, 'D-': 4, 'F+': 3, 'F': 2, 'F-': 1}
coded_neigh_df.replace(grade_map, regex=True, inplace=True)

# convert data to associated data types
coded_neigh_df = coded_neigh_df.astype({"total_liv_score": "int64", "edmonton_rank": "int64",
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


def save_csv(df):
    df = df.replace({'%': '', '#': '', ',': '', '\$': ''}, regex=True)

    df = df.replace(grade_map, regex=True)

    df = df.astype({"total_liv_score": "int64", "edmonton_rank": "int64",
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

    dt_string = datetime.now().strftime("%d%m%H%M")
    df.to_csv(f"data/sorted_data{dt_string}.csv", index=False)
    print("Data has been saved to a CSV file.")


# worst time complexity: O(log n)
# worst space complexity: O(1)
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


# worst time complexity: O(n^2)
# worst space complexity: O(log n)
# can be made better if you dont use recursion
def quick_sort(df, col):
    if len(df) <= 1:
        return df
    else:
        pivot = df[col].iloc[len(df) // 2]
        left = df[df[col] < pivot]
        middle = df[df[col] == pivot]
        right = df[df[col] > pivot]
        return pd.concat([quick_sort(left, col), middle, quick_sort(right, col)], axis=0)


# worst time complexity: O(n^2)
# worst space complexity: O(1)
def selection_sort(df, col):
    for i in range(len(df)):
        min_idx = i
        for j in range(i + 1, len(df)):
            if df[col].iloc[min_idx] > df[col].iloc[j]:
                min_idx = j
        df.iloc[i], df.iloc[min_idx] = df.iloc[min_idx], df.iloc[i]
    return df


# worst time complexity: O(n log n)
# worst space complexity: O(n)
def merge_sort(df, col):
    if len(df) <= 1:
        return df
    else:
        mid = len(df) // 2
        left = merge_sort(df[:mid], col)
        right = merge_sort(df[mid:], col)
        return merge(left, right, col)


def merge(left, right, col):
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left
    if left[col].iloc[0] < right[col].iloc[0]:
        return pd.concat([left.iloc[:1], merge(left.iloc[1:], right, col)], axis=0)
    return pd.concat([right.iloc[:1], merge(left, right.iloc[1:], col)], axis=0)


print("\nWelcome to the Edmonton Neighborhoods Data Sorting/Searching Program")
print("The following columns are available for sorting: \n")

for col in clean_neigh_df.columns:
    print(f"{col} ({clean_neigh_df[col].dtype})")

print("\n*Please do not use any sort algo non-quantitative data types*")
while True:
    user_choice = input("Would you like to sort or search the data? (sort/search/exit): ")

    input_df = coded_neigh_df.copy()

    if user_choice == "sort":
        sort_choice = input("Enter the column name you would like to sort by: ")
        sort_type = input("Enter the sorting algorithm you would like to use (quick/merge/selection): ")

        if sort_type == "quick":
            sorted_df = quick_sort(input_df, sort_choice)
        elif sort_type == "merge":
            sorted_df = merge_sort(input_df, sort_choice)
        elif sort_type == "selection":
            sorted_df = selection_sort(input_df, sort_choice)
        else:
            print("Invalid sorting algorithm choice. Please try again.")
            continue

        print(
            f"Data has been sorted by {sort_choice} using the {sort_type} sort algorithm. It has now been saved to a CSV file.")

        save_csv(sorted_df)

    elif user_choice == "search":
        found_search_df = pd.DataFrame(columns=clean_neigh_df.columns)
        search_choice = input("Enter the column name you would like to search by: ")
        search_target = input("Enter the target value you would like to search for: ")

        if search_choice == "neigh_name":
            for val in coded_neigh_df["neigh_name"]:
                if val == search_target:
                    found_search_df = coded_neigh_df.loc[input_df["neigh_name"] == search_target]
                    save_csv(found_search_df)
                    print(
                        "Data has been searched by neigh_name for the value {search_target}. The results have been saved to a CSV file.")
        else:
            while True:

                search_value = num_binary_search(input_df, search_target, search_choice)

                if type(search_value) == int:

                    dt_string = datetime.now().strftime("%d%m%Y%H%M")
                    if len(found_search_df) > 0:
                        print(
                            f"Data has been searched by {search_choice} for the value {search_target}. The results have been saved to a CSV file.")
                        save_csv(found_search_df)
                        break
                    print("No more results found.")


                else:
                    found_search_df = found_search_df._append(search_value)
                    input_df.drop(search_value.name, inplace=True)

    elif user_choice == "exit":
        print("\nThank you for using the Edmonton Neighborhoods Data Sorting/Searching Program. Goodbye.")
        break

    else:
        print("Invalid choice. Please try again.")

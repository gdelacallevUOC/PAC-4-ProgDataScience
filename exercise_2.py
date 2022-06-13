"""Module with all the functions in Exercise 2.

The functions allow us to obtain certain basic statistics of the set of players.
"""

import pandas as pd
import numpy as np
from exercise_1 import join_datasets_year


def find_max_col(df_data: pd.DataFrame, filter_col: str, cols_to_return: list) -> pd.DataFrame:
    """It receives a dataframe and, given the name of a numeric column, returns the
       row/s in which its value is maximum. In addition, the function will receive as
       argument a list of column names that are the ones that the dataframe returned by
       the function must contain.

    Args:
            df_data: dataframe containing the data.
            filter_col: name of the column for which we want to know the maximum.
            cols_to_return: list of columns to return.

    Returns:
            A dataframe in which the column value is maximum.
    """
    max_value = df_data[filter_col].max()
    return df_data.loc[df_data[filter_col] == max_value, cols_to_return]


def find_rows_query(df_data: pd.DataFrame, query: tuple,
                    cols_to_return: list) -> pd.DataFrame:
    """Filters the data with advanced filters. The function receives a query in
       the form of a tuple. The first element of the tuple will be a list of
       columns on which we want to filter. The second element will be the list
       of values we want to use in the filter.

    Args:
            df_data: dataframe containing the data.
            query: tuple containing the query.
            cols_to_return: list of columns to return.

    Returns:
            A dataframe in which the filtered data.
    """
    df_filtered = df_data
    i = 0
    number_types = df_filtered.select_dtypes(include=np.number).columns.tolist()
    for filter_column in query[0]:
        if filter_column in number_types:
            df_filtered = df_filtered.loc[df_filtered[filter_column].
                                    between(query[1][i][0], query[1][i][1])]
        else:
            df_filtered = df_filtered.loc[df_filtered[filter_column] ==
                                          query[1][i]]
        i = i + 1
    return df_filtered[cols_to_return]


def exercise_2c_main() -> None:
    """Displays the short_name, year, age, overall and potential of:
    - Players of Belgian nationality under 25 years of age are the maximum
    potential in men's soccer.
    - Goalkeepers over 28 years of age wth overall greater than 85 in women's
    soccer.
    """
    print("EXERCICI 2C")
    data = join_datasets_year("data", [2016 + i for i in range(7)])
    cols_to_return = ["short_name", "year", "age", "overall", "potential"]
    # Male players
    c_filter = ["nationality_name", "age", "gender"]
    v_filter = ["Belgium", (0, 24), "M"]  # Menors de 25 anys -> No inclou 25
    male_belgium = find_rows_query(data, (c_filter, v_filter), cols_to_return)
    male_belgium_pot = find_max_col(male_belgium, "potential", cols_to_return)
    print("Jugadors de nacionalitat belga menors de 25 anys màxim potential:")
    print(male_belgium_pot)
    # Female players
    c_filter = ["age", "overall", "player_positions", "gender"]
    v_filter = [(29, 100), (86, 100), "GK", "F"]
    female_gk = find_rows_query(data, (c_filter, v_filter), cols_to_return)
    print("Porteres majors de 28 anys amb overall superior a 85:")
    print(female_gk)

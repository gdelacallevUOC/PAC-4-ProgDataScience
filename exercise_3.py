"""Module with all the functions in Exercise 3.

This package will make it possible to study the body mass index (BMI)
of professional athletes.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from exercise_1 import read_add_year_gender
from exercise_2 import find_max_col


def calculate_bmi(df_data: pd.DataFrame, gender: str, year: int,
                  cols_to_return: list) -> pd.DataFrame:
    """Given a dataframe with the data, a gender and a year, return a dataframe
       that includes a column with the body mass index (BMI) for each soccer
       player of that gender and year. The BMI is calculated as:
                          BMI = weight/(height * height)

    Args:
            df_data: dataframe containing the data.
            gender: gender we want to study.
            year: year we want to study in XXXX format (e.g. 2020).
            cols_to_return: list of columns to return (without BMI column).

    Returns:
            Returns a dataframe that includes a column with the body mass index
            (BMI) of each player of a given gender and year. It contains a
            number of columns that are specified, in addition to the new BMI
            column.
    """
    df_data = df_data[df_data["gender"] == gender]
    df_data = df_data[df_data["year"] == year]
    df_data["BMI"] = df_data.weight_kg / ((df_data.height_cm / 100) *
                                          (df_data.height_cm / 100))
    cols_to_return.append("BMI")
    return df_data[cols_to_return]


def exercise_3a_main() -> None:
    """It shows a bar chart with the maximum BMI per country filtered
    by male gender and year 2022.
    """
    print("EXERCICI 3A")
    data = read_add_year_gender("data/players_22.csv", "M", 2022)
    cols_to_return = ["club_flag_url"]
    data_bmi = calculate_bmi(data, "M", 2022, cols_to_return).dropna()
    data_bmi = data_bmi.astype({"club_flag_url": str})

    # Obtain all the countries
    countries_web = data_bmi["club_flag_url"].unique()
    countries = [webp[29:-4] for webp in countries_web]

    # We draw a bar chart
    # We declare values for the y-axis
    values_bmi = []
    for country in countries_web:
        max_bmi = find_max_col(data_bmi[data_bmi["club_flag_url"] == country],
                               "BMI", "BMI").unique()
        values_bmi.extend(list(max_bmi))
    # We create graphics
    plt.bar(countries, values_bmi)
    plt.ylabel("Maximum BMI")
    plt.xlabel("Country")
    plt.title("Maximum BMI per country by male gender and year 2022")
    plt.show()
    print("Gràfic realitzat")


def exercise_3b_main() -> None:
    """It shows a grouped bar chart with the percentage of men aged
    18-34 compared to soccer players in 2020, in each category of BMI.
    """
    print("EXERCICI 3B")
    data = read_add_year_gender("data/players_20.csv", "M", 2020)
    cols_to_return = ["club_flag_url"]
    data_bmi = calculate_bmi(data, "M", 2020, cols_to_return)
    data_bmi = data_bmi.astype({"club_flag_url": str})

    # Obtain players that play in Spain
    flag_url = "https://cdn.sofifa.net/flags/es.png"
    data_bmi = data_bmi[data_bmi["club_flag_url"] == flag_url]
    # Obtain the proportion of each category
    total_players = data_bmi.shape[0]
    players_under = data_bmi[data_bmi["BMI"] < 18.5].shape[0]
    serie_players = [(players_under)/(total_players)*100]
    players_normal = data_bmi[(18.5 <= data_bmi["BMI"]) &
                              (data_bmi["BMI"] < 25)].shape[0]
    serie_players.append((players_normal)/(total_players)*100)
    players_over = data_bmi[(25 <= data_bmi["BMI"]) &
                            (data_bmi["BMI"] < 30)].shape[0]
    serie_players.append((players_over)/(total_players)*100)
    players_obes = data_bmi[data_bmi["BMI"] >= 30].shape[0]
    serie_players.append((players_obes)/(total_players)*100)

    # Proportion of poblation (IME)
    serie_poblation = [2, 59.58, 30.83, 7.59]

    # We draw a bar chart
    bars_index = np.arange(4)
    plt.bar(bars_index, serie_players, width=0.35, label='Football players')
    plt.bar(bars_index + 0.35, serie_poblation, width=0.35,
            label='Male population')
    plt.legend(loc='best')
    plt.xticks(bars_index + 0.175, ('underweight', 'normal weight',
               'overweight', 'obese'))
    plt.ylabel('Proportion of each category')
    plt.xlabel('Category of BMI')
    plt.title('Proportion of BMI')
    plt.show()
    print("Gràfic realitzat")

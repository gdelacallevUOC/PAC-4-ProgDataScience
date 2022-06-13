"""Module with all the functions in Exercise 5.

The functions will be used to study the evolution of some
characteristcs of the players.
"""

from statistics import mean
import math
import matplotlib.pyplot as plt
from exercise_1 import join_datasets_year
from exercise_4 import players_dict, clean_up_players_dict


def top_average_column(data: dict, identifier: str, col: str, threshold: int) -> list:
    """Returns a list of tuples where the average value of a
    given characteristic col is calculated for each sofifa_id if we
    have information of threshold or more years. If not, that sofifa_id
    is ignored.

    Args:
            data: dictionary containing the information of several sofifa_id.
            identifier: column/key to be used as identifier.
            col: name of a numeric column/key.
            threshold: minimum number of data required.

    Returns:
            list of tuples consisting of three elements: value of the identifier
            column; average of the characteristic; and a dictionary composed of
            the key year containing the list of years corresponding to the values
            and the key value with these values. It is sorted in descending
            order according to the calculated average.
    """
    list_tuples = []
    for player_id in data.values():
        if len(player_id["year"]) >= threshold:
            if not any(math.isnan(x) for x in player_id[col]):
                mean_col = mean(player_id[col])
                list_tuples.append((player_id[identifier], mean_col,
                                   {"value": player_id[col], "year": player_id["year"]}))
    list_tuples.sort(key=lambda y: y[1], reverse=True)
    return list_tuples


def exercise_5b_main() -> None:
    """Considering the dataframe with both genders and the years 2016,
    2017 and 2018, it shows per screen:
        - The dictionary built with the function of section 4a with
          the information of columns [short_name, overall, potential,
          player_positions, year] and ids=[226328, 192476, 230566].
        - The query that would be passed to the function in section 4b
          to clean this dictionary.
        - The dictionary with all the redundant information eliminated.
    """
    print("EXERCICI 5B")
    data = join_datasets_year("data", [2016, 2017, 2018, 2019, 2020, 2021, 2022])
    columns_of_interest = ["short_name", "movement_sprint_speed", "gender", "year"]
    col_query = [("short_name", "one"), ("gender", "one")]
    data_dict = players_dict(data,
                             list(data["sofifa_id"].unique()),
                             columns_of_interest)
    data_dict = clean_up_players_dict(data_dict, col_query)
    top_movement = top_average_column(data_dict, "short_name", "movement_sprint_speed", 2)
    top_movement = top_movement[:4]
    print("4 futbolistes amb millor mitjana de movement_sprint_speed:")
    print(top_movement)

    # Graph
    for elem in top_movement:
        x_values = elem[2]['year']
        y_values = elem[2]['value']
        plt.plot(x_values, y_values, label = elem[0])
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("Movement_sprint_speed")
    plt.show()
    print("Gràfic realitzat")

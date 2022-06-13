"""Module with all the functions in Exercise 4.

The functions will be used to track the evolution of players
appearing in different years in our dataset.
"""

from pprint import pprint
import sys
import pandas as pd

from exercise_1 import join_datasets_year


def players_dict(df_data: pd.DataFrame, ids: list, cols: list) -> dict:
    """Given a dataframe with the data, a list of identifiers and a list
       of columns returns a dictionary.

    Args:
            df_data: dataframe containing the data.
            ids: list of identifiers sofifa_id
            cols: list of columns for which we want information

    Returns:
            dictionary
               - that has as keys the identifiers sofifa_id contained in the
                 list ids.
               - that has as values dictionaries with the information
                 corresponding to each player. Specifically, the keys of each
                 of these dictionaries will be the names of the columns
                 included in col and their values will be the information of all
                 the years available in the dataframe for each player.
    """
    dict_data = {i: {column: list(df_data[df_data["sofifa_id"] == i][column]) for
                     column in cols} for i in ids}
    return dict_data


def clean_up_players_dict(player_dict: dict, col_query: list) -> dict:
    """Eliminates redundant information from a dictionary.

    Args:
            player_dict: dictionary in the format of (a) players_dict
            col_query: list of tuples with details about the information
                       to be simplified.

    Returns:
            dictionary with the redundant information eliminated.
    """
    for query in col_query:
        if query[1] == "one":
            for id_player in player_dict:
                player_dict[id_player][query[0]] = player_dict[id_player][query[0]][0]
        elif query[1] == "del_rep":
            for id_player in player_dict:
                # If a list is not a string, we convert
                converted_list = [str(element) for element in player_dict[id_player][query[0]]]
                text = ", ".join(converted_list)
                list_del_rep = list(set(text.split(", ")))
                player_dict[id_player][query[0]] = list_del_rep
        else:
            sys.exit("The query hs to be one or del_rep")
    return player_dict


def exercise_4c_main() -> None:
    """Considering the dataframe with both genders and the years 2016,
    2017 and 2018, it shows per screen:
        - The dictionary built with the function of section 4a with
          the information of columns [short_name, overall, potential,
          player_positions, year] and ids=[226328, 192476, 230566].
        - The query that would be passed to the function in section 4b
          to clean this dictionary.
        - The dictionary with all the redundant information eliminated.
    """
    print("EXERCICI 4C")
    df_data = join_datasets_year("data", [2016, 2017, 2018])
    cols = ["short_name", "overall", "potential", "player_positions", "year"]
    ids = [226328, 192476, 230566]
    dict_players = players_dict(df_data, ids, cols)
    print("Diccionari:")
    pprint(dict_players)
    col_query = [("short_name", "one"), ("player_positions", "del_rep")]
    print("Query:")
    print(col_query)
    dict_eli = clean_up_players_dict(dict_players, col_query)
    print("Diccionari net:")
    pprint(dict_eli)

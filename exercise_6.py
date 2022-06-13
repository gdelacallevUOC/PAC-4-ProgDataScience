"""Module with all the functions in Exercise 6.

The functions will be used to choose the best defenders
of the world.
"""

from itertools import product
import pandas as pd
from exercise_1 import join_male_female


def players_best_position(df_data: pd.DataFrame) -> dict:
    """Returns a dictionary composed of the key position containing the list
       of 10 best players in this position.

    Args:
            df_data: dataframe containing all the data.

    Returns:
            dictionary composed of the key position containing the list of
            10 best players in each position
    """
    position_players = {}
    cb_players = df_data[df_data["player_positions"].str.contains("CB")]["sofifa_id"][:20]
    position_players["CB"] = list(cb_players)
    rb_players = df_data[df_data["player_positions"].str.contains("RB")]["sofifa_id"][:10]
    position_players["RB"] = list(rb_players)
    lb_players = df_data[df_data["player_positions"].str.contains("LB")]["sofifa_id"][:10]
    position_players["LB"] = list(lb_players)
    return position_players


def qualities_players_position(df_data: pd.DataFrame, identifier: str, qualities: list) -> dict:
    """Returns a dictionary composed of the key identifier of a player
    and a list including the qualities and the sum of the qualities.

    Args:
            df_data: dataframe containing all the data.
            identifier: column/key to be used as identifier.
            qualities: list of strings with the 5 qualities that we want to
                       consider

    Returns:
            dictionary composed of the key identifier and with values the qualities
            and sums of different qualities to make a study
    """
    qualities_players = {}
    for ind in df_data.index:
        qual_1 = int(df_data[qualities[0]][ind])
        qual_2 = int(df_data[qualities[1]][ind])
        qual_3 = int(df_data[qualities[2]][ind])
        qual_4 = int(df_data[qualities[3]][ind])
        qual_5 = int(df_data[qualities[4]][ind])
        qualities_players[df_data[identifier][ind]] = [qual_1, qual_2, qual_3, qual_4, qual_5,
                                                  qual_1+qual_2+qual_3+qual_4+qual_5,
                                                  qual_1+qual_2+qual_3, qual_4, qual_5]
    return qualities_players


def order_combinations(combinations: list) -> list:
    """Returns a list of combinations of 4 players ordered by the sum of
    all the qualities considered.

    Args:
            combinations: list of dictionaries containing a combination of
                          4 players.

    Returns:
            list of dictionaries ordered.
    """
    for elem in combinations:
        elem["SUM"] = 0
        for item in elem.items():
            if item[0] != "SUM":
                elem["SUM"] = elem["SUM"] + item[1][5]
    sorted(combinations, key=lambda x: x["SUM"], reverse=True)
    return combinations


def print_combinations(combinations: list, number: int) -> None:
    """Displays by screen the number best lineups along with their
    contributions to offense, possession and defense based on the
    criteria used.

    Args:
            combinations: list of dictionaries ordered containing a
                          combination of 4 players.
            number: number of lineups that we have to display.
    """
    for elem in range(number):
        print(f"ALINEACIÓ {elem+1}:")
        list_players = list(combinations[elem].keys())
        print(f"CB 1: {list_players[0]}")
        print(f"CB 2: {list_players[1]}")
        print(f"LB: {list_players[2]}")
        print(f"RB: {list_players[3]}")
        contr_defense = combinations[elem][list_players[0]][6] + \
                        combinations[elem][list_players[1]][6] + \
                        combinations[elem][list_players[2]][6] + \
                        combinations[elem][list_players[3]][6]
        print(f"Contribució a la defensa: {contr_defense}")
        contr_posse = combinations[elem][list_players[0]][7] + \
                      combinations[elem][list_players[1]][7] + \
                      combinations[elem][list_players[2]][7] + \
                      combinations[elem][list_players[3]][7]
        print(f"Contribució a la possessió: {contr_posse}")
        contr_attack = combinations[elem][list_players[0]][8] + \
                       combinations[elem][list_players[1]][8] + \
                       combinations[elem][list_players[2]][8] + \
                       combinations[elem][list_players[3]][8]
        print(f"Contribució a l'atac: {contr_attack}")
        print()


def exercise_6_main() -> None:
    """We obtain the best defenders line in the world under our criteria.
    """
    print("EXERCICI 6")
    data = join_male_female("data", 2022)
    qualities_cb = ["mentality_interceptions", "mentality_aggression",
                    "defending_standing_tackle", "passing", "attacking_heading_accuracy"]
    qualities_lb_rb = ["defending_marking_awareness", "mentality_aggression",
                       "mentality_interceptions", "passing", "pace"]


    # MALE TEAM
    data_m = data[data["gender"] == "M"]
    # 10 or 20 best players of each position (by overall)
    best_position = players_best_position(data_m)
    # qualities of cb players
    data_cb_best = data_m[data_m["sofifa_id"].isin(best_position["CB"])]
    cb_best_qualities = qualities_players_position(data_cb_best, "short_name", qualities_cb)
    # qualities of lb players
    data_lb_best = data_m[data_m["sofifa_id"].isin(best_position["LB"])]
    lb_best_qualities = qualities_players_position(data_lb_best, "short_name", qualities_lb_rb)
    # qualities of rb players
    data_rb_best = data_m[data_m["sofifa_id"].isin(best_position["RB"])]
    rb_best_qualities = qualities_players_position(data_rb_best, "short_name", qualities_lb_rb)
    # We combine all the possibilities
    combinations = list(map(dict, product(cb_best_qualities.items(), cb_best_qualities.items(),
                            lb_best_qualities.items(), rb_best_qualities.items())))
    # We create a new list without repetition
    combinations = [item for item in combinations if len(item) == 4]
    combinations = order_combinations(combinations)
    print("3 millors línies defensives masculina")
    print_combinations(combinations, 3)
    print()


    # FEMALE TEAM
    data_f = data[data["gender"] == "F"]
    # 10 or 20 best players of each position (by overall)
    best_position = players_best_position(data_f)
    # qualities of cb players
    data_cb_best = data_f[data_f["sofifa_id"].isin(best_position["CB"])]
    cb_best_qualities = qualities_players_position(data_cb_best, "short_name", qualities_cb)
    # qualities of lb players
    data_lb_best = data_f[data_f["sofifa_id"].isin(best_position["LB"])]
    lb_best_qualities = qualities_players_position(data_lb_best, "short_name", qualities_lb_rb)
    # qualities of rb players
    data_rb_best = data_f[data_f["sofifa_id"].isin(best_position["RB"])]
    rb_best_qualities = qualities_players_position(data_rb_best, "short_name", qualities_lb_rb)
    # We combine all the possibilities
    combinations = list(map(dict, product(cb_best_qualities.items(), cb_best_qualities.items(),
                        lb_best_qualities.items(), rb_best_qualities.items())))
    # We create a new list without repetition
    combinations = [item for item in combinations if len(item) == 4]
    combinations = order_combinations(combinations)
    print("3 millors línies defensives femenina")
    print_combinations(combinations, 3)
    print()


    # VET TEAM
    data_v = data[data["age"] >= 30]
    # 10 or 20 best players of each position (by overall)
    best_position = players_best_position(data_v)
    # qualities of cb players
    data_cb_best = data_v[data_v["sofifa_id"].isin(best_position["CB"])]
    cb_best_qualities = qualities_players_position(data_cb_best, "short_name", qualities_cb)
    # qualities of lb players
    data_lb_best = data_v[data_v["sofifa_id"].isin(best_position["LB"])]
    lb_best_qualities = qualities_players_position(data_lb_best, "short_name", qualities_lb_rb)
    # qualities of rb players
    data_rb_best = data_v[data_v["sofifa_id"].isin(best_position["RB"])]
    rb_best_qualities = qualities_players_position(data_rb_best, "short_name", qualities_lb_rb)
    # We combine all the possibilities
    combinations = list(map(dict, product(cb_best_qualities.items(), cb_best_qualities.items(),
                            lb_best_qualities.items(), rb_best_qualities.items())))
    # We create a new list without repetition
    combinations = [item for item in combinations if len(item) == 4]
    combinations = order_combinations(combinations)
    print("3 millors línies defensives de jugadors veterans")
    print_combinations(combinations, 3)

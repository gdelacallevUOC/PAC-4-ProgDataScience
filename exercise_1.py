"""Module with all the functions in Exercise 1.

The functions will be used to read and process our data.
"""

import sys
import os
import pandas as pd


def read_add_year_gender(filepath: str, gender: str,
                         year: int) -> pd.DataFrame:
    """Read a player file that adds two columns to the information
        obtained: gender and year.

    Args:
            filepath: string with the path of the file we want to read.
            gender: M or F (acronym for Male or Female).
            year: year to which the data corresponds in XXXX format
                  (for example, 2020)

    Returns:
            Pandas dataframe resulting from adding the two columns mentioned to
            the initial information.
    """
    if (year < 2016 or year > 2022):
        sys.exit('The year has to be between 2016 and 2022')
    datafr = None
    # dtype warning
    dtype_df = {"gk": "str", "lw": "str", "lf": "str", "cf": "str", "rf": "str"}
    dtype_df["rw"] = "str"
    dtype_df["nation_position"] = "str"
    dtype_df["nation_logo_url"] = "str"
    if gender in ('M', 'F'):
        datafr = pd.read_csv(filepath, dtype = dtype_df)
    else:
        sys.exit('The gender has to be M or F')
    # we add the two columns
    datafr['gender'] = gender
    datafr['year'] = year
    return datafr


def join_male_female(path: str, year: int) -> pd.DataFrame:
    """Create a single dataframe with the data of all players
       in the same year.

    Args:
            path: string with the path in the folder containing the data.
            year: year to which the data corresponds in XXXX format
                  (for example, 2020)

    Returns:
            Pandas dataframe with the data of all players in the same year
            and contains information on the gender and year to which each
            player's data corresponds.
    """
    # We obtain the year with two digits
    year_str = str(year % 100)
    path_male = os.path.join(path, 'players_' + year_str + '.csv')
    path_female = os.path.join(path, 'female_players_' + year_str + '.csv')
    # We create the dataframe with the function read_add_year_gender
    datafr = pd.concat([read_add_year_gender(path_male, 'M', year),
                        read_add_year_gender(path_female, 'F', year)], ignore_index=True)
    return datafr


def join_datasets_year(path: str, years: list) -> pd.DataFrame:
    """Reads information corresponding to soccer players of both
       genders for several years and returns a single dataframe.

    Args:
            path: string with the path in the folder containing the data.
            years: list of years to be included in the dataframe, in
                   [XXXX,...] format

    Returns:
            Pandas dataframe with the data of all players in several years
            and contains information on the gender and year to which each
            player's data corresponds.
    """
    # We create the dataframe with the function join_male_female
    datafr = pd.concat([join_male_female(path, year) for year in years], ignore_index=True)
    return datafr

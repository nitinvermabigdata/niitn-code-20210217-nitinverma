"""
Following unit test cases are tested:

Test function `calculate_bmi`
TC1: should calculate the bmi correctly.

Test function `calc_category_health_risk`
TC2: should insert bmi_category based on bmi_range provided
TC3: should insert correct health_risk based on bmi_range provided
TC4: should raise ValueError if bmi_range dont have 2 elements
"""

import pytest 
import solution
import pandas as pd
from os.path import abspath, join
data_path = abspath(join('..', 'data'))
table1=join(data_path, 'bmi.csv')#Bmi Table data path
data_dictionary=pd.read_csv(table1).to_dict(orient="index") # Read Bmi table data
def define_test_data():
    df = pd.DataFrame(data=[['Male', 175, 75],
                            ['Female', 150, 62]],
                      columns=['Gender', 'HeightCm', 'WeightKg'])

    return df


# TC1
def test_bmi_calculation():
    # df = pd.DataFrame(data=[['Male', 175, 75]],
    #                   columns=['Gender', 'HeightCm', 'WeightKg'])
    df = define_test_data()
    df = solution.calculate_bmi(df)
    assert round(df.loc[0, 'bmi'], 2) == 24.49


# TC2
def test_category():
    # df = pd.DataFrame(data=[['Male', 175, 75],
    #                         ['Female', 150, 62]],
    #                   columns=['Gender', 'HeightCm', 'WeightKg'])
    df = define_test_data()
    bmi_range = [20, 29]
    category = 'test'
    health_risk = 'test_risk'
    df = solution.calculate_bmi(df)
    df = solution.calc_category_health_risk(df,data_dictionary=data_dictionary )
    assert df.loc[1, 'bmi_category'] == category


# TC3
def test_health_risk():
    df = define_test_data()
    bmi_range = [20, 29]
    category = 'test'
    health_risk = 'test_risk'
    df = solution.calculate_bmi(df)
    df = solution.calc_category_health_risk(df,data_dictionary=data_dictionary)
    assert df.loc[1, 'health_risk'] == health_risk


# TC4
def test_bmi_range_value_error():
    df = define_test_data()
    bmi_range = [20, 29, 30]
    category = 'test'
    health_risk = 'test_risk'

    with pytest.raises(ValueError):
        solution.calc_category_health_risk(df,data_dictionary=data_dictionary)

from os.path import abspath, join
import pandas as pd
import numpy as np
import ijson
import json
def calculate_bmi(df):
    """
    1. Convert height from cm to m^2
    2. Calculate the BMI based on the below formula:
        BMI(kg/m2) = mass(kg) / height(m)2
    
    Returns:
        modified df with `bmi` column.
    """    
    height_m2 = (df['HeightCm'] / 100)**2
    df['bmi'] = (df['WeightKg'] / height_m2)
    return df


def calc_category_health_risk(df,data_dictionary):
    """
    Calculate the BMI Category and health risk based on the BMI.
    Args:
        df: pandas DataFrame
            dataframe with bmi information.
            must have column 'bmi'
        bmi_range: dict 
            min and max range of bmi
        category_name: str
            category name value based on bmi range
        health_risk: str
            health risk value based on the bmi range
    
    Returns: pandas DataFrame
        The df is updated with two new columns `bmi_category` and `health_risk`
        

    """
    for i,k in data_dictionary.items():
        bmi_range=k['BMI Range (kg/m2)'].split('-')
        if len(bmi_range) ==0:
            raise ValueError(f"bmi_range must have 1 elements, ",f"{len(bmi_range)} were provided.")
        if len(bmi_range)> 1:
            min_range=float(bmi_range[0])
            max_range=float(bmi_range[1])
            idx = df.index[(df['bmi'] >= min_range) &(df['bmi'] <= max_range)]
            category_name=data_dictionary[i]['BMI Category']
            health_risk=data_dictionary[i]['Health risk']
            df.loc[idx, 'bmi_category'] = category_name
            df.loc[idx, 'health_risk'] = health_risk
        else:
            min_range=float(bmi_range[0])
            idx = df.index[(df['bmi'] >= min_range)]
            category_name=data_dictionary[i]['BMI Category']
            health_risk=data_dictionary[i]['Health risk']
            df.loc[idx, 'bmi_category'] = category_name
            df.loc[idx, 'health_risk'] = health_risk
            
    return df
    


if __name__ == '__main__':
    
    data_path = abspath(join('..', 'data'))
    infile = join(data_path, 'data.json')# input file path
    outfile = join(data_path, 'out.json')# Output file path
    table1=join(data_path, 'bmi.csv')#Bmi Table data path
    # below variables can be read directly from table as well
   
    category_name='Overweight'
    data_dictionary=pd.read_csv(table1).to_dict(orient="index") # Read Bmi table data 
    
    df = pd.read_json(infile)
	 
    
    df = calculate_bmi(df)
    df = calc_category_health_risk(df, data_dictionary)
    
    cnt = len(df[df['bmi_category'] == category_name])
    print(f"Number of {category_name} people = {cnt}")
    df.to_json(outfile, orient='records')

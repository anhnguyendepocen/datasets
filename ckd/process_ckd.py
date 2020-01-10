""" Process CKD file to CSV
"""

import os.path as op

import numpy as np
import pandas as pd
from scipy.io import arff

# Load data as Numpy record arrays.
data, meta = arff.loadarff('chronic_kidney_disease_full.arff')

# To pandas data frame
df = pd.DataFrame.from_records(data)

# Rename columns to full names given in header of ARFF file.
renames = {
    'age': 'Age',
    'bp': 'Blood Pressure',
    'sg': 'Specific Gravity',
    'al': 'Albumin',
    'su': 'Sugar',
    'rbc': 'Red Blood Cells',
    'pc': 'Pus Cell',
    'pcc': 'Pus Cell clumps',
    'ba': 'Bacteria',
    'bgr': 'Blood Glucose Random',
    'bu': 'Blood Urea',
    'sc': 'Serum Creatinine',
    'sod': 'Sodium',
    'pot': 'Potassium',
    'hemo': 'Hemoglobin',
    'pcv': 'Packed Cell Volume',
    'wbcc': 'White Blood Cell Count',
    'rbcc': 'Red Blood Cell Count',
    'htn': 'Hypertension',
    'dm': 'Diabetes Mellitus',
    'cad': 'Coronary Artery Disease',
    'appet': 'Appetite',
    'pe': 'Pedal Edema',
    'ane': 'Anemia',
    'class': 'Class'
}

df = df.rename(renames, axis='columns')


def recode_bytes(val):
    """ Recode columns with byte strings to strings

    Replace ? with NA
    """
    out = val.decode('latin1')
    if out == '?':
        out = np.nan
    return out


for col_name, col_dtype in df.dtypes.items():
    if col_dtype != np.dtype(object):
        continue
    # Recode object column with recoder.
    new_col = df[col_name].apply(recode_bytes)
    # Convert to float if possible.
    try:
        new_col = new_col.astype(float)
    except ValueError:
        pass
    df[col_name] = new_col

out_fname = op.join('processed', 'chronic_kidney_disease.csv')
df.to_csv(out_fname, index=False)
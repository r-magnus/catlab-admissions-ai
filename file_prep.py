# file_prep.py
# Converts the given .csv into a usable, numeric format. Hard-coded.
# @author Ryan Magnuson rmagnuson@westmont.edu

# Setup
import pandas as pd
import seaborn as sns
import numpy as np
import sklearn.preprocessing

np.random.seed(1128)

# Loading CSV
students = pd.read_csv("admissions_data.csv")

# Dropping Unnecessary Data
removable = ["Contact Case Safe ID [TRUNCATED]", "Active Application: Case Safe ID [TRUNCATED]", # hard-coded
             "Education ID [TRUNCATED]", "Case Safe ID_x [TRUNCATED]",
             "Case Safe ID_y [TRUNCATED]", "Case Safe ID.1 [TRUNCATED]",
             "Financial Aid Package ID [TRUNCATED]", "Application Case Safe Id [TRUNCATED]",
             "Colleague_Id [TRUNCATED]", "External Package Id [TRUNCATED]"]

for to_remove in removable: # ID removal
  students = students.drop(to_remove, axis=1)

students.drop("_Short8374", axis=1) # manual

# Binarize Cols # (currently unused)
def binarize(to_binarize):
  """
  Binarizes a list of given columns in a dataset, in-place.
  :param to_binarize: List of column names
  """
  for binarizable in to_binarize:
    for row in range(len(students[binarizable])):
      if not pd.isna(students.loc[row, binarizable]):
        students.loc[row, binarizable] = 1
      else:
        students.loc[row, binarizable] = 0

to_binarize = ["_Cover6848", "_Think8418"]
#binarize(to_binarize)

# print(students["_Cover6848"]) # debug sout

# Label Encode Categorical Vars
def label_encode(to_encode):
  """
  Performs a Label Encoding on given list of cat. vars, in-place.
  :param to_encode: list of cols to label encode.
  """
  le = sklearn.preprocessing.LabelEncoder()
  for encodable in to_encode:
    le.fit(students[encodable])
    le.transform(students[encodable])

to_encode = []
label_encode(to_encode)

# Augustinian Score/Fill-In
def fill_in(to_fill):
  """
  Fills-in the list of given numeric columns with zeroes, keeping original numbers. In-place.
  :param to_fill: List of columns to fill with zeroes.
  """
  for fillable in to_fill:
    for row in range(len(students[fillable])):
      if pd.isna(students.loc[row, fillable]):
        students.loc[row, fillable] = 0

to_fill_in = ["Augustinian Fit", "Augustinian Leadership"]
fill_in(to_fill_in)

# print(students["Augustinian Fit"]) # debug sout
# print(students["Augustinian Leadership"]) # debug sout

# Dropping Similar Cols


# Displaying Missing Data (updated)

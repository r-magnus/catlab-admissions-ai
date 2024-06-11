# file_prep.py
# Converts the given .csv into a usable, numeric format. Hard-coded.
# @author Ryan Magnuson rmagnuson@westmont.edu

# Setup
import pandas as pd
import seaborn as sns
import numpy as np
import sklearn.preprocessing
import matplotlib.pyplot as plt

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

students = students.drop("_Short8374", axis=1) # manual

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
#binarize(to_binarize) # TODO: Uncomment to use -- currently deprecated.

# print(students["_Cover6848"]) # debug sout

# Label Encode Categorical Vars
def label_encode(to_encode): # NOTE: used later on once other cat vars are automatically found
  """
  Performs a Label Encoding on given list of cat. vars, in-place.
  :param to_encode: list of cols to label encode.
  """
  le = sklearn.preprocessing.LabelEncoder()
  for encodable in to_encode:
    students[encodable] = le.fit_transform(students[encodable])

to_encode = ["_Cover6848", "_Think8418", "_Child5781", "_Past0912"]
label_encode(to_encode)

# print(students["_Child5781"]) # debug sout

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

to_fill_in = ["Augustinian Fit", "Augustinian Leadership",
              "Number of Visits", "Active Application: Max SAT Composite",
              "Unmet Need", "Family Contribution", "Award to Total Aid Validation", # NOTE: may need to remove some of these -- assumptions
              "Pell Grant Eligible", "Total Funds", "Total Aid"
              ]
fill_in(to_fill_in)

# print(students["Augustinian Fit"]) # debug sout
# print(students["Augustinian Leadership"]) # debug sout

# Combine Numeric Cols
def combine_num(A_col, B_col):
  """
  Combines the given two columns, adds the new combined column to the dataframe. Recommended dropping used cols.
  :param A_col: first column to combine
  :param B_col: second column to combine
  """
  combined = []
  for i in range(len(students[A_col])): # len(A_col) == len(B_col)
    if pd.isna(students.loc[i, A_col]):
      if pd.isna(students.loc[i, B_col]):
        combined.append(None)
      else:
        combined.append(students.loc[i, B_col])
    else:
      combined.append(students.loc[i, A_col]) # currently ignores if B_col also has mismatching val (average)

  students["Combined %s + %s" % (A_col, B_col)] = combined # new column

combine_num("GPA", "GPA Academic")
students = students.drop("GPA", axis=1)
students = students.drop("GPA Academic", axis=1)

combine_num("Combined GPA + GPA Academic", "Cum GPA") # Instead of keeping separate
students = students.drop("Cum GPA", axis=1)
students = students.drop("Combined GPA + GPA Academic", axis=1) # messy

# fill_in("Combined Combined GPA + GPA Academic + Cum GPA")

# print(students["Combined GPA + GPA Academic"]) # debug sout
# print(students.head()) # debug sout

# Encoding Major of Interest
to_encode = ["Active Application: Major of Interest", "Active Application: Major of Interest 2"]
label_encode(to_encode) # NOTE: Currently ignoring null data and just throwing it into encoding.

# Separate Categorical vars
cat_vars = []
for column in students.columns: # NOTE: add in skipping id entries (or drop them)
  if not (students[column].dtype.name == "int64" or students[column].dtype.name == "float64"):
    cat_vars.append(column)

def separate_date_vars(columns): # NOTE: current bug -- must be called after 'Major of Interest' columns are encoded
  """
  Separates categorical vars from vars with specifically dates. Modifies given list in-place.
  :param columns: List of categorical columns to parse through and separate
  :return: list of vars with dates for data
  """
  date_vars = []
  for var in columns:
    for row in range(len(students[var])):
      if "/" in str(students.loc[row, var]):
        date_vars.append(var)
        break

  for var in date_vars:
    columns.remove(var)

  return date_vars

date_vars = separate_date_vars(cat_vars)

# print(cat_vars) # debug sout
# print(date_vars) # debug sout

# Mass Encoding
label_encode(cat_vars) # NOTE: Currently ignoring null data and just throwing it into encoding.

# Manual Column Removal
to_drop = ["To Date:", "Active Application: Date Prospect"] # NOTE: may need to restore, currently operating under a big assumption
for droppable in to_drop:
  date_vars.remove(droppable)
  students = students.drop(droppable, axis=1)

# Calculate Age
def parse_dates(date_columns):
  """
  Turns all dates (str) into list of ints, from given column name
  :param date_columns: individual column with date-based data
  :return: List of lists with the format [[month, day, year], ...]
  """
  dates = []
  for date in date_columns:
    dates.append(date.split("/"))
  return dates

def calculate_age(start_date_col, end_date_col):
  """
  Calculates age based on given column names, assuming date data type, split with '/' character.
  Recommended to drop given columns once called.
  :param start_date_col: Name of beginning column
  :param end_date_col: Name of ending column
  """
  ages = []
  for i in range(len(students[start_date_col])):
    if not (pd.isna(students.loc[i, start_date_col]) or pd.isna(students.loc[i, end_date_col])):
      born, current = parse_dates([students.loc[i, start_date_col], students.loc[i, end_date_col]])
      age = int(current[2]) - int(born[2]) # NOTE: currently only using year to calculate age
      ages.append(age)
    else:
      ages.append(None)

  students["Age"] = ages

# calculate_age("_Suddenly7410", "Active Application: Date Applied") # TODO: Uncomment to use -- currently inaccurate!
# students = students.drop("_Suddenly7410", axis=1)
# students = students.drop("Active Application: Date Applied", axis=1)
# date_vars.remove("_Suddenly7410")
# date_vars.remove("Active Application: Date Applied")

# Binarize 'Date Cancel'
def build_enrolled(col):
  """
  Binarizes inversely the given column by adding a new column. Recommended to remove used column after use.
  :param col: Given column name
  """
  enrolled = []
  for row in range(len(students[col])):
    if pd.isna(students.loc[row, col]):
      enrolled.append(1) # enrolled
    else:
      enrolled.append(0) # cancelled

  students["Enrolled"] = enrolled

build_enrolled("Active Application: Date Cancel")
students = students.drop("Active Application: Date Cancel", axis=1)
date_vars.remove("Active Application: Date Cancel")

# Manual Remove of Dates
for col in date_vars: # NOTE: This removes all date variables. Remove if dates are needed.
  students = students.drop(col, axis=1)

# Remove Missing Rows (currently new 'GPA' column)
students = students.dropna() # TODO: Comment to prevent data loss.
# NOTE: This is removing about 21.6% of data.

# Displaying Missing Data (updated)
plt.figure(figsize=(10,6)) # TODO: Uncomment to generate new graph
sns.set(font_scale=.45)
sns.displot(
  data=students.isna().melt(value_name="missing"),
  y="variable",
  hue="missing",
  multiple="fill"
)
plt.savefig("updated_null_entries.jpg")
plt.close()

# Save CSV
students.to_csv("updated_admissions_data.csv") # TODO: Uncomment to save .csv file

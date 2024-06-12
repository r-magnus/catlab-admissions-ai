# Predictive regression model for CATlab's admissions project
# @author Ryan Magnuson rmagnuson@westmont.edu

# Warning Suppression # TODO: Uncomment the below code to suppress warnings from scikit!
# def warn(*args, **kwargs): # @Override
#     pass # suppression
# import warnings
# warnings.warn = warn

# Setup
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split

np.random.seed(1128) # consistency

# Data Processing
students = pd.read_csv("updated_admissions_data.csv")
print(students.head(), students.shape)

# removable = ["Contact Case Safe ID [TRUNCATED]", "Active Application: Case Safe ID [TRUNCATED]", # hard-coded
#              "Education ID [TRUNCATED]", "Case Safe ID_x [TRUNCATED]",
#              "Case Safe ID_y [TRUNCATED]", "Case Safe ID.1 [TRUNCATED]",
#              "Financial Aid Package ID [TRUNCATED]", "Application Case Safe Id [TRUNCATED]",
#              "Colleague_Id [TRUNCATED]", "External Package Id [TRUNCATED]"]
# for to_remove in removable: # ID removal
#   students = students.drop(to_remove, axis=1)
print(students.head(), students.shape)

train, test = train_test_split(students,test_size=.20)

# Separate cat/num vars
cat_vars = [] # should now be empty
num_vars = []
for column in students.columns: # NOTE: add in skipping id entries (or drop them)
  if students[column].dtype.name == "int64" or students[column].dtype.name == "float64":
    num_vars.append(column)
  else:
    cat_vars.append(column)

# print("CAT VARS: \n%s\nLen: %d" % (cat_vars, len(cat_vars)))
# print("NUM VARS: \n%s\nLen: %d" % (num_vars, len(num_vars)))

# Data Conversion & Transformation
# from sklearn.preprocessing import LabelBinarizer # not quite what we want here
# lb = LabelBinarizer()

# students.drop("_Short8374", axis=1)

# Missing Data Plot
# plt.figure(figsize=(10,6))
# sns.set(font_scale=.45)
# sns.displot(
#   data=students.isna().melt(value_name="missing"),
#   y="variable",
#   hue="missing",
#   multiple="fill"
# )
# plt.savefig("null_entries.jpg")
# plt.close()
#sns.set(font_scale=1) # reset, just in case

# SCATTER PLOTS #
for y in num_vars: # TODO: Uncomment this section to regenerate scatter plots!
  print(y)
  for x in num_vars:
    plt.figure(figsize=(10,10))
    sns.set(font_scale=.8)
    sns.scatterplot(
      x=students[x],
      y=students[y]
    )
    plt.savefig("scatters/%s_%s.jpg" % (str(x).replace("Active Application: ", ""), str(y).replace("Active Application: ", "")))
    plt.close()

# Correlation Matrix (numerical)
# sns.set(font_scale=.6) # .6
# corrMatrix = train[students.columns].corr() # num_vars
# sns.heatmap(corrMatrix, annot=True)
# plt.savefig("correlation_matrix.png")
# plt.close()

# DATA IMPUTATION #
# from sklearn.experimental import enable_iterative_imputer
# from sklearn.impute import IterativeImputer
#
# imputer = IterativeImputer(n_nearest_features=None, imputation_order='ascending') # estimator=BayesianRidge()
# imputer.fit(students)
# students_imputed = imputer.transform(students)
# students_imputed = pd.DataFrame(students_imputed)
# students_imputed.to_csv("imputed.csv", sep=",") # this will probably not give accurate results... but who knows?

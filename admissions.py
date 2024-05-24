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

# Data Processing
students = pd.read_csv("admissions_data.csv")
print(students.head(), students.shape)

# Missing Data Plot
plt.figure(figsize=(10,6))
sns.set(font_scale=.45)
sns.displot(
    data=students.isna().melt(value_name="missing"),
    y="variable",
    hue="missing",
    multiple="fill"
)
plt.savefig("null_entries.jpg")
plt.close()
sns.set(font_scale=1) # reset, just in case


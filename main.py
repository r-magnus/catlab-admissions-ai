# main.py
# Main file to run for making ML Admissions predictions.
# @author Ryan Magnuson rmagnuson@westmont.edu

# Setup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.preprocessing
from sklearn.model_selection import train_test_split

# exec(open("file_prep.py").read()) # TODO: Uncomment to build new .csv and data graphic
np.random.seed(1128)

# Data Loading
students = pd.read_csv("updated_admissions_data.csv")
train, test = train_test_split(students,test_size=.20)

# Correlation Matrix
plt.figure(figsize=(30, 20))
sns.set(font_scale=.6)
corrMatrix = train[students.columns].corr()
sns.heatmap(corrMatrix, annot=True)
plt.savefig("updated_correlation_matrix.png")
plt.close()

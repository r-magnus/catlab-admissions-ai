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
from sklearn.linear_model import LogisticRegression

# exec(open("file_prep.py").read()) # TODO: Uncomment to build new .csv and data graphic
np.random.seed(1128)

# Warning Suppression
def warn(*args, **kwargs):  # TODO: Uncomment this section to suppress warnings from scikit!
    pass
import warnings
warnings.warn = warn

# Data Loading
students = pd.read_csv("updated_admissions_data.csv")
students = students.drop("Admit From Institution", axis=1) # NOTE: this column is entirely '1', and not super useful
train, test = train_test_split(students, test_size=.20)

# Prep Data Split
def prep_data(data):
  """
  Splits given data into X and y sections.
  :param data: Given data to split.
  :return: Split (tuple) of given data. Format: (X, y)
  """
  df = data.copy()
  return df.drop("Enrolled", axis=1), df["Enrolled"]

X_train, y_train = prep_data(train)
X_test,  y_test  = prep_data(test)

# Correlation Matrix
# plt.figure(figsize=(30, 20)) # TODO: Uncomment to regenerate Correlation Matrix!
# sns.set(font_scale=.6)
# corrMatrix = train[students.columns].corr()
# sns.heatmap(corrMatrix, annot=True)
# plt.savefig("updated_correlation_matrix.png")
# plt.close()

# Logistic Regression Model
lr = LogisticRegression(max_iter=9999) # max_iter for balance of accuracy & time
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test) # prediction
y_pred_proba = lr.predict_proba(X_test) # confidence rating
score = lr.score(X_train, y_train)
print("Accuracy: %.2f%%" % (score*100))

for i in range(len(y_pred)):
  print("Enrolled: %d | CR: %.5f" % (y_pred[i], y_pred_proba[i][0]*100))

print("Max (Enrolled: 1): %.5f" % (max([y_pred_proba[e][0] for e in range(len(y_pred_proba)) if y_pred[e] == 1])*100)) # debug sout

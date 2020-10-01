#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 17:54:37 2017

@author: mohammedalbatati
"""

# import numpy as np
import csv
import pandas

# import matplotlib.pyplot as plt

survey_source_path = "Survey.csv"
out_put_file_path = "Surveyresults.csv"
list_of_MD_file_path = "MD_input.csv"
# ===========================================
# load the sourse data for survey and fill the MD and TVD lists
with open(survey_source_path, "r") as f:
    data = csv.reader(f, delimiter=",")
    header = next(data)
    MD = []
    TVD = []
    for row in data:
        MD.append(row[0])
        TVD.append(row[1])
# ===========================================
# load the needed MD values to compute the TVD
with open(list_of_MD_file_path, "r") as f:
    data_in = csv.reader(f, delimiter=",")
    this_header = next(data_in)
    MD_in = []
    for row in data_in:
        if row:
            MD_in.append(float(row[0]))

        # the (if row:) disregards the empty values

# The below block also skip the blank / empty rows in csv files
#        if not (row):
#            continue
#        else:
#            MD_in.append(float(row[0]))
# Make the input with 2 digits
# ===========================================
# making the values float with 2 digits xx.00
MD_in_2f = []
for x in MD_in:
    MD_in_2f.append(format(x, ".2f"))

# ===========================================
# The calculation function
def calTVD(MDi):
    """ Calculate the TVD based on the MD using the survey"""
    if float(MDi) < float(MD[0]):
        print(
            "The values of MD should be between {0}m and {1}m the selected {2}m value is not valid".format(
                MD[0], MD[-1], MDi
            )
        )
    elif float(MDi) > float(MD[-1]):
        print(
            "The values of MD should be between {0}m and {1}m the selected {2}m value is too High".format(
                MD[0], MD[-1], MDi
            )
        )
    else:
        # find the index to start calculation
        indx = [
            i
            for i in range(0, len(MD))
            if float(MD[i]) <= MDi and float(MD[i + 1]) >= MDi
        ]
        indint = indx[0]
        # Calculation bolck
        newTVD = float(TVD[indint]) + (float(MDi) - float(MD[indint])) * (
            float(TVD[indint + 1]) - float(TVD[indint])
        ) / (float(MD[indint + 1]) - float(MD[indint]))
        #        print('At MD depth',MDi,'m the nearest MD is ', MD[indint +1 ],' at index ', indx[0])
        #        print('Calculated TVD equals {0} m at MD {1} m'.format(float(newTVD), float(MDi)))
        return newTVD


# ===========================================
# Perform the calculation
TVD_out = []
for x in MD_in:
    TVD_out.append(format(calTVD(x), ".2f"))
# print(MD_in)
# print(TVD_out)

# ===========================================
"""Pass the results to a new csv file """
pd = pandas.DataFrame(list(zip(TVD_out, MD_in_2f)), columns=["TVD", "MD"])
pd.to_csv(out_put_file_path, line_terminator="\n")
print(len(TVD_out))

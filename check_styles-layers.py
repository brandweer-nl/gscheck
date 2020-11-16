#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:25:47 2020

@author: legemg

Scripted test om gscheck aan de tand te voelen over styles (ook in workspaces).

ALLSTYLES
1. alle styles uit de hoofdstructuur ophalen
2. alle styles uit alle workspaces ophalen

"""

import gscheck
import copy
from csv import DictWriter

# create GSCheck object
brwaa = gscheck.GSCheck("brwaa")

# ALLSTYLES algorithm - part 1

allstyles = []

# get all styles from root of tree
styles = brwaa.retrieve("styles")[1]

# iterate over all styles and build part 1 of the endresult
print("Retrieving styles with list comprehension")
allstyles = [{"name_workspace": "", "name_style": y}
            for k, v in styles["styles"].items()
            for i in v
            for x, y in i.items() if x == "name"]

# # same result as with the list comprehension implementation above
# # only with a classic for loop which allows print statements inter alia
# # only use/uncomment one of these implementations
# counter = 0
# # iterate over all styles and build part 1 of the endresult
# print("Getting styles with classic for loop")
# for k, v in styles["styles"].items():
#     for i in v:
#         for x, y in i.items():
#             if x == "name":
#                 tempdict = {}
#                 tempdict["name_workspace"] = "" # empty for root
#                 tempdict["name_style"] = y
#                 allstyles.append(tempdict)
#                 counter += 1
#                 print("Processing style {}".format(counter))

# ALLSTYLES algorithm - part 2

# get all workspaces from root of tree to iterate over later
workspaces = brwaa.retrieve("workspaces")[1]

print("Retrieving workspaces")
wplist = [y for k, v in workspaces["workspaces"].items()
          for i in v
          for x, y in i.items() if x == "name"]

# now go into the workspaces themselves to fetch the styles
wpcounter = 0
stylecounter = 0
print("Iterating over all workspaces for styles")
for wp in wplist:
    wpcounter += 1
    print("Working on workspace {}: {}".format(wpcounter, wp))
    tempdict = {}
    tempdict["name_workspace"] = wp
    tempstyle = brwaa.retrieve("workspaces", "{}".format(wp), "styles")[1]
    if len(tempstyle["styles"]) > 0:
        #print("Iterating over all workspaces for styles")
        for k, v in tempstyle["styles"].items():
            for i in v:
                for x, y in i.items():
                    if x == "name":
                        tempdict["name_style"] = y
                        allstyles.append(copy.deepcopy(tempdict))
                        stylecounter += 1
                        print("Processing workspace/style {}: {}".format(stylecounter, y))
    elif len(tempstyle["styles"]) == 0:
        print("Workspace has remote or no styles attached: {}".format(wp))
        
with open("./output/styles-layers.csv","w") as outfile:
    writer = DictWriter(outfile, ("name_workspace","name_style"))
    writer.writeheader()
    writer.writerows(allstyles)
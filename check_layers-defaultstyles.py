#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:25:47 2020

@author: legemg

Scripted test om gscheck aan de tand te voelen over default styles bij layers.

"""

import gscheck

from csv import DictWriter

brwaa = gscheck.GSCheck("brwaa_prod")

layers = brwaa.retrieve("layers")[1]
styles = brwaa.retrieve("styles")[1]

layerstyle = []
counter = 0

for k, v in layers["layers"].items():
    for i in v:
        for x, y in i.items():
            if x == "name":
                tempdict = {}
                tempdict["name_layer"] = y
                #global templayer # for debugging
                templayer = brwaa.retrieve("layers", "{}".format(y))[1]
                for k, v in templayer.items():
                    if k == "error":
                        print("Found error!")
                        tempdict["type_layer"] = "ERROR"
                        tempdict["name_defaultstyle"] = v
                    elif k == "layer":
                        for k, v in v.items():
                            if k == "defaultStyle":
                                for x, y in v.items():
                                    if x == "name":
                                        tempdict["name_defaultstyle"] = y
                            if k == "type":
                                tempdict["type_layer"] = v
                    layerstyle.append(tempdict)
                    counter += 1
                    print("Processing layer {}".format(counter))

with open("./output/layers-defaultstyles.csv","w") as outfile:
    writer = DictWriter(outfile, ("name_layer","type_layer","name_defaultstyle"))
    writer.writeheader()
    writer.writerows(layerstyle)
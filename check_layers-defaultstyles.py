#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:25:47 2020

@author: legemg

Scripted test om gscheck aan de tand te voelen over default styles bij layers.

"""

import gscheck
import pandas as pd

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
                templayer = brwaa.retrieve("layers", "{}".format(y))[1]
                for k, v in templayer.items():
                    if k == "error":
                        brwaa.log("Found error!")
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
                    brwaa.log("Processing layer {}".format(counter))

writer = pd.ExcelWriter("./output/brwaa_layers-defaultstyles.xlsx")
dflayer = pd.DataFrame(layerstyle)
dflayer.to_excel(writer,
                        sheet_name = "layers_defaultstyles",
                        header = ["name_layer",
                                  "type_layer",
                                  "name_defaultstyle"],
                        index = False)
dflog = pd.DataFrame(brwaa.logdata)
dflog.to_excel(writer,
                       sheet_name = "log_messages",
                       header = ["log message"],
                       index = False)
writer.save()
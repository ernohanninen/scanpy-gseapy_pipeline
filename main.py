#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: main.py
Date: 2021-03-09
Author: Erno Hänninen

Description:
    This script connects the server with the scanpy-gseapy pipeline

List of functions:
    -    sc_analysis
    -    gsea_analysis
List of "non standard" modules:
    -    pandas

Error handling:
    - Reading the file in function gsea_analysis happens inside try clause. If error occurs during reading, error message is printed to the user
    
Procedure for sc_analysis function:
    1. Call run_gsea function. Function run_gsea takes the output of run_sc_analysis function as an argument

Procedure for gsea_analysis function:
    1. Get the file from folder where ranked list is stored
    2. Read the file to a dataframe
    3. Call the run_gsea function. Function run_gsea takes the dataframe as an argument 
    
"""

import gsea
import os
import sys
import api 
import pandas

def sc_analysis(numPlots):
    #calling run_gsea function. run_gsea takes the ranked list from run_sc_analysis as an argument
    status = gsea.run_gsea(gsea.run_sc_analysis(), numPlots) 
    if status == "error":
        return "error"
    else:
        return "done"
    
def gsea_analysis(numPlots):
    #Reading the ranked list given by the user to a dataframe
    path = os.getcwd() + "/rankedList/"
    folder = os.fsencode(path)
    for file in os.listdir(folder): #Reading the folder where ranked list is stored
        filename = os.fsdecode(file)
    
    try:
        df = pandas.read_csv(path + filename, sep="\t") #Read the file
    except:     
        return("error")
    else:
        #Call run_gsea function. Function takes ranked list as an argument
        gsea.run_gsea(df, numPlots)
        return("done")
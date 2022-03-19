#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: gsea.py
Date: 2021-03-09
Author: Erno Hänninen

Description:
   This script communicates between scanpy-gseapy pipeline and the frontend. 
   It handles the requests of frontend and sends responses back to the frontend.
   This script also builds new file structure for every analysis, where the input files are stored
    
List of functions:
   -  upload_10xGenomicsFile, upload_RankedList, read_image_path

List of "non standard" modules:
   -  flask, flask restful, werkzeug

Procedure:
   -  Procedure for functions upload_10xGenomicsFile and upload_RankedList are very similar:
      1. Read the input files to variable
      2. Build the folder structure and save the input files
      3. Calling function to run the analysis
      4. Handling the possible errors occured during analysis / reading the GSEA plot paths to list
      5. Returning the analysis result / information about possible error to the frontend
"""

from flask import  Flask, request
from flask_restful import Api, Resource, reqparse
#import flask_restful
from werkzeug.utils import secure_filename
import sys
import shutil
sys.path.append("../../")
import main
import os

app = Flask(__name__)

#This function handles the inputted 10xgenomics files
#This function is called from script FileUploader1.js
@app.route('/uploadFile', methods = ['POST'])
def upload_10xGenomicsFile():
   if request.method == 'POST':
      print("Starting the analysis")
      
      #Reading the files
      f1 = request.files["file1"] #provided 10xGenomics files
      f2 = request.files["file2"]
      f3 = request.files["file3"]
      f4 = request.files["geneSetFile"] #Provided geneset
      numPlots = request.values.get("numPlots") #Number of output plots
      
      original_dir = os.getcwd() #Get the current working directory

      #Building the folder structure for the input files
      if(os.path.isdir("../../data")):
        shutil.rmtree("../../data")
      os.mkdir("../../data")
      os.mkdir("../../data/hg")
      os.mkdir("../../data/geneSet")
      os.chdir("../../data/hg")
      #Storing the 10xGenomics files to folder
      f1.save(secure_filename(f1.filename))
      f2.save(secure_filename(f2.filename))
      f3.save(secure_filename(f3.filename))
      
      #Saving the geneset to folder
      os.chdir("../geneSet")
      f4.save(secure_filename(f4.filename))
      
      #Working directory is now the data folder
      os.chdir("../") 
      #Calling function that starts the actual analysis
      status = main.sc_analysis(numPlots)
      
      #If return value is "done", analysis is done correctly
      if status == "done":
         images = read_image_path()
            
         #Change the working dir back to what it was in the beginning 
         os.chdir(original_dir)
         #Return a list of the GSEA plot paths in JSON format
         return  {'files': images}
      #If error occured during analysis, frontend prints error message to client
      elif status == "error":
         #Change working dir back to what it was before analysis
         os.chdir(original_dir)
         return "error"

#THis function handles the inputted ranked gene list 
#This function is called from script FileUploader2.js
@app.route('/uploadRankedFile', methods = ['POST'])
def upload_RankedList():
   if request.method == 'POST':
      print("Starting the analysis")
      original_dir = os.getcwd()
      
      #Reading the files
      f1 = request.files["file1"] #Ranked gene list
      geneSet = request.files["geneSetFile"] #Gene set
      numPlots = request.values.get("numPlots") #Number of output plots
      
      #Building the folder structure to the input and saiving the input files
      if(os.path.isdir("../../data")):
        shutil.rmtree("../../data")
      os.mkdir("../../data")
      os.mkdir("../../data/rankedList")
      os.mkdir("../../data/geneSet")
      os.chdir("../../data/rankedList")
      
      #Saving the files
      f1.save(secure_filename(f1.filename))#Ranked list
      os.chdir("../geneSet")
      geneSet.save(secure_filename(geneSet.filename)) #gene set
      
      os.chdir("../") #Working directory is now in data folder
      
      #Calling function that starts the actual analysis
      status = main.gsea_analysis(numPlots)
      
      #If error occurs during gsea, the error is handled
      if status == "done":
         images = read_image_path()
         #Change the working dir back what it was before programe runned
         os.chdir(original_dir)
         return {'files': images}
      #If error occured during analysis, frontend prints error message to client
      elif status == "error":
         os.chdir(original_dir)
         return "error"

#Reading the GSEA plot paths to a list
#This function is reading the plot path, so that the paths can then be sent to frontend for displaying the images to the user. 
#Unfortunately the code (on file FuleUploader1.js) that tires to display the images to the user doesn't work
def read_image_path():
   wd = os.getcwd()
   path =  wd + "/GSEA_Prerank/"  
   print("PATH : ", path)  
   folder = os.fsencode(path)
   images = []
   for file in os.listdir(folder):
      filename = os.fsdecode(file)     
      if filename.endswith(".png"):
         images.append(path+filename)
   return images
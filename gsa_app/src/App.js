/*
Title: App.js
Date: 2021-03-09
Author: Erno Hänninen

Description:
  - This script contains the elements of the web interface. It uses two other scripts FileUploader1 and FileUploader2.
    Componets of the web page can be displayed using radio buttons. Also components are displayed depending on the state 
    of the program.
    
List of functions:
  - App, HandleChange1, HandleChange2

Procedure:
  - Hide and show elements according to the values of radio buttons
   
*/

import React from 'react';
import './App.css';
import { FileUploader1 } from "./components/FileUploader1"
import { FileUploader2 } from "./components/FileUploader2"


function App() {

  //Show and hide elements depending on the value of radio button
  function HandleChange1(event){
    var x = document.getElementById("geneList");
    var y = document.getElementById("xGenomics");

    x.style.display = "block";
    y.style.display = "none";
  }

  function HandleChange2(event){
    var x = document.getElementById("xGenomics");
    var y = document.getElementById("geneList");

    x.style.display = "block";
    y.style.display = "none";    
  }
  //Structure of the web interface
  return (  
    <div className="App">

      <div id="main">
        <header>    
          <p>Select the input files:</p>
          Ranked gene list<input type="radio"  name="group1" onChange={HandleChange2} /><br></br>
          10X genomics files<input type="radio" name="group1" onChange={HandleChange1} />   
        <div hidden id = "geneList">
          <FileUploader1 />
        </div>
        <div hidden id = "xGenomics">
          <FileUploader2 />
        </div>
        </header>
      </div>

      <div hidden id="load">
        <header>
          <p>Running the analysis. Results are written to a file when analysis is ready.</p>         
        </header>
      </div>

      <div hidden id="results">
        <header>
          <p>Results are stored in /scanpy-gseapy_pipeline/data/GSEA_Prerank folder</p>
          <a href="http://localhost:3000">Home page</a>    
        </header>
      </div>
         
    </div>
  );
}

export default App;
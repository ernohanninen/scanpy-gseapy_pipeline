/*
Title: FileUploader1.js
Date: 2021-03-09
Author: Erno Hänninen

Description:
  - This script submits the files inputted to the server.
List of functions:
  - FileUploader1

Procedure:
  - Read the input from the user. When form is submitted, send the input to the server.
  - Display elements to the user
*/

import React, {useState} from 'react';
import axios from 'axios';


export const FileUploader1 = () => {

    //initialize the variables
    const [file1, setFile1] = useState([])
    const [file2, setFile2] = useState()
    const [num, setNum] = useState()

    //After file has uploaded to web page, read the file to variable
    function handleChange1(event) {
      setFile1(event.target.files)    
    }
    function handleChange2(event) {
      setFile2(event.target.files[0])
    }

    function handleChange3(event){
      setNum(event.target.value)
    }

    //When submit button is clicked this function is executed
    //THis function sends the file t server
    function handleSubmit1(event) {
      
      event.preventDefault()
      //Define the url where the files are send
      const url = '/uploadFile'; 
      //Uploading the files to formData object
      const formData1 = new FormData();   
      formData1.append('file1', file1[0]);
      formData1.append('file2', file1[1]);
      formData1.append('file3', file1[2]);
      formData1.append("geneSetFile", file2)
      formData1.append("numPlots", num)
      //displaying new components to user 
      document.getElementById('main').style.display = 'none';
      document.getElementById('load').style.display = 'block';

      //send the files to server
      axios.post(url, formData1).then((response) => {
        if(response.data == "error"){
          //If error display the error message to user and display components
          alert("Error when performing the analysis, please check your input files and try again.")
          document.getElementById('main').style.display = 'block';
          document.getElementById('load').style.display = 'none';
        }
        else{
          //When server returns the results, displaying new components to user  
          document.getElementById('load').style.display = 'none';
          document.getElementById('results').style.display = 'block';
        }
        console.log("Analysis is ready")
         
        /*
        This code is for displaying the image on the screen (doesn't work)
        console.log(response)
        
        listOfImages = []
        const obj = JSON.parse(JSON.stringify(response));
        
        for(var i=0;i<obj.data.files.length;i++){
            listOfImages.push(obj.data.files[i])
            console.log(obj.data.files[i])
            image = obj.data.files[i]
        }*/      
    });
  }
    //Compoent structure
    return(
        <div className='fileUploader1'>          
                {
                // matrix.mtx, barcodes.tsv, features.tsv (genes.tsv)
                }               
                <br></br>
                <form onSubmit={handleSubmit1}>          
                  <p>Submit three 10xGenomics files (matrix.mtx, barcodes.tsv and features.tsv/genes.tsv):&nbsp;&nbsp;<input multiple type="file" accept=".mtx, .tsv" onChange={handleChange1}/></p>
                  <p>Submit gene set:&nbsp;&nbsp;<input type="file" onChange={handleChange2}/></p>
                  <p>Number of GSEA plots as output: <input type="text" pattern="[0-9]*" onInput={handleChange3} size="5" title="Only numbers are accepted." /> </p>
                  <button type="submit" disabled={!num || !file1 || !file2} >Run analysis</button><br></br>      
                </form>      
            
        </div>
    );
    
};
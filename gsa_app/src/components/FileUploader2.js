/*
Title: FileUploader2.js
Date: 2021-03-09
Author: Erno Hänninen

Description:
  - This script submits the files inputted to the server.
    
List of functions:
  - FileUploader2
Procedure:
  - Read the input from the user. When form is submitted, send the input to the server.
  - Display elements to the user
*/

import React, {useState} from 'react';


export const FileUploader2 = () => {
  //initialize the variables
  const [file1, setFile1] = useState()
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
  function handleSubmit(event) {
    
    event.preventDefault()
    //Define the url where the files are send
    const url = '/uploadRankedFile';
    const formData1 = new FormData();
    const formData2 = new FormData(); 
    //Uploading the files to formData object
    formData1.append('file1', file1[0]);
    formData1.append("geneSetFile", file2)
    formData1.append("numPlots", num)
    //displaying new components to user 
    document.getElementById('main').style.display = 'none';
    document.getElementById('load').style.display = 'block';
   
     //send the files to server
    axios.post(url, formData1).then((response) => {
      console.log(response.data)
      if(response.data == "error"){
                  //If error display the error message to user and display components
        alert("Error when performing the analysis, please check your input files and try again.")
        document.getElementById('main').style.display = 'block';
        document.getElementById('load').style.display = 'none';
      }
       //When server returns the results, displaying new components to user  
      else{
        document.getElementById('load').style.display = 'none';
        document.getElementById('results').style.display = 'block';
      }  
      
    });
    }
    //Compoent structure
    return(
        <div className='fileUploader1'>          
                
                <br></br>
                <form onSubmit={handleSubmit}>
                  <p>Submit ranked gene list:&nbsp;&nbsp;<input type="file" onChange={handleChange1}/></p>
                  <p>Submit gene set:&nbsp;&nbsp;<input type="file" onChange={handleChange2}/></p>
                  <p>Number of GSEA plots as output: <input type="text" pattern="[0-9]*" onInput={handleChange3} size="5" title="Only numbers are accepted." /> </p>
                  <button type="submit" disabled={!num || !file1 || !file2} >Run analysis</button><br></br>      
                </form>      
        </div>
    );
    
};
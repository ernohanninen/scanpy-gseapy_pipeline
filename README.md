# scanpy-gseapy pipeline

This application is a SCANPY-GSEAPY pipeline with a web interface. The SCANPY-GSEAPY pipeline is written using Python (3.8.5). Flask server connects the pipeline and ReactJS frontend. The application accepts ranked gene list or 10xGenomics gene expression dataset as input. If ranked list is inputted only GSEA part of the pipeline is executed. If 10xGenomics gene expression dataset is inputted ranked gene list is computed and thereafter GSEA is performed to the ranked list. The pipeline outputs enrichment plots.
<br/><br/>

Setup the application:
1. Open terminal
2. Clone the repository to your computer:
```
git clone https://github.com/ernohanninen/scanpy-gseapy_pipeline.git
```
3. Navigate:
```
cd scanpy-gseapy_pipeline
```
4. Set up conda virtual environment:
```
conda env create -f gsea_env.yml
```
5. Activate the conda environment:
```
conda activate gsea_env
```
6. Navigate:
```
cd gsa_app
```
7. Start the Flask server:
```
yarn run start-api
```
8. Open new terminal window and navigate to folder: ~/scanpy-gseapy_pipeline/gsa_app
9. Activate the conda environment:
```
conda activate gsea_env
```
10. Start the ReactJS frontend:
```
yarn start
```
11. Application is running in: http://localhost:3000/
<br/><br/>

Using the application:
1. Select the input file type using radio button:
 - Input types:
   - In ranked gene list (.csv) genes should be ranked according to their differential expression. In the inputted list genes should be in column one and the ranking metric in column two. Example ranked gene list is provided. It is named ranked.csv and can be found in input_data folder.
   - 10xGenomics files refers to gene expression dataset (HDF5 Format). 10xGenomics gene expression dataset consists of three files and are named in the following way: matrix.mtx, barcodes.tsv and features.tsv or genes.tsv. Example 10xGenomics dataset can be found in input_data/hg folder. Submit all the three files.
2. Select the gene set: Two example gene sets are provided. KEGG_2021_Human.txt and NCI-60_Cancer_Cell_Lines.txt files can be found in input_data folder
3. Choose the number of GSEA plots wanted as output.
4. Run the analysis by pressing the Run analysis button. The pipeline contains a lot of computation, thus it takes a while to run. "Starting the analysis" text is printed to the terminal window, where Flask server is running, if the application runs correctly.
5. The results (GSEA plots) are written to /scanpy-gseapy_pipeline/data/GSEA_Prerank folder

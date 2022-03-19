#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: gsea.py
Date: 2021-03-07
Author: Erno Hänninen

Description:
    This script consists of two functions. Function run_sc_analysis get's 10xGenomics files as a input and performs clustering to the dataset, finds marker genes and
    outputs a ranked list. Function run_gsea performs gene set enrichment to the ranked list and plots the result.

List of functions:
    -    run_sc_analysis
    -    run_gsea
List of "non standard" modules:
    -    numpy, pandas, scanpy, gseapy
    
Error handling:
    - reading the 10xGenomics files happens inside try clause, if error occurs during reading, error message is printed to the user
    - GSEA is performed inside try clause, if error occurs during reading, error message is printed to the user
    
Procedure for run_sc_analysis function:
    1. Read the input files
    2. Filter the dataset
    3. Perform pca to the dataset
    4. Clustering the genes and finding marker genes for different clusters
    5. Rank the genes according to expression level and return the ranked list

Procedure for run_gsea function:
    1. Rename the gene set file inputted by the user (this step needs to be done to get the gsea run locally)
    2. Perform the gene set enrichment analysis 
"""

import os
import numpy as np
import pandas as pd
import scanpy as sc
import gseapy as gseapy

"""
#Input is 10x genomics file:
#matrix.mtx number of transcripts for a given gene in a given cell
#barcodes.tsv file contains cell barcodes in our data
#genes.tsv file contains information of gene expression
"""

#Single cell analysis part of the pipeline
def run_sc_analysis():

    #Reading the 10xGenomics files submitted by user
    #If error occurs during reading the files, the error is handled
    try:
        adata=sc.read_10x_mtx("hg/")
    except:
        return "error"
    else:

        #MAking the index unique
        adata.var_names_make_unique()
    
        #Basic filtering of the data
        sc.pp.filter_cells(adata, min_genes=200)
        sc.pp.filter_genes(adata, min_cells=3)

        #Annotating the group of mitocondrial genes and computing metrics
        adata.var["mt"] = adata.var_names.str.startswith("MT-")
        sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)

        #Filtering 
        #Setting the filtering limits
        upper_limit = np.quantile(adata.obs.n_genes_by_counts.values, .9976)
        #lower_limit = np.quantile(adata.obs.n_genes_by_counts.values, .02)

        #Filtering from upper and lower limit
        adata = adata[adata.obs.n_genes_by_counts < upper_limit, :]
        #adata = adata[adata.obs.n_genes_by_counts > lower_limit, :]
        #Filtering the mitocondrial counts
        adata = adata[adata.obs.pct_counts_mt < 5, :]

        #Filtering using count values
        #adata = adata[adata.obs.n_genes_by_counts < 2500, :]
        #adata = adata[adata.obs.pct_counts_mt < 5, :]

        #Normalixe count data
        sc.pp.normalize_total(adata, target_sum=1e4)

        #logarithmize the data:
        sc.pp.log1p(adata)

        #identify highly-variable-genes
        sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5) #default values are used

        #Save raw data before further filtering
        adata.raw = adata

        #filter out all of the genes that are highly variable
        adata=adata[:, adata.var.highly_variable]

        #Regress out effects of total counts per cell and the percentage of mitochondrial genes expressed
        sc.pp.regress_out(adata, ["total_counts", "pct_counts_mt"])

        #Scaling each gene to unit variance
        sc.pp.scale(adata, max_value=10)

        #PCA
        sc.tl.pca(adata, svd_solver="arpack")

        #Computing the neighborhood graph
        sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)

        #Calculating umap
        sc.tl.umap(adata)

        #Clustering neighborhood graph
        #Leiden algorithm is used to calculate the clusters
        sc.tl.leiden(adata)
        #sc.pl.umap(adata, color=['leiden'])
        #Plot the umap

        #Finding marker genes for different clusters
        #rankg_genes_group function perfoms differential experssion analysis
        #From different statistical methods wilcoxon was used
        """
        #sc.tl.rank_genes_groups(adata, 'leiden', method='t-test')
        #sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)

        #sc.tl.rank_genes_groups(adata, 'leiden', method='logreg')
        #sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)
        """

        sc.tl.rank_genes_groups(adata, 'leiden', method='wilcoxon', key_added = "wilcoxon")
        #sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False, key="wilcoxon")

        #Get significant differently expressed genes
        gene_rank = sc.get.rank_genes_groups_df(adata, group=None, key='wilcoxon')[['names','scores', "pvals_adj", "group"]]
        gene_rank.sort_values(by=['scores'], inplace=True, ascending=False)

        # calculate_qc_metrics will calculate number of cells per gene
        sc.pp.calculate_qc_metrics(adata, percent_top=None, log1p=False, inplace=True)

        # filter for genes expressed in at least 30 cells.
        gene_rank = gene_rank[gene_rank['names'].isin(adata.var_names[adata.var.n_cells_by_counts>30])]
        
        #print(gene_rank.iloc[:,[0,1]])
        #gene_rank.to_csv("ranked.csv", sep="\t", index=False)
        
        #Ranked gene list is ready for GSEA analysis
        return gene_rank

#GSEA part of the pipeline
def run_gsea(gene_rank, numPlots):
    gene_set = ""
    path = os.getcwd() + "/geneSet/"
    folder = os.fsencode(path)
    #This loop renames the input gene sets. This step is needed, because gsea runs locally if files are ending .gmt
    for file in os.listdir(folder): 
        os.rename(path + os.fsdecode(file), path + os.fsdecode(file) + ".gmt")

    #Updating the gene_set variable with the gene set path
    for file in os.listdir(folder):      
            gene_set = "./geneSet/" + os.fsdecode(file)     
     
    #Running the gsea analysis and plotting the results
    #If error occurs during gsea, the error is handled
    try:
        res = gseapy.prerank(rnk=gene_rank.iloc[:,[0,1]], gene_sets=gene_set, format="png", graph_num=numPlots)
        terms = res.res2d.index
        gseapy.gseaplot(rank_metric=res.ranking, term=terms[0], **res.results[terms[0]])
    except:
        return "error"
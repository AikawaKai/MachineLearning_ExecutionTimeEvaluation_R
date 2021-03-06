library(caret); 	## to model
library(HEMDAG); 	## to create stratified fold (do.stratified.cv.data.single.class)



## SERVER\LOCAL DATA PATH SETTING
server.bool <- FALSE

#LIBS AND PATHS
if(server.bool){
  lib.dir <- "/home/modore/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/lib/"
  annotation.dir <- "/data/GO_EXP/"
  net.dir <- "/home/modore/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/"
  scores.dir <- perf.dir <- "/home/modore/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/";
}else{
  lib.dir <- "/home/kai/Documents/Unimi/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/lib/"
  annotation.dir <- "/home/kai/Documents/Unimi/Tesi-Bioinformatica/";
  net.dir <- "/home/kai/Documents/Unimi/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/data/"; 
  scores.dir <- perf.dir <- "/home/kai/Documents/Unimi/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/" ;
}

source(paste(lib.dir, "caret.metrics.R", sep =""));## to use customize performance metrics ("precrec" pkg)
source(paste(lib.dir, "utility.R", sep =""));
source(paste(lib.dir, "R_CARET_MODELLING.R", sep = "")); ## to call the high-level fun caret.training
args <- commandArgs(trailingOnly = TRUE)
algorithm <- args[1]
curr_onto <- args[2]

## GENERAL PARAMETERS SETTING
net.file <- "pca.rda";
ann.file <- paste0("/6239_CAEEL/6239_CAEEL_GO_", curr_onto, "_ANN_STRING_v10.5_20DEC17.rda");
PreProc <- TRUE;
norm <- TRUE;
n <- 9;
kk <- 10;
defGrid	<- getCurrentAlgoGrid(algorithm);
cutoff <- 0.5;
summaryFunction <- AUPRCSummary;
metric <- "AUC"; 
pkg <- "precrec";
seed <- 1;

# LOADING DATA
load(file=paste(annotation.dir, ann.file, sep=""));
load(file=paste(net.dir, net.file, sep=""));
W <- pca$x

#SELECT BY VARIANCE
W_90 <- W[,1:1000]
W_70 <- W[,1:100]
W_50 <- W[,1:15]
W_variance <- list(W_50, W_70, W_90)
variance_names <- list("variance_50", "variance_70", "variance_90")

# selected classes for replicability
set.seed(seed)
ann_select <-ann[,colSums(ann)>9]
ann_sample <- sample(colnames(ann_select), 10)
print(ann_sample)
classes <- ann_select[,ann_sample]


## MODELING by CARET
for(i in seq(1:3)){
  curr_variance <- variance_names[[i]]
  if(algorithm == "LogitBoost" || algorithm == "rf"){
    defGrid = defGridModifier(algorithm, curr_variance)
  }
  W <- W_variance[[i]]
  curr_csv_name <- paste0(curr_onto, "_", curr_variance, "_", algorithm, ".csv")
  vals <- system.time(caret.training(
    W=W, ann=classes, PreProc=PreProc, 
    n=n, norm=norm, kk=kk, seed=seed, algorithm=algorithm, 
    summaryFunction=summaryFunction, defGrid=defGrid, cutoff=cutoff, 
    metric=metric, pkg=pkg, scores.dir=scores.dir, perf.dir=perf.dir, 
    variance=curr_variance, csv_name=curr_csv_name)
  )
}



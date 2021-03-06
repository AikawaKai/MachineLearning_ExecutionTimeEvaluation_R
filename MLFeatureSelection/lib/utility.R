library(stats)
library(Rcpp)

getCurrentAlgoGrid <- function(algo){
  if(algo == "gaussprPoly"){
    return(data.frame(degree = 1, scale = 1))
  }
  if(algo == "mlp"){
    return(data.frame(size = 5))
  }
  if(algo == "knn"){
    return(data.frame(k=9))
  }
  if(algo == "svmLinear"){
    return(data.frame(C = 1))
  }
  if(algo == "svmRadial"){
    return(data.frame(C = 1, sigma = 1))
  }
  if(algo == "xgbLinear"){
    return(data.frame(nrounds = 15 , lambda = 1, alpha = 0, eta = 0.3))
  }
  if(algo == "rf"){
    return(data.frame(mtry = 32))
  }
  if(algo == "C5.0"){
    return(data.frame(trials = 1, model = "tree" , winnow =FALSE ))
  }
  if(algo == "LogitBoost"){
    return(data.frame(nIter = 1000))
  }
  if(algo == "glmnet"){
    return(data.frame(alpha = 1, lambda = 100))
  }
  if(algo == "randomGLM"){
    return(data.frame(maxInteractionOrder = 1))
  }
  if(algo == "treebag"){
    return(data.frame(parameter = "none"))
  }
  if(algo == "AdaBoost.M1"){
    return(data.frame(mfinal = 100 , maxdepth = 30 , coeflearn = "Breiman"))
  }
}

defGridModifier <- function(algorithm, curr_variance){
  if(algorithm=="LogitBoost"){
    if (curr_variance == "variance_50"){
      return(data.frame(nIter = 15))
    }else if(curr_variance == "variance_70"){
      return(data.frame(nIter = 100))
    }else {
      return(data.frame(nIter = 1000))
    }
  }else{
    if (curr_variance == "variance_50"){
      return(data.frame(mtry = 4))
    }else if(curr_variance == "variance_70"){
      return(data.frame(mtry = 10))
    }else {
      return(data.frame(mtry = 32))
    }
  }
}

ptestCalculation <- function(col_vals, col_classes){
  curr_data <- data.frame(vals = col_vals, classes = as.factor(col_classes))
  p_value <- t.test(vals ~ classes, data=curr_data)[["p.value"]]
  return(c(p_value))
}
tryCatch({sourceCpp(file=paste("/home/kai/Documents/Unimi/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/", "fastIter.cpp", sep=""))},
         error = function(err){
           sourceCpp(file=paste("/home/modore/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/", "fastIter.cpp", sep=""))
         })
iterTtestCalculation <-function(W, ann){
  for(i in 1:ncol(ann)){
    for(j in 1:ncol(W)){
      ptestCalculation(W[,j], ann[,i])
    }
  }
}
library(factoextra)

load(file="/home/kai/Documents/Unimi/Tesi-Bioinformatica/BioinformaticThesis/MLFeatureSelection/data/pca.rda")
PoV <- (pca$sdev^2)/sum(pca$sdev^2)

fviz_eig(pca, ncp = 50)
curr_var <- 0
count <- 0
th <- 0.7
for(i in seq(1:length(PoV))){
  curr_var <- curr_var + PoV[[i]]
  count <- count + 1
  print(curr_var)
  if (curr_var >= th)
    break
}
print(count)

curr_var <- 0
count <- 0
count_th <- 1000
for(i in seq(1:length(PoV))){
  curr_var <- curr_var + PoV[[i]]
  count <- count + 1
  print(curr_var)
  if (count >= count_th)
    break
}
print(curr_var)

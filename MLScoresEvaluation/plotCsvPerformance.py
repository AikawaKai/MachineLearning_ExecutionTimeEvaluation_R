import os, csv
from numpy import mean, std
import pandas as pd
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

colors = ["red", "blue", "green", "grey", "grey", "grey", "grey", "grey",
          "grey", "grey", "grey", "grey", "grey", "grey", "grey", "grey",
          "grey"]

def saveBoxPlot(list_data, list_names):
    fig = plt.figure(1, figsize=(20, 8))
    print(list_names)
    plt.xlabel("Algorithms", fontsize=15)
    plt.ylabel("AUPRC", fontsize=15)
    boxes = plt.boxplot(list_data, patch_artist=True)
    i=0
    for box in boxes["boxes"]:
        box.set_facecolor(colors[i])
        i+=1
    plt.xticks([i for i in range(1, len(list_names)+1)], list_names)
    plt.tick_params(labelsize=13)
    # Save the figure
    fig.savefig('box_plot_times.png', bbox_inches='tight')


if __name__ == '__main__':
    path = "./Performance_results/"
    csv_ = os.listdir(path)
    names = [c.split("_")[0] for c in csv_]
    print(names)

    dataframes = [pd.read_csv(path+csv) for csv in csv_]
    roc = dict()
    pr = dict()
    i = 0
    for dataframe in dataframes:
        algo = names[i]
        roc[algo] = [dataframe["AUROC"].values]
        pr[algo] = [dataframe["AUPRC"].values]
        i+=1
    for key, value in roc.items():
        print(key)
        max_val = max(value[0])
        min_val = min(value[0])
        mean_val = mean(value[0])
        std_val = std(value[0])
        print("max: ", max_val)
        print("min: ", min_val)
        print("mean: ", mean_val)
        print("std: ", std_val)
        roc[key]+=[max_val, min_val, mean_val, std_val]
    for key, value in pr.items():
        print(key)
        max_val = max(value[0])
        min_val = min(value[0])
        mean_val = mean(value[0])
        std_val = std(value[0])
        print("max: ", max_val)
        print("min: ", min_val)
        print("mean: ", mean_val)
        print("std: ", std_val)
        pr[key]+=[max_val, min_val, mean_val, std_val]


    box_plot_values = [val[0] for key, val in pr.items()]
    print(box_plot_values)
    if len(box_plot_values)<15:
        len_ = 15 - len(box_plot_values)
        for i in range(len_):
            box_plot_values.append([0])
            names.append("to_do")

    saveBoxPlot(box_plot_values, names)

    first_row = ["algo", "max_AUPRC", "min_AUPRC", "mean_AUPRC", "std_AUPRC"]
    with open("./prauc_.csv", "w") as f_:
        wr = csv.writer(f_, delimiter= ",")
        wr.writerow(first_row)
        for key, value in pr.items():
            wr.writerow([key, value[1], value[2], value[3], value[4]])

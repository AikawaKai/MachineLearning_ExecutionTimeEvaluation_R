import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import wilcoxon
from itertools import combinations


algo_done = ["TPR-DAGthreshold.free", "ISO-TPRthreshold.free", "GPAV", "HTD"]
dict_translate_hier_method = {"TPR-DAGthreshold.free": "TPR-TF", "ISO-TPRthreshold.free": "ISO-TPR-TF",
                              "GPAV": "GPAV", "HTD": "HTD", "flat": "flat"}

dict_metric = {"AUC": "AUROC", "PRC": "AUPRC", "FMM": "FMM"}
blues = [(30, 144, 255), (0, 191, 255), (135, 206, 250), (173, 216, 230), (240, 248, 255)]
blues = [[val/255 for val in tupl] for tupl in blues]
print(blues)


def changeFontSize(ax, label_font, tick_font, title_font):
    ax.title.set_fontsize(title_font)
    ax.xaxis.label.set_fontsize(label_font)
    ax.yaxis.label.set_fontsize(label_font)
    ax.tick_params(axis='both', which='major', labelsize=tick_font)


def normalize_name(name):
    if "flat" in name:
        return "flat"
    else:
        return dict_translate_hier_method[name.split("_")[0]]


def split_name(file_name):
    res = file_name.split("_")
    return res


def put_data_in_dict(curr_csv, onto, hier_method, splitted_name, dict_onto, metrics):
    #print(splitted_name)
    for key in curr_csv.keys():
        res = split_name(key)
        if len(res)==4:
            algo = res[0]+"_"+res[1]
            metric = res[2]
            fs = res[3]
        else:
            algo = res[0]
            metric = res[1]
            fs = res[2]
        metric = hier_method+"_"+metric
        if algo not in dict_onto[onto][fs]:
            dict_onto[onto][fs][algo] = dict()
            dict_onto[onto][fs][algo][metric] = list(curr_csv[key])
        elif metric not in dict_onto[onto][fs][algo]:
            dict_onto[onto][fs][algo][metric] = list(curr_csv[key])
        if metric not in metrics:
            metrics[metric] = 0
        else:
            metrics[metric] += 1


def fill_data_dict(curr_path, hier_algo, dict_onto, metrics):
    files = [(curr_path+file_, file_) for file_ in os.listdir(curr_path)
             if file_.endswith(".csv") and file_ != hier_algo+".csv"]
    print(files)
    for file_, file_name in files:
        file_name = file_name.split(".csv")[0]
        print(file_name)
        curr_csv = pd.read_csv(file_, sep="\t")
        splitted_name = split_name(file_name)
        onto = splitted_name[0]
        hier_method = splitted_name[1]
        put_data_in_dict(curr_csv, onto, hier_method, splitted_name[2:], dict_onto, metrics)


def wilcoxon_test_by_metric(algo_dict, dict_metrics, onto, key):
    num_row = len(algo_dict["FS"].keys())*2
    i = 0
    algo_dict_list = [algo for algo in algo_dict["FS"]]
    for algo in algo_dict_list:
        for fs in ["FS", "PCA"]:
            i += 1
            algo_vals_dict = algo_dict[fs][algo]
            names = [n for n in dict_metrics.keys() if key in n]
            names_1 = []
            count = 0
            for name in names:
                if "flat" in name:
                    count += 1
                    if count == 1:
                        names_1.append(name)
                else:
                    names_1.append(name)
            metric_values = [algo_vals_dict[metric] for metric in names_1]
            names_1 = [normalize_name(n) for n in names_1]
            zip_metric_names = zip(metric_values, names_1)
            metric_values_by_comb = combinations(zip_metric_names, 2)
            for comb in metric_values_by_comb:
                print(algo, onto, key, fs, "Comparison between: ", comb[0][1],"," , comb[1][1])
                print("p_value", wilcoxon(comb[0][0], comb[1][0]))


def wilcoxon_test(algo_dict, dict_metrics, onto):
    wilcoxon_test_by_metric(algo_dict, dict_metrics, onto, "AUC")
    wilcoxon_test_by_metric(algo_dict, dict_metrics, onto, "PRC")
    # wilcoxon_test_by_metric(algo_dict, dict_metrics, onto, "FMM")


def get_wilcoxon_test_from_dict_data(dict_onto, dict_metrics):
    for onto in ["BP", "MF", "CC"]:
        wilcoxon_test(dict_onto[onto], dict_metrics, onto)


if __name__ == '__main__':
    path_ = "/home/kai/Documenti/UNIMI/BioinformaticThesis/Ensemble/hierPerf"
    dict_onto = {key: {"FS": dict(), "PCA": dict()} for key in ["BP", "MF", "CC"]}
    dict_metrics = dict()
    dict_algos = dict()
    for hier_algo in algo_done:
        curr_path = path_+"/"+hier_algo+"/"
        fill_data_dict(curr_path, hier_algo, dict_onto, dict_metrics)
    get_wilcoxon_test_from_dict_data(dict_onto, dict_metrics)


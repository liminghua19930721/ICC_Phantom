import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import json
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

def heat_map_plot(data, x_label=None, y_label=None, save_dict=None):
    if x_label is None:
        x_label = [i for i in range(data.shape[1])]
    if y_label is None:
        y_label = [i for i in range(data.shape[0])]
    # 定义颜色渐变的断点
    colors = [(1, 1, 1), (0.8, 1, 0.8), (0, 0.5, 0)]  # R -> G -> B
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors, N=100)

    fig, ax = plt.subplots(figsize=(10, 10))

    # 使用pcolormesh绘制热度图，并为每个单元格添加黑色边框
    x = np.arange(data.shape[1] + 1)
    y = np.arange(data.shape[0] + 1)
    c = ax.pcolormesh(x, y, data, cmap=cmap, edgecolor='black', linewidth=4, vmin=0.5, vmax=1, shading='auto')

    height = ax.get_window_extent().height
    txt_fontsize = height / max(len(x), len(y)) * 0.2
    # 在每个单元格上显示数值
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j] < 0.75:
                if data[i, j] < 0:
                    ax.text(j + 0.5, i + 0.5, f"{0:.2f}", ha='center', va='center', color='black', fontsize=txt_fontsize)
                else:
                    ax.text(j + 0.5, i + 0.5, f"{data[i, j]:.2f}", ha='center', va='center', color='black', fontsize=txt_fontsize)

    # 添加颜色条
    cbar = fig.colorbar(c, ax=ax, ticks=[0.5, 0.75, 0.85, 1], fraction=0.046, pad=0.04, shrink=0.8)
    cbar.ax.set_yticklabels(['0.5', '0.75', '0.85', '1'])

    # 设置轴的限制和刻度
    ax.set_aspect('equal')
    ax.set_xlim(0, data.shape[1])
    ax.set_ylim(0, data.shape[0])
    ax.set_xticks(np.arange(data.shape[1]) + 0.5)
    ax.set_yticks(np.arange(data.shape[0]) + 0.5)
    ax.xaxis.tick_top()   
    ax.set_xticklabels(x_label, fontdict={'fontsize': 10, 'fontfamily': 'serif'}, rotation=90)
    ax.set_yticklabels(y_label, fontdict={'fontsize': 10, 'fontfamily': 'serif'})

    ax.set_xticks(np.arange(data.shape[1] + 1), minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)

    # plt.show()
    
    if save_dict is not None:
        description = save_dict.get('description', 'Unknow')
        fig.text(0.5, -0.1, description, ha='center', va='center', color='black', fontsize=15, transform=ax.transAxes)

        save_root = save_dict.get('save_root', os.getcwd())
        if not os.path.exists(save_root):
            os.makedirs(save_root)
        save_file_name = save_dict.get('save_file_name', 'result.png')
        save_path = os.path.join(save_root, save_file_name)
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


with open('filters.txt', 'r') as f:
    unique_fliters = [line.strip() for line in f]

with open('features.txt', 'r') as f:
    categories_parameters = json.load(f)

print(unique_fliters)
print(categories_parameters)


data_root = 'results_wholeset/'
save_root = 'test_test_result_fig/result_heatmap_wholeset_repro/'
for sub_root in os.listdir(data_root):
    #loop for generate figs
    sub_data_root = os.path.join(data_root, sub_root)
    for key in categories_parameters.keys():
        plot_filters = unique_fliters
        plot_features = categories_parameters[key]
        plot_data = []
        for fl in plot_filters:
            row_data = []
            for ft in plot_features:
                f_name = fl + '_' + key + '_' + ft +'.csv'
                path = os.path.join(sub_data_root, f_name)
                data = pd.read_csv(path)
                icc_value = data[data['Type'] == 'ICC3k']['ICC'].values[0]
                row_data.append(icc_value)
            plot_data.append(row_data)

        plot_data = np.array(plot_data)
        plot_data = plot_data.astype(float)
        x_label = plot_features
        y_label = plot_filters

        save_dict = {'description': key,
                        'save_root': os.path.join(save_root, sub_root),
                        'save_file_name': fl + '_' + key + '.png'}
        heat_map_plot(plot_data, x_label=x_label, y_label=y_label, save_dict=save_dict)

    #######usable
    # colors = [(1, 1, 1), (0, 0.5, 0)]  # White to dark green
    # cmap_name = 'white_to_green'
    # cm_white_to_green = LinearSegmentedColormap.from_list(cmap_name, colors)

    # plot_data = np.array(plot_data)
    # plot_data = plot_data.astype(float)
    # plot_data_average = np.mean(plot_data)
    # featrue_average[key] = plot_data_average
    # fig, ax = plt.subplots(figsize=(12, 10))
    # cax = ax.matshow(plot_data, cmap=cm_white_to_green)

    # description = key
    # fig.text(0.5, -0.1, description, ha='center', va='center', color='black', fontsize=15, transform=ax.transAxes)

    # # Setting labels
    # ax.set_xticks(np.arange(plot_data.shape[1]+1)-.5, minor=True)
    # ax.set_yticks(np.arange(plot_data.shape[0]+1)-.5, minor=True)
    # ax.grid(which="minor", color="white", linestyle='-', linewidth=2)
    # ax.tick_params(which="minor", size=0)
    # ax.grid(which='major', visible=False)
    # ax.set_xticks(np.arange(len(plot_features)))
    # ax.set_yticks(np.arange(len(plot_filters)))
    # ax.set_xticklabels(plot_features, rotation=90, fontsize=10)
    # ax.set_yticklabels(plot_filters)

    # # Displaying colorbar
    # fig.colorbar(cax, fraction=0.046, pad=0.04)

    # # Showing the heatmap
    # # plt.show()
    # save_root = 'test_result_fig/result_heatmap_sub2_repro'
    # save_sub = os.path.basename(data_root.rstrip("/"))
    # save_root = os.path.join(save_root, save_sub)
    # if not os.path.exists(save_root):
    #     os.makedirs(save_root)
    # save_fig_name = key + '.png'
    # save_path = os.path.join(save_root, save_fig_name)
    # fig.savefig(save_path, dpi=300, bbox_inches='tight')
    # plt.close()
    ################

# # Extracting keys and values
# x_labels = list(featrue_average.keys())
# y_values = list(featrue_average.values())

# fig, ax = plt.subplots(figsize=(10, 6))
# # Plotting
# plt.figure(figsize=(10, 6))
# plt.bar(x_labels, y_values, color='blue', alpha=0.7)
# plt.xlabel("Features class")
# plt.ylabel("Mean ICC")
# # plt.title("Feature classes")
# plt.show()
# save_fig_name = 'Feature class' + '.png'
# save_path = os.path.join(save_root, save_fig_name)
# fig.savefig(save_path, dpi=300, bbox_inches='tight')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import json
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

# np.random.seed(0)
# data1 = np.random.rand(10, 10)
# data2 = np.random.rand(10, 10)
# data3 = np.random.rand(10, 10)
# data4 = np.random.rand(10, 10)

def horizontal_white_gap_heat_map_plot_v2(datasets, gap=1, y_label=None, x_label=None, title='test'):
    # Combine the datasets with gaps in between horizontally
    combined_data = []
    for data in datasets:
        combined_data.append(data)
        combined_data.append(np.full((data.shape[0], gap), -1))  # Using -1 for the white gap
    combined_data = np.hstack(combined_data[:-1])  # remove the last gap

    if y_label is None:
        y_label = [i for i in range(combined_data.shape[0])]
    
    # Remaining parts of the function are unchanged, with some modifications to handle the combined data and the white gap
    colors = [(1, 1, 1), (0.8, 1, 0.8), (0, 0.8, 0)]  # R -> G -> B
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors, N=100)

    fig, ax = plt.subplots(figsize=(30, 18))
    x = np.arange(combined_data.shape[1] + 1)
    y = np.arange(combined_data.shape[0] + 1)
    c = ax.pcolormesh(x, y, combined_data, cmap=cmap, edgecolor='none', linewidth=0.5, vmin=0, vmax=1, shading='auto')

    height = ax.get_window_extent().height
    txt_fontsize = height / max(len(x), len(y)) * 0.2
    for i in range(combined_data.shape[0]):
        for j in range(combined_data.shape[1]):
            if 0 <= combined_data[i, j] < 0.75:
                ax.text(j + 0.5, i + 0.5, f"{combined_data[i, j]:.2f}", ha='center', va='center', color='black', fontsize=txt_fontsize)

    # Add colorbar
    cbar = fig.colorbar(c, ax=ax, ticks=[0, 0.5, 0.75, 1], fraction=0.046, pad=0.04, shrink=0.3)
    cbar.ax.set_yticklabels(['0', '0.5', '0.75', '1'])
    
    ax.set_aspect('equal')
    # Set x-axis ticks and labels to indicate each 10x10 matrix
    xlabel_len = len(datasets)
    xlabel_initial = datasets[0].shape[1]
    tick_positions_numbers = []
    for i in range(xlabel_len):
        tick_positions_numbers += list(range(i * xlabel_initial + i * gap, (i+1) * xlabel_initial + i * gap))
    ax.set_xticks([x + 0.5 for x in tick_positions_numbers])

    if x_label == None:
        ax.set_xticklabels([str(i+1) for i in range(xlabel_initial)] * xlabel_len)
    
    ax.set_xticklabels(x_label * xlabel_len, rotation=90, fontdict={'fontsize': 5, 'fontfamily': 'serif'})
    ax.xaxis.tick_top() 
    
    ax.set_yticks(np.arange(combined_data.shape[0]) + 0.5)
    ax.set_yticklabels(y_label, fontdict={'fontsize': 5, 'fontfamily': 'serif'})

    fig.text(0.5, -0.1, title, ha='center', va='center', color='black', fontsize=15, transform=ax.transAxes)

    group_labels = ['mask_group_1', 'mask_group_2', 'mask_group_3', 'mask_group_all']
    group_label_positions = [xlabel_initial // 2, 
                             xlabel_initial // 2 + xlabel_initial + gap, 
                             xlabel_initial // 2 + 2 * xlabel_initial + 2 * gap, 
                             xlabel_initial // 2 + 3 * xlabel_initial + 3 * gap]
    for label, position in zip(group_labels, group_label_positions):
        ax.text(position, -0.5, label, ha='center', va='center', color='black', fontsize=5)

    save_data_root = '/home/ericlee/RF/modify_result_fig/result_heatmap_mask/subset2/'
    if not os.path.exists(save_data_root):
        os.mkdir(save_data_root)
    save_file_name = title + '.png'
    save_path = os.path.join(save_data_root, save_file_name)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

with open('filters.txt', 'r') as f:
    unique_fliters = [line.strip() for line in f]

with open('features.txt', 'r') as f:
    categories_parameters = json.load(f)


print(unique_fliters)
print(categories_parameters)

data_root = ['result_masks/subset2_mask_group1',
             'result_masks/subset2_mask_group2',
             'result_masks/subset2_mask_group3',
             'results_subset2/result_1']

for key in categories_parameters.keys():
    plot_filters = unique_fliters
    plot_features = categories_parameters[key]
    dataset = []
    for d_root in data_root:
        sub_dataset = []
        for fl in plot_filters:
            row_data = []
            for ft in plot_features:
                f_name = fl + '_' + key + '_' + ft +'.csv'
                path = os.path.join(d_root, f_name)
                data = pd.read_csv(path)
                icc_value = data[data['Type'] == 'ICC3k']['ICC'].values[0]
                row_data.append(icc_value)
            sub_dataset.append(row_data)
        sub_dataset = np.array(sub_dataset)
        sub_dataset = sub_dataset.astype(float)
        dataset.append(sub_dataset)
        sub_dataset = []

    print(dataset[0].shape)
    print(len(dataset))
    horizontal_white_gap_heat_map_plot_v2(dataset, gap=1, y_label=unique_fliters, title=key, x_label=plot_features)


# def horizontal_white_gap_heat_map_plot_v2(datasets, gap=1, y_label=None):
#     # Combine the datasets with gaps in between horizontally
#     combined_data = []
#     for data in datasets:
#         combined_data.append(data)
#         combined_data.append(np.full((data.shape[0], gap), -1))  # Using -1 for the white gap
#     combined_data = np.hstack(combined_data[:-1])  # remove the last gap

#     if y_label is None:
#         y_label = [i for i in range(combined_data.shape[0])]
    
#     # Remaining parts of the function are unchanged, with some modifications to handle the combined data and the white gap
#     colors = [(1, 1, 1), (0.8, 1, 0.8), (0, 0.8, 0)]  # R -> G -> B
#     cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors, N=100)

#     fig, ax = plt.subplots(figsize=(15, 8))
#     x = np.arange(combined_data.shape[1] + 1)
#     y = np.arange(combined_data.shape[0] + 1)
#     c = ax.pcolormesh(x, y, combined_data, cmap=cmap, edgecolor='none', linewidth=0.5, vmin=0, vmax=1, shading='auto')

#     height = ax.get_window_extent().height
#     txt_fontsize = height / max(len(x), len(y)) * 0.2
#     for i in range(combined_data.shape[0]):
#         for j in range(combined_data.shape[1]):
#             if 0 <= combined_data[i, j] < 0.75:
#                 ax.text(j + 0.5, i + 0.5, f"{combined_data[i, j]:.2f}", ha='center', va='center', color='black', fontsize=txt_fontsize)

#     # Add colorbar
#     cbar = fig.colorbar(c, ax=ax, ticks=[0, 0.5, 0.75, 1], fraction=0.046, pad=0.04, shrink=0.5)
#     cbar.ax.set_yticklabels(['0', '0.5', '0.75', '1'])
    
#     ax.set_aspect('equal')
#     # Set x-axis ticks and labels to indicate each 10x10 matrix
#     xlabel_len = len(datasets)
#     xlablel_initial = datasets[0].shape[1]
#     tick_positions_numbers = []
#     for i in range(xlabel_len):
#         tick_positions_numbers += list(range(i * xlablel_initial + i * gap, (i+1) * xlablel_initial + i * gap))
#     ax.set_xticks([x + 0.5 for x in tick_positions_numbers])
#     ax.set_xticklabels([str(i+1) for i in range(xlablel_initial)] * xlabel_len)
#     ax.xaxis.tick_top() 
    
#     ax.set_yticks(np.arange(combined_data.shape[0]) + 0.5)
#     ax.set_yticklabels(y_label, fontdict={'fontsize': 10, 'fontfamily': 'serif'})
#     ax.set_ylabel("Rows")

#     group_labels = ['group_1', 'group_2', 'group_3', 'group_4']
#     group_label_positions = [4.5, 14.5 + gap, 24.5 + 2*gap, 34.5 + 3*gap]
#     for label, position in zip(group_labels, group_label_positions):
#         ax.text(position, -0.5, label, ha='center', va='center', color='black', fontsize=txt_fontsize)

#     plt.savefig('/home/ericlee/Desktop/combined.png', dpi=300, bbox_inches='tight')
#     plt.show()
#     plt.close()

# # Calling the modified function with the three datasets
# horizontal_white_gap_heat_map_plot_v2([data1, data2, data3, data4])

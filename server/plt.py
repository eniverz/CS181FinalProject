import numpy as np
import matplotlib.pyplot as plt

def plot_histograms(data_list_b, data_list_f):
    bins = np.arange(40, 85, 2)
    labels = ['50', '150', '250']
    colors = ['deepskyblue', 'slateblue', 'coral']
    
    # Calculate histogram data
    hist_data_b = [np.histogram(data, bins=bins) for data in data_list_b]
    hist_data_f = [np.histogram(data, bins=bins) for data in data_list_f]
    
    # Get the bin edges and width
    bin_edges = hist_data_b[0][1]
    bin_width = bin_edges[1] - bin_edges[0] - 0.5
    
    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot the histograms for 'b' data
    for i, (hist, label, color) in enumerate(zip(hist_data_b, labels, colors)):
        bin_centers = bin_edges[:-1] + bin_width / 2
        hist_normalized = hist[0] / np.sum(hist[0])
        axs[1].bar(bin_centers + i * bin_width / len(data_list_b), hist_normalized, width=bin_width / len(data_list_b), label=f'dvi-iter {label}', color=color, edgecolor='none', alpha=1 if i != 1 else 0.5)
    
    axs[1].set_xlabel('Win step')
    axs[1].set_ylabel('Frequency')
    axs[1].set_title('Frequency of steps needed to win greedy (greedy first)')
    axs[1].set_xlim(40, 80)
    axs[1].legend()
    
    # Plot the histograms for 'f' data
    for i, (hist, label, color) in enumerate(zip(hist_data_f, labels, colors)):
        bin_centers = bin_edges[:-1] + bin_width / 2
        hist_normalized = hist[0] / np.sum(hist[0])
        axs[0].bar(bin_centers + i * bin_width / len(data_list_f), hist_normalized, width=bin_width / len(data_list_f), label=f'dvi-iter {label}', color=color, edgecolor='none', alpha=1 if i != 1 else 0.5)
    
    axs[0].set_xlabel('Win step')
    axs[0].set_ylabel('Frequency')
    axs[0].set_title('Frequency of steps needed to win greedy (DVI first)')
    axs[0].set_xlim(40, 80)
    axs[0].legend()
    
    plt.tight_layout()
    plt.show()

# Example usage
data_50_b = [62, 56, 70, 62, 50, 66, 64, 70, 56, 64, 56, 68, 68, 64, 56, 54, 60, 62, 66, 68, 58, 50, 72, 62, 70, 74, 70, 58, 64, 62, 50, 62, 60, 60, 72, 54, 66, 58, 62, 70, 62, 54, 54, 66, 60, 64, 58, 58, 62, 62, 64, 60, 62, 58, 58, 70, 54, 62, 64, 68, 60, 64, 52, 68, 60, 54, 46]
data_150_b = [66, 52, 52, 56, 46, 54, 68, 66, 62, 50, 52, 60, 50, 50, 52, 58, 60, 60, 60, 54, 48, 60, 46, 58, 64, 58, 74, 56, 50, 50, 58, 70, 56, 48, 58, 66, 60, 68, 62, 44, 54, 56, 52, 50, 36, 62, 52, 62, 50, 62, 54, 66, 46, 42, 46, 66, 62, 44, 64, 62, 52, 58, 50, 60, 58, 46, 52, 54, 50, 70, 58, 38, 44, 56, 64, 50, 48, 56, 56, 68, 38, 52, 62, 68, 52, 52, 52, 54, 54, 56, 60, 56, 56, 56]
data_250_b = [62, 66, 54, 62, 56, 56, 62, 66, 58, 56, 68, 52, 66, 64, 54, 56, 46, 52, 60, 52, 60, 54, 66, 62, 64, 58, 54, 62, 50, 64, 60, 60, 64, 56, 58, 52, 50, 58, 48, 68, 54, 60, 56, 54, 60, 58, 64, 56, 62, 64, 58, 68, 66, 50, 62, 56, 64, 64, 56, 48, 58, 72, 56, 52, 58, 60, 60, 68, 56, 56, 56, 50, 70, 64, 60, 56, 60, 56, 68, 58, 46, 58, 54, 58, 60, 60, 66, 56, 56, 68, 50, 56]
data_50_f =  [57, 59, 75, 55, 69, 53, 51, 59, 71, 65, 63, 67, 59, 73, 67, 67, 65, 67, 65, 79, 55, 63, 59, 61, 77, 59, 65, 73, 61, 77, 65, 63, 59, 57, 69, 63, 65, 65, 65, 55, 59, 61, 67, 69, 63, 65, 65, 65, 57, 61, 67, 53, 57, 67, 75, 73, 75, 65, 55, 55, 67, 67, 65, 59, 55, 71, 63, 65]
data_150_f = [67, 65, 59, 57, 59, 57, 59, 53, 57, 57, 53, 51, 53, 59, 51, 59, 57, 53, 63, 65, 59, 53, 63, 55, 61, 53, 61, 65, 51, 59, 55, 47, 59, 65, 57, 57, 51, 49, 55, 67, 63, 51, 65, 65, 61, 59, 59, 61, 55, 61, 55, 65, 61, 57, 55, 63, 57, 65, 57, 53, 55, 59, 51, 47, 59, 47, 55, 63, 59, 61, 51, 53, 59, 59, 57, 65, 55, 53, 53, 57, 49, 55, 55, 61, 61, 65, 51, 59, 65, 55, 55, 71, 51, 51, 69, 51, 65, 49, 53, 57, 51, 57, 51, 67, 63, 57, 61, 55, 61, 61, 45, 63, 67, 49]
data_250_f = [67, 55, 49, 51, 45, 51, 53, 59, 63, 61, 53, 57, 45, 63, 59, 43, 61, 61, 51, 49, 67, 67, 55, 57, 57, 53, 67, 53, 59, 63, 67, 57, 47, 57, 63, 53, 61, 63, 57, 67, 69, 65, 43, 59, 59, 45, 57, 63, 63, 61, 63, 57, 61, 67, 53, 59, 59, 57, 49, 59, 57, 69, 59, 59, 59, 63, 55, 59, 65, 53, 51, 59, 59, 57, 61, 63, 51, 57, 57, 53, 55, 65, 57, 57, 45, 53, 63, 61, 71, 67, 57, 65, 55, 51, 61, 51, 47, 51, 65, 49, 51, 51, 41, 55, 57, 57, 55, 69, 71, 55, 55, 71, 57, 57, 57, 63, 55, 53, 57, 51]

plot_histograms([data_50_b, data_150_b, data_250_b], [data_50_f, data_150_f, data_250_f])
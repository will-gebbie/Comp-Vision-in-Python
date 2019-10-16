import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


def new_grayscale(pixel_values):
    new_matrix = [[0 for i in range(pixel_values.shape[1])] for j in range(pixel_values.shape[0])]
    for row in range(pixel_values.shape[0]):
        for col in range(pixel_values.shape[1]):
            new_matrix[row][col] = pixel_values[row][col][0]
    return new_matrix


def rgb_grayscale(pixel_values):
    rgb_grayscale_matrix = np.zeros((len(pixel_values), len(pixel_values[0]), 3))
    for row in range(rgb_grayscale_matrix.shape[0]):
        for col in range(rgb_grayscale_matrix.shape[1]):
            for item in range(rgb_grayscale_matrix.shape[2]):
                rgb_grayscale_matrix[row][col][item] = pixel_values[row][col]
    return rgb_grayscale_matrix


def make_histogram_dict(pixel_values):
    value_dict = {gray_level: 0 for gray_level in range(256)}
    for row in range(len(pixel_values)):
        for col in range(len(pixel_values[0])):
            key = pixel_values[row][col]
            value_dict[key] += 1

    # Normalize values
    for key, value in value_dict.items():
        value /= (len(pixel_values) * len(pixel_values[0]))
        value_dict[key] = value

    return value_dict


def make_cumulative_hist(original_hist):
    cumulative_hist = {gray_level: 0 for gray_level in range(256)}
    L = 255
    cumulative_hist[0] = original_hist[0] * L
    for key in range(1, 256):
        cumulative_hist[key] = cumulative_hist[key-1] + original_hist[key] * L
    return cumulative_hist


def equalize_image(cumulative_hist, pixel_values):
    for row in range(len(pixel_values)):
        for col in range(len(pixel_values[0])):
            key = pixel_values[row][col]
            pixel_values[row][col] = int(cumulative_hist[key])
    return pixel_values


def display_histogram(hist_dict):
    plt.bar(hist_dict.keys(), hist_dict.values(), 1, color='b')
    plt.show()


def show_image(pixel_values):
    plt.imshow(pixel_values.astype(np.uint8))
    plt.show()


def main():
    raw_gray_values = mpimg.imread('./grayscale_pup.jpg')
    new_gray_values = new_grayscale(raw_gray_values)

    original_hist = make_histogram_dict(new_gray_values)
    cumulative_hist = make_cumulative_hist(original_hist)

    equalized_gray_values = equalize_image(cumulative_hist, new_gray_values)
    equalized_hist = make_histogram_dict(equalized_gray_values)
    # Convert back to raw rgb grayscale format
    raw_equalized_gray_values = rgb_grayscale(equalized_gray_values)

    # Original Image and Histogram
    show_image(raw_gray_values)
    display_histogram(original_hist)

    # Equalized Image and Histogram
    show_image(raw_equalized_gray_values)
    display_histogram(equalized_hist)


if __name__ == '__main__':
    main()

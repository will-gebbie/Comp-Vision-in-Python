import cv2
import numpy as np


def get_coordinates(bgr_values):
    height, width = bgr_values.shape[0], bgr_values.shape[1]
    num_pixels = height * width

    sample_size = int(0.2 * num_pixels)

    coord_list = []
    for i in range(sample_size):
        random_coord = (np.random.randint(height), np.random.randint(width))
        coord_list.append(random_coord)

    return coord_list


def add_salt_pepper(bgr_values):
    black = [0, 0, 0]
    white = [255, 255, 255]

    coord_list = get_coordinates(bgr_values)

    copy_array = np.copy(bgr_values)

    for coord in coord_list:
        binary_random = np.random.randint(2)

        if binary_random == 0:
            copy_array[coord[0], coord[1]] = black
        else:
            copy_array[coord[0], coord[1]] = white

    return copy_array


def filter_noise(noisy_bgr_values):
    after_median_values = cv2.medianBlur(noisy_bgr_values, 7)
    return after_median_values

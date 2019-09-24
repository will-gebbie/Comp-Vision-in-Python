import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


def show_image(rgb_values):
    plt.imshow(rgb_values)
    plt.show()


def bilinear_interpolation(rgb_values, x, y):
    x_0 = int(np.floor(x))
    y_0 = int(np.floor(y))
    dx = x - x_0
    dy = y - y_0

    # Handle out of bounds
    x_plus1 = np.minimum(x_0 + 1, rgb_values.shape[1] - 1)
    y_plus1 = np.minimum(y_0 + 1, rgb_values.shape[0] - 1)

    top_left = rgb_values[x_0, y_0] * (1 - dx) * (1 - dy)
    bottom_left = rgb_values[x_plus1, y_0] * dx * (1 - dy)
    top_right = rgb_values[x_plus1, y_0] * (1 - dx) * dy
    bottom_right = rgb_values[x_plus1, y_plus1] * dx * dy
    # Calculate rgb at (x,y) using bilinear interpolation on known values
    value_at_xy = top_left + bottom_left + top_right + bottom_right
    return value_at_xy


def fill_matrix(rgb_values, k):
    rows = rgb_values.shape[0] * k
    cols = rgb_values.shape[1] * k
    # Expanded rgb matrix
    expanded_rgb = np.zeros((rows, cols, rgb_values.shape[2]))
    row_scale = (rows / k) / rows
    col_scale = (cols / k) / cols
    for row in range(rows):
        for col in range(cols):
            # Calculate position of original x and y coordinates
            orig_x = row * row_scale
            orig_y = col * col_scale
            # Bilinear interpolate to fill in intermediate rgb_values
            expanded_rgb[row, col] = bilinear_interpolation(rgb_values, orig_x, orig_y)

    return expanded_rgb


def main():
    img_rgb_values = mpimg.imread('./toad.png')
    for k in range(2, 4):
        bp_img_rgb = fill_matrix(img_rgb_values, k)
        print('K = {}'.format(k))
        show_image(img_rgb_values)
        show_image(bp_img_rgb)


if __name__ == '__main__':
    main()

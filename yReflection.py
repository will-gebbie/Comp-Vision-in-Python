import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def show_image(rgb_values):
    plt.imshow(rgb_values)
    plt.show()


def reflect_image(rgb_values):
    # This slice operation reverses the order of columns in each row of a 2d array
    reverse_rgb_values = rgb_values[:, ::-1]

    """
    Example: [2 5] --> [5 2]
             [6 7] --> [7 6]
    """

    return reverse_rgb_values


def main():
    img_rgb_values = mpimg.imread('./Kame_House.png')
    y_flip_rgb_values = reflect_image(img_rgb_values)
    show_image(img_rgb_values)
    show_image(y_flip_rgb_values)


if __name__ == '__main__':
    main()

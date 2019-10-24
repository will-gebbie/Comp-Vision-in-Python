import argparse
import cv2
import numpy as np
import add_filter_noise as afn


def show_image(window_name, img):
    cv2.namedWindow(winname=window_name, flags=cv2.WINDOW_NORMAL)
    cv2.imshow(winname=window_name, mat=img)
    # cv2.waitKey(0)


def only_one_color(bgr_values, color):
    # Initialize color hsv boundary for common colors
    blue_boundary = (np.array([95, 25, 25]), np.array([140, 255, 255]))
    green_boundary = (np.array([36, 25, 25]), np.array([70, 255, 255]))
    yellow_boundary = (np.array([20, 25, 25]), np.array([35, 255, 255]))

    # Convert colormap to HSV (HSI)
    hsv_values = cv2.cvtColor(bgr_values, cv2.COLOR_BGR2HSV)

    # Trick to find red due to wrap around in hsv hue values
    # Invert the bgr values and now red is cyan.
    invert_bgr_hsv = cv2.cvtColor(cv2.bitwise_not(bgr_values), cv2.COLOR_BGR2HSV)
    red_boundary = (np.array([80, 25, 25]), np.array([100, 255, 255]))

    # Threshold for the specific color, converting other pixels not in range to black
    if color.lower() == 'green':
        thresh = color_threshold(hsv_values, green_boundary)
    elif color.lower() == 'blue':
        thresh = color_threshold(hsv_values, blue_boundary)
    elif color.lower() == 'red':
        thresh = color_threshold(invert_bgr_hsv, red_boundary)
    elif color.lower() == 'yellow':
        thresh = color_threshold(hsv_values, yellow_boundary)
    else:
        raise ValueError('Invalid color! Please use python edgeDetection.py -h to see which colors are available')

    return thresh


def color_threshold(hsv_values, boundary):
    # If HSV values are not in this range, return black pixel
    hsv_mask = cv2.inRange(hsv_values, boundary[0], boundary[1])
    return hsv_mask


def get_draw_contours(thresh_values, bgr_values):
    contours = cv2.findContours(thresh_values, cv2.RETR_LIST,
                                cv2.CHAIN_APPROX_NONE)[1]
    bgr_values_outlined = np.copy(bgr_values)
    bgr_values_outlined = cv2.drawContours(bgr_values_outlined, contours, -1, (255, 0, 0), 3)

    return bgr_values_outlined


def custom_parser():
    parser = argparse.ArgumentParser(description='Outline specific colors of an image!')
    parser.add_argument('img', metavar='PATH/TO/FILE.ext',
                        help='The image you want the program to process.')
    parser.add_argument('--color', action='store', dest='color', default='green', type=str,
                        help='blue, yellow, red, or green. Default = \'green\'')
    return parser


def main():
    args = custom_parser().parse_args()

    bgr_values = cv2.imread(args.img)
    color = args.color

    # Threshold for a specific color
    color_thresh = only_one_color(bgr_values, color)
    # Outline in blue
    outlined_image = get_draw_contours(color_thresh, bgr_values)

    # Add in salt n pepper noise
    noisy_bgr_values = afn.add_salt_pepper(bgr_values)
    noise_color_thresh = only_one_color(noisy_bgr_values, color)
    noise_outline = get_draw_contours(noise_color_thresh, noisy_bgr_values)

    # Filter out noise
    filtered_bgr_values = afn.filter_noise(noisy_bgr_values)

    show_image('Threshold Image', color_thresh)
    show_image('Outline Image', outlined_image)
    show_image('Noisy Image', noisy_bgr_values)
    show_image('Noise Outline', noise_outline)
    show_image('Filtered Image', filtered_bgr_values)

    print('Press any key to exit.')
    cv2.waitKey(0)


if __name__ == '__main__':
    main()

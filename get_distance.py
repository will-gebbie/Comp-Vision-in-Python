import cv2
import math


def convert2gray(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img


def otsu_threshold(img):
    threshold_image = cv2.threshold(img, thresh=100, maxval=255,
                                    type=cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return threshold_image


def get_contours(thresh_img):
    contours = cv2.findContours(thresh_img, cv2.RETR_LIST,
                                cv2.CHAIN_APPROX_SIMPLE)[1]
    return contours


"""
***************************************************************************************
*    Author: Andriy Makukha
*    Date: 03/30/2018
*    Availability: https://stackoverflow.com/questions/49577973/how-to-crop-the-biggest-object-in-image-with-python-opencv
***************************************************************************************
"""


def find_biggest_object_coordinates(contours):
    mx = (0, 0, 0, 0)  # biggest bounding box so far
    mx_area = 0
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = w * h
        if area > mx_area:
            mx = x, y, w, h
            mx_area = area
    x, y, w, h = mx
    return x, y, w, h


def pixel_dist_2_real_dist(x_i, x_f, img_w):
    WINDOW_WIDTH = 6.5  # inches

    # Feet/Inch RealWorld/Picture
    SCALE = 3 / 1

    # Inches per Pixel
    pixel_scale = WINDOW_WIDTH / img_w

    pixel_dist = abs(x_f - x_i)
    dist_in_inches = pixel_dist * pixel_scale
    dist_in_feet = dist_in_inches * SCALE

    return dist_in_feet


def show_image(window_name, img):
    cv2.namedWindow(winname=window_name, flags=cv2.WINDOW_NORMAL)
    cv2.imshow(winname=window_name, mat=img)


def main():
    img1 = cv2.imread('./car_1.jpg')
    img2 = cv2.imread('./car_2.jpg')

    img_width = img1.shape[0]

    # Convert to grayscale
    grayimg1 = convert2gray(img1)
    grayimg2 = convert2gray(img2)

    # Equalize Photos
    equalized_1 = cv2.equalizeHist(grayimg1)
    equalized_2 = cv2.equalizeHist(grayimg2)

    # Apply Gaussian Blur filter
    blurimg1 = cv2.GaussianBlur(equalized_1, (5, 5), 0)
    blurimg2 = cv2.GaussianBlur(equalized_2, (5, 5), 0)

    # Threshold each image
    thresh1 = otsu_threshold(blurimg1)
    thresh2 = otsu_threshold(blurimg2)

    # Find the contours of the threshold images
    thresh1_conts = get_contours(thresh1)
    thresh2_conts = get_contours(thresh2)

    # Get biggest object coordinates (the car)
    initial_position = find_biggest_object_coordinates(thresh1_conts)
    final_position = find_biggest_object_coordinates(thresh2_conts)

    x_initial = initial_position[0]
    y_initial = initial_position[1]
    width_initial = initial_position[2]
    height_initial = initial_position[3]
    x_final = final_position[0]
    y_final = final_position[1]
    width_final = final_position[2]
    height_final = final_position[3]

    print('Initial Position: x: {}, y: {}, width: {}, height: {}'.format(x_initial, y_initial,
                                                                         width_initial, height_initial))
    print('Final Position: x: {}, y: {}, width: {}, height: {}'.format(x_final, y_final,
                                                                       width_final, height_final))

    # Calculate distance based on pixel position x_initial and x_final
    real_world_distance = pixel_dist_2_real_dist(x_initial, x_final, img_width)

    print('Real World Distance between two cars: {} feet'.format(real_world_distance))


if __name__ == '__main__':
    main()

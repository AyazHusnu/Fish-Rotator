import os
import cv2
import math
from PIL import Image
import numpy as np

def read_image(image_path):
    """
    Read an image from the specified file path.

    Args:
        image_path (str): The path to the image file (with extensions '.png', '.jpg', '.jpeg').

    Returns:
        numpy.ndarray: The image as a NumPy array if successful, None otherwise.
    """
    # Check if the file path is valid
    if not os.path.isfile(image_path):
        print(f"Error: Invalid file path '{image_path}'. The file does not exist.")
        return None

    # Check if the file has a valid image extension
    valid_extensions = ['.png', '.jpg', '.jpeg']
    _, file_extension = os.path.splitext(image_path)
    if file_extension.lower() not in valid_extensions:
        print(f"Error: Invalid file extension '{file_extension}'. Supported extensions are {valid_extensions}.")
        return None

    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)

        # Check if the image reading was successful
        if image is None:
            print(f"Error: Unable to read the image from '{image_path}'.")
            return None

        return image

    except Exception as e:
        print(f"Error: {e}")
        return None

def rotate_image(angle, image):
    """
    Rotate the specified image by the given angle.

    Args:
        angle (float): The angle in degrees to rotate the image.
        image (numpy.ndarray): The input image as a NumPy array.

    Returns:
        numpy.ndarray: The rotated image as a NumPy array.
    """
    # Specify the rotation angle
    rotation_angle = angle

    # Create the rotation matrix
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), rotation_angle, 1)

    # Rotate the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return rotated_image

def mirror(image):
    """
    Mirror the specified image horizontally.

    Args:
        image (numpy.ndarray): The input image as a NumPy array.

    Returns:
        numpy.ndarray: The horizontally mirrored image as a NumPy array.
    """
    # Flip the image horizontally
    mirrored_image = cv2.flip(image, 1)

    return mirrored_image

def radian_to_degree(radian):
    """
    Convert an angle from radians to degrees.

    Args:
        radian (float): Angle in radians.

    Returns:
        float: Angle converted to degrees.
    """
    degree = radian * (180 / math.pi)
    return degree


def calculate_angle(X, Y, Head_X, Head_Y, Tail_X, Tail_Y):
    """
    Calculate the angle based on the provided coordinates and reference points.

    Args:
        X (float): X coordinate.
        Y (float): Y coordinate.
        Head_X (list): List of X coordinates for objects with label 0 (head).
        Head_Y (list): List of Y coordinates for objects with label 0 (head).
        Tail_X (list): List of X coordinates for objects with label 1 (tail).
        Tail_Y (list): List of Y coordinates for objects with label 1 (tail).

    Returns:
        None: The calculated angle in degrees is printed.

    Note:
        The function relies on the existence of the 'RotatePhoto' and 'Mirror' functions,
        which are assumed to be defined elsewhere.
    """
    # Calculate the coordinates of the head (label 0)
    Head_Point = [X * Head_X, abs((Y * Head_Y) - Y)]
    x0, y0 = Head_Point

    # Calculate the coordinates of the tail (label 1)
    Tail_Point = [X * Tail_X, abs((Y * Tail_Y) - Y)]
    x1, y1 = Tail_Point

    # Calculate the angle in radians
    a = abs(x1 - x0)
    c = math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))
    angle_radian = math.acos(a / c)

    return angle_radian


def read_labels(txt_path):
    with open(txt_path) as file:
        for line in file:
            s = line.strip().split()
            if s[0] == '0':
                X0 = (float(s[1]))
                Y0 = (float(s[2]))
            elif s[0] == '1':
                X1 = (float(s[1]))
                Y1 = (float(s[2]))
    return X0,Y0,X1,Y1

images_directory_path = "C:/Users/Ayaz/Desktop/Fish-Rotator/images"
image_names = os.listdir(images_directory_path)

labels_directory_path = "C:/Users/Ayaz/Desktop/Fish-Rotator/labels"
label_names = os.listdir(labels_directory_path)

output_folder_path = "C:/Users/Ayaz/Desktop/Fish-Rotator/output"
images_and_labels = tuple(zip(image_names, label_names))

for image_name in image_names:
    image_path = os.path.join(images_directory_path, image_name)
    label_name,_ = os.path.splitext(image_name)
    label_name = label_name + '.txt'

    label_path = os.path.join(labels_directory_path, label_name)


    image = read_image(image_path)
    X0, Y0, X1, Y1 = read_labels(label_path)

    width,height, _ = image.shape
    print(height,width,image_name)
    radian = calculate_angle(height, width, X0, Y0, X1, Y1)
    angle = radian_to_degree(radian)

    print(f"Processing: Image '{image_name}' with angle {angle} degrees")

    if X0 - X1 > 0 and Y0 - Y1 < 0:
        angle = -angle
        print("Region 1: Rotating")
        rotated_image = rotate_image(angle, image)
        image = rotated_image
    elif X0 - X1 <= 0 and Y0 - Y1 <= 0:
        angle = angle
        print("Region 2: Rotating and Mirroring")
        rotated_image = rotate_image(angle, image)
        mirrored_image = mirror(rotated_image)
        image = mirrored_image
    elif X0 - X1 <= 0 and Y0 - Y1 >= 0:
        angle = -angle
        print("Region 3: Rotating and Mirroring")
        rotated_image = rotate_image(angle, image)
        mirrored_image = mirror(rotated_image)
        image = mirrored_image
    elif X0 - X1 > 0 and Y0 - Y1 > 0:
        angle = angle
        print('Region 4: Rotating')
        rotated_image = rotate_image(angle, image)
        image = rotated_image

    output_image_path = os.path.join(output_folder_path, image_name)
    cv2.imwrite(output_image_path, image)





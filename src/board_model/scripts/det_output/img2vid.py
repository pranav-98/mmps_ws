import cv2
import os
import glob
import re

def extract_number(img_name):
    return int(re.search(r'\d+', img_name).group())

def jpg_to_video(input_folder, output_video, fps):
    img_array = []
    size = None

    # Get all image file paths in the input folder
    img_names = glob.glob(os.path.join(input_folder, '*.jpg'))
    img_files = sorted(img_names, key=extract_number)
    # print(img_files)

    # Loop through each image file
    for filename in img_files:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    # Create a VideoWriter object
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'XVID'), fps, size)

    # Write each image to the video
    for i in range(len(img_array)):
        out.write(img_array[i])

    # Release the VideoWriter object
    out.release()


if __name__ == "__main__":
    input_folder = 'runs/detect/exp'
    output_video = 'vid.avi'
    fps = 24

    jpg_to_video(input_folder, output_video, fps)

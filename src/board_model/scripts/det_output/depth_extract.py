import cv2
import os
import glob
import re

def extract_number(img_name):
    return int(re.search(r'\d+', img_name).group())

label_path = '/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/det_output/yolov5/runs/detect/exp2/labels'
depth_img_path = '/home/ajith/Documents/git_repos/mmps_ws/src/board_model/scripts/depth_images'

# Get all image file paths in the input folder
img_names = glob.glob(os.path.join(depth_img_path, '*.jpg'))
img_files = sorted(img_names, key=extract_number)

# Loop through each image file
for file_loc in img_files:

    # extracting filename
    img_name = os.path.basename(file_loc)
    file_name, _ = os.path.splitext(img_name)

    # extracting labels for that file
    with open(os.path.join(label_path, file_name+'.txt'), "r") as f:
        labels = f.read().splitlines()

    image = cv2.imread(file_loc)
    
    img_h, img_w, _ = image.shape
    bounding_boxes = []

    for label in labels:
        class_index, x_center, y_center, width, height = map(float, label.split())

        # convert to image coordinates
        x_min = int((x_center - width / 2) * img_w)
        y_min = int((y_center - height / 2) * img_h)
        x_max = int((x_center + width / 2) * img_w)
        y_max = int((y_center + height / 2) * img_h)

        bounding_boxes.append((x_min, y_min, x_max, y_max, class_index))
    
    obj_list = []
    for bbox in bounding_boxes:
        x_min, y_min, x_max, y_max, class_index = bbox

        # draw the bounding box
        color = (0, 255, 0)
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
        cv2.putText(image, f"class {class_index}", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # display the image
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # obj_list.append(image[y_min:y_max, x_min:x_max])
    
    for obj in obj_list:
        print(obj.shape)

    if file_name == 'img1':
        # print(image[345:350,345:350,:])
        # print(file_name)
        # print(labels)
        break


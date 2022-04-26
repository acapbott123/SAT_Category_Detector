
import os
import cv2
import numpy as np
def yoloFormattocv(x1, y1, x2, y2, H, W):
    bbox_width = x2 * W
    bbox_height = y2 * H
    center_x = x1 * W
    center_y = y1 * H

    voc = []

    voc.append(center_x - (bbox_width / 2))
    voc.append(center_y - (bbox_height / 2))
    voc.append(center_x + (bbox_width / 2))
    voc.append(center_y + (bbox_height / 2))

    return [int(v) for v in voc]

# convert from opencv format to yolo format
# H,W is the image height and width
def cvFormattoYolo(corner, H, W):
    bbox_W = corner[3] - corner[1]
    bbox_H = corner[4] - corner[2]

    center_bbox_x = (corner[1] + corner[3]) / 2
    center_bbox_y = (corner[2] + corner[4]) / 2

    return corner[0], round(center_bbox_x / W, 6), round(center_bbox_y / H, 6), round(bbox_W / W, 6), round(bbox_H / H,
                                                                                                            6)
#files =  os.listdir(listdr)
image_paths = []
txt_paths = []
for folderName in os.listdir('Images'):
    for fileName in os.listdir('Images/'+folderName):
        if '.txt' not in fileName:
            file_path = os.path.join('Images',folderName, fileName)
            image_paths.append(file_path)
        elif '.txt' in fileName:
            file_path = os.path.join('Images',folderName, fileName)
            txt_paths.append(file_path)
txt_paths = sorted(txt_paths)
image_paths = sorted(image_paths)
#print(txt_paths)
#print(image_paths)
image = cv2.imread(image_paths[0])
imageText = open(txt_paths[0] , "r").read()

(H, W) = image.shape[:2]
image = cv2.resize(image, (756//2,1008//2))
(H, W) = image.shape[:2]
print(imageText)
#cv2.imshow("Image1", image)
#cv2.waitKey()
imageText = imageText.split('\n')
colors = {'0': (0, 0, 255),
          '1' : (0, 255, 0),
          '2' : (255, 0, 0),
          '3' : (255, 255, 0)} 
for i in range(0,len(imageText)-1):

    splitimage = imageText[i].split()
    classname, centerX, centerY, width, height = splitimage
    width = float(width)
    height = float(height)
    centerX = float(centerX)
    centerY = float(centerY)
    
    image = cv2.rectangle(image, (int(((centerX - width/2)*W)), int(((centerY - height/2)*H))), (int(((centerX + width/2)*W)), int(((centerY + height/2)*H))),colors[classname], 2) 
#cv2.imshow("Image1", image)
#cv2.waitKey()

# image_path = []
# for file in files:
#     if '.txt' not in file:
#         file_path = os.path.join(image_folder_root, file)
#         image_paths.append(file_path)
# image_paths = sorted(image_paths)

# txt_paths = []
# for file in files:
#     if '.txt' in file:
#         file_path = os.path.join(txt_folder_root, file)
#         txt.append(file_path)
# txt_paths = sorted(txt_paths)



# for folderName in os.listdir('Images'):
#     print(foldername)
class yoloRotatebbox:
    def __init__(self, filename, image_ext, angle):
        assert os.path.isfile(filename + image_ext)
        assert os.path.isfile(filename + '.txt')

        self.filename = filename
        self.image_ext = image_ext
        self.angle = angle

        # Read image using cv2
        self.image = cv2.imread(self.filename + self.image_ext, 1)
        (H, W) = self.image.shape[:2]
        self.image = cv2.resize(self.image, (756//2,1008//2))

        # create a 2D-rotation matrix
        rotation_angle = self.angle * np.pi / 180
        self.rot_matrix = np.array(
            [[np.cos(rotation_angle), -np.sin(rotation_angle)], [np.sin(rotation_angle), np.cos(rotation_angle)]])
        


    def rotate_image(self):
        """
        Rotates an image (angle in degrees) and expands image to avoid cropping
        """
        height, width = self.image.shape[:2]  # image shape has 3 dimensions
        image_center = (width / 2,
                        height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, self.angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origin) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated_mat = cv2.warpAffine(self.image, rotation_mat, (bound_w, bound_h))
        return rotated_mat



    def rotateYolobbox(self):

        new_height, new_width = self.rotate_image().shape[:2]

        f = open(self.filename + '.txt', 'r')

        f1 = f.readlines()

        new_bbox = []

        H, W = self.image.shape[:2]

        for x in f1:
            bbox = x.strip('\n').split(' ')
            if len(bbox) > 1:
                (center_x, center_y, bbox_width, bbox_height) = yoloFormattocv(float(bbox[1]), float(bbox[2]),
                                                                               float(bbox[3]), float(bbox[4]), H, W)
                
                # shift the origin to the center of the image.
                upper_left_corner_shift = (center_x - W / 2, -H / 2 + center_y)
                upper_right_corner_shift = (bbox_width - W / 2, -H / 2 + center_y)
                lower_left_corner_shift = (center_x - W / 2, -H / 2 + bbox_height)
                lower_right_corner_shift = (bbox_width - W / 2, -H / 2 + bbox_height)

                new_lower_right_corner = [-1, -1]
                new_upper_left_corner = []

                for i in (upper_left_corner_shift, upper_right_corner_shift, lower_left_corner_shift,
                          lower_right_corner_shift):
                    new_coords = np.matmul(self.rot_matrix, np.array((i[0], -i[1])))
                    x_prime, y_prime = new_width / 2 + new_coords[0], new_height / 2 - new_coords[1]
                    if new_lower_right_corner[0] < x_prime:
                        new_lower_right_corner[0] = x_prime
                    if new_lower_right_corner[1] < y_prime:
                        new_lower_right_corner[1] = y_prime

                    if len(new_upper_left_corner) > 0:
                        if new_upper_left_corner[0] > x_prime:
                            new_upper_left_corner[0] = x_prime
                        if new_upper_left_corner[1] > y_prime:
                            new_upper_left_corner[1] = y_prime
                    else:
                        new_upper_left_corner.append(x_prime)
                        new_upper_left_corner.append(y_prime)
                #             print(x_prime, y_prime)

                new_bbox.append([bbox[0], new_upper_left_corner[0], new_upper_left_corner[1],
                                 new_lower_right_corner[0], new_lower_right_corner[1]])



        return new_bbox    
print(image_paths[0])
if image_paths[0].endswith('.JPG'):
    image_paths[0] = image_paths[0].replace('.JPG', '')
rotator = yoloRotatebbox(image_paths[0],'.JPG', 25)
rotatedImage = rotator.rotate_image()
newBox = rotator.rotateYolobbox()
for i in range(0,len(newBox)):

    bboxData = newBox[i]
    classname, upperLeftX, upperLeft1Y, lowerRightX, lowerRightY = bboxData
    
    print(upperLeftX, upperLeft1Y, lowerRightX, lowerRightY)
    image = cv2.rectangle(rotatedImage, (int(upperLeftX), int(upperLeft1Y)), (int(lowerRightX), int(lowerRightY)),colors[classname], 2) 

cv2.imshow("Image1", image)

cv2.waitKey()

# Ví dụ sử dụng thư viện Open-CV cho xử lý ảnh trong Python
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html
import cv2
image = cv2.imread("/home/tamvm/Downloads/Tut 3-Data Preparation/img/cat.jpg")

print ("shape =", image.shape)
print (image[:, :, 2])


# Sử dụng thư viện Matplotlib để hiển thị ảnh trong Python
# https://matplotlib.org/
from matplotlib import pyplot as plt
plt.subplots()
plt.imshow(image)

# Thay đổi kích thước ảnh
resized_image = cv2.resize(image, (15, 15)) 
print ("shape =", resized_image.shape)
print (resized_image[:, :, 2])

plt.subplots()
plt.imshow(resized_image)

# Chuyển sang ảnh xám
greyscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print ("shape =", greyscale_image.shape)
print (greyscale_image[:, :])

plt.subplots()
plt.imshow(greyscale_image,cmap = 'gray')

import numpy as np
plt.subplots(figsize=(20, 10))

# Lật ảnh
horizontal_img = cv2.flip(image, 0 )
plt.subplot(141),plt.imshow(horizontal_img)
plt.xticks([])
plt.yticks([])

vertical_img = cv2.flip(image, 1 )
plt.subplot(142),plt.imshow(vertical_img)
plt.xticks([])
plt.yticks([])


both_img = cv2.flip(image, -1 )
plt.subplot(143),plt.imshow(both_img)
plt.xticks([])
plt.yticks([])

# Xoay ảnh
angle = 20
image_center = tuple(np.array(image.shape[1::-1]) / 2)
rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
rot_img = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
plt.subplot(144),plt.imshow(rot_img)
plt.xticks([])
plt.yticks([])


# Với "Mask" là một ma trận cho trước 
# Sử dụng phép nhân hadamard để áp dụng lớp "Mask" lên hình ảnh

mask = np.random.random(greyscale_image.shape[:2])
masked_image = mask * greyscale_image

plt.subplots()
plt.imshow(masked_image,cmap = 'gray')

plt.show()
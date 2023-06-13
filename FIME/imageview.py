import flet as ft
import numpy as np
# from numpy.typing import NDArray,ArrayLike
# from typing import Any
import cv2

import os
import secrets
import base64


VERTICAL_KERNAL  = np.array([[1,0,-1],
                             [1,0,-1],
                            [1,0,-1]])

HORIZONTAL_KERNAL = np.array([[1,1,1],
                              [0,0,0],
                              [-1,-1,-1]])
SOBEL_KERNAL = np.array([[1,0,-1],
                         [2,0,-2],
                         [1,0,-1]])


class ImageContext:
    def __init__(self, 
                 path:str,
                 height:int=500,
                 width:int=500,
                 preload:bool=False) -> None:
        
        self.path = path
        self.height = height
        self.width = width
        self.preload = preload
        self.image_array : np.ndarray = None
       
        self.__loaded:bool = False
        self.__image_array_state : np.ndarray = None

        if self.preload:
            self._from_path()

    def __call__(self):
        if self.__loaded:
            return self.image_array
        else:
            self._from_path()
            return self.image_array
        
    def get_relative_coordinate(self, x, y):
        if not self.__loaded:
            self._from_path()

        if len(self.shape)==3:
            H, W, _ = self.shape
        else:
            H, W = self.shape

        return (W/self.width)*x, (H/self.height)*y

    def get_base64(self):
        if not self.__loaded:
            return self._from_path_base64()
        else:
            return self._from_memory_base64()
    

    def get_rgb(self):
        if not self.__loaded:
            self._from_path()

        return cv2.cvtColor(self.image_array.copy(), cv2.COLOR_BGR2RGB)
    
    def from_rgb_array(self, image):
        self.image_array = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    def discard(self):
        if not self.__loaded:
            self._from_path()
        
        self.image_array = self.__image_array_state.copy()

    def reload(self):
        self.__loaded = False
        self.__image_array_state = None
        self.image_array = None
    
    def save_state(self):
        print("--- Image State Saved")
        if not self.__loaded:
            self._from_path()

        self.__image_array_state = self.image_array.copy()

    def _from_path(self):
        image = cv2.imread(self.path)
        self._update_state(image)
    
    def _from_path_base64(self):
        with open(self.path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
        
    def _from_memory(self):
        return self.image_array

    def _from_memory_base64(self):
        image_encode = cv2.imencode('.png', self.image_array)[1]
        return base64.b64encode(image_encode).decode('utf-8')

    def _update_state(self, image=None):
        if not self.__loaded:
            self.__loaded = True
        
        if type(image) != type(None):
            print("--- Image Loaded In Memory")
            self.image_array = image

    @property
    def shape(self):
        if not self.__loaded:
            self._from_path()
        
        return self.image_array.shape
    
    @property
    def channel(self):
        if not self.__loaded:
            self._from_path()
        
        if len(self.image_array.shape)==3:
            return self.image_array.shape[2]
        else:
            return 1
    
        
## image editing functions here 

def image_median_blur(image:ImageContext, kernal_size):
   image.image_array = cv2.medianBlur(image(), kernal_size)
   return image

def image_gray(image:ImageContext):
    if type(image.image_array) == type(None):
        image()

    if len(image.image_array.shape) <3:
        return image 
    
    image.image_array = cv2.cvtColor(image(), cv2.COLOR_RGB2GRAY)
    return image

def image_filter(image:ImageContext, kernal=VERTICAL_KERNAL):
    image.image_array = cv2.filter2D(image(), -1, kernal)
    return image

def draw_dot(image:ImageContext, x, y, point_size=5):
    if len(image.shape)<3:
        return cv2.circle(image, (int(x), int(y)), point_size, 255, -1)

    return cv2.circle(image, (int(x), int(y)), point_size, (0, 0, 255), -1)
    
def image_conrast(image:ImageContext, alpha, beta):
    image.image_array = cv2.convertScaleAbs(image(),None, alpha, beta)
    return image


def image_save(image:ImageContext, name:str=None, path=None):
    if name==None or name=="":
        name = secrets.token_hex(10)

    actual_path = os.path.join(path, f'{name}.jpg')
    cv2.imwrite(actual_path, image())

if __name__ == "__main__":
    image = ImageContext("cosmetics.jpg")
    print(image.shape)
    image = image_gray(image)
    print(image.shape)

    # img = base64.b64encode(image()).decode('utf-8')

    # print(image.get_base64())
    # print(img)
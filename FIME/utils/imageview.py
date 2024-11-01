"""
Python Module for Writing Image Editing Software
Author: Pritom Mojumder
Email: pritom.blue2@gmail.com
"""
import flet as ft
import numpy as np
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
                 keep_track:bool=True,
                 preload:bool=False) -> None:
        
        self.path = path
        self.height = height
        self.width = width
        self.keep_track = keep_track
        self.preload = preload
        
        self.image_array : np.ndarray = None
       
        self.__loaded:bool = False # flag: if the image is loaded as array
        self.__image_array_state : np.ndarray = None # image array state before a change
        self.__image_history : list = [] # arrays of images to preserve history
        self.__track_pointer = -1
        self.__FLAG_UNDO:bool = False
    

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
        '''This method discard the immediate change'''
        if not self.__loaded:
            self._from_path()
        
        self.image_array = self.__image_array_state.copy()

    def reload(self):
        ''' This method reload the image from source'''
        self.__loaded = False
        self.__image_array_state = None
        self.image_array = None
    
    def save_state(self):
        print("--- Image State Saved")
        if not self.__loaded:
            self._from_path()
        
        if self.keep_track:
            self.__keep_track(self.image_array)
        
        self.__image_array_state = self.image_array.copy()


    def __keep_track(self, image_array:np.ndarray ):
        if self.__FLAG_UNDO:
            self.__image_history = self.__image_history[0:self.__track_pointer+1]
            self.__FLAG_UNDO = False

        self.__image_history.append(image_array.copy())
        self.__track_pointer += 1 
    
    def undo(self):
        # [h0, h1, h3]
        # __track_pointer = 2
        print(self.__track_pointer, self.history_length)
        if self.__track_pointer>=0:
            self.__FLAG_UNDO = True
            self.__track_pointer = self.__track_pointer-1 if self.__track_pointer>0 else 0
            self.image_array = self.__image_history[self.__track_pointer]

    def redo(self):
        print(self.__track_pointer, self.history_length)
        if self.__track_pointer<self.history_length:
            self.__FLAG_UNDO = True
            self.__track_pointer = self.__track_pointer if self.__track_pointer==self.history_length-1 else self.__track_pointer+1
            self.image_array = self.__image_history[self.__track_pointer]

    # def get_from_history(self, idx):
    #     if idx<=len(self.history_length)-1:
    #         return self.imag
    #     if self.__loaded:
    #         return self.image_array
    #     else:
    #         self._from_path()
    #         return self.image_array
        
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
    def history_length(self):
        return len(self.__image_history)
    
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

def image_gaussian_blur(image:ImageContext, kernal_size):
   image.image_array = cv2.GaussianBlur(image(), (kernal_size,kernal_size),0)
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


def image_invert(image:ImageContext):
    image.image_array = cv2.bitwise_not(image())
    return image

if __name__ == "__main__":
    path = r"C:\Users\Pritom\Desktop\dog.jpg"
    image = ImageContext(path=path)
    print(image.shape)
    image = image_gray(image)
    image = image_invert(image)
    print(image.shape)
    cv2.imshow("show", image())

    # waits for user to press any key
# (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)

# closing all open windows
    cv2.destroyAllWindows()
    # img = base64.b64encode(image()).decode('utf-8')

    # print(image.get_base64())
    # print(img)
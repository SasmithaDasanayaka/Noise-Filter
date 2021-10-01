# libraries only for reading and saving images
import numpy as np
import cv2
from pathlib import Path
import glob
import os

def read_all_images():
    paths = []
    image_names = []
    for image_name in glob.glob("*.jpg")+glob.glob("*.jpeg"):
        path = os.path.join(Path().absolute(),image_name)
        paths.append(path)
        image_names.append(image_name.split('.'))

    raw_images = []
#     read numpy arrays
    for path in paths:
        image = cv2.imread(path,1)
        raw_images.append(image)
        
#     convert to python list 
    images = []
    for image in raw_images:
        image = image.tolist()
        images.append(image)
    return images,image_names


def write_image(image, image_name, filter_name):
    name = image_name[0]+'_'+filter_name+'.'+image_name[1]
    cv2.imwrite(name,np.asarray(image))
	
	
def wrap_image(images):
    for image in images:
        image.insert(0,image[-1]+[])
        image.append(image[1]+[])
        for k in range(len(image)):
            image[k].insert(0,image[k][-1]+[])
            image[k].append(image[k][1]+[])
    return images

def mean_filter(image, kernel_size):
    height = len(image)
    width = len(image[0])
    kernel = [[1]*kernel_size for i in range(kernel_size)]
    kernel_elements = kernel_size**2
    
    result = []
    
    middle = kernel_size // 2
    for y in range(middle, (height-middle)):
        result_row = []
        for x in range(middle, (width-middle)):
            value_r = 0
            value_g = 0
            value_b = 0
            for a in range(kernel_size):
                for b in range(kernel_size):
                    blu = (kernel[a][b]*image[y-middle+a][x-middle+b][0])
                    grn = (kernel[a][b]*image[y-middle+a][x-middle+b][1])
                    red = (kernel[a][b]*image[y-middle+a][x-middle+b][2])
                    value_r+=red
                    value_g+=grn
                    value_b+=blu
            
            result_row.append([int(value_b/kernel_elements),int(value_g/kernel_elements),int(value_r/kernel_elements)])
        result.append(result_row)
    return result

def median_filter(image, kernel_size):
    height = len(image)
    width = len(image[0])
    kernel = [[1]*kernel_size for i in range(kernel_size)]
    kernel_elements = kernel_size**2
    
    result = []
    
    middle = kernel_size // 2
    for y in range(middle, (height-middle)):
        result_row = []
        for x in range(middle, (width-middle)):
            value_r = []
            value_g = []
            value_b = []
            for a in range(kernel_size):
                for b in range(kernel_size):
                    blu = image[y-middle+a][x-middle+b][0]
                    grn = image[y-middle+a][x-middle+b][1]
                    red = image[y-middle+a][x-middle+b][2]
                    value_r.append(red)
                    value_g.append(grn)
                    value_b.append(blu)
            value_r = sorted(value_r)
            value_g = sorted(value_g)
            value_b = sorted(value_b)
            result_row.append([int(value_b[kernel_elements//2]),int(value_g[kernel_elements//2]),int(value_r[kernel_elements//2])])
        result.append(result_row)
    return result
            

def mid_point_filter(image, kernel_size):
    height = len(image)
    width = len(image[0])
    kernel = [[1]*kernel_size for i in range(kernel_size)]
    kernel_elements = kernel_size**2
    
    result = []
    
    middle = kernel_size // 2
    for y in range(middle, (height-middle)):
        result_row = []
        for x in range(middle, (width-middle)):
            value_r = []
            value_g = []
            value_b = []
            for a in range(kernel_size):
                for b in range(kernel_size):
                    blu = image[y-middle+a][x-middle+b][0]
                    grn = image[y-middle+a][x-middle+b][1]
                    red = image[y-middle+a][x-middle+b][2]
                    value_r.append(red)
                    value_g.append(grn)
                    value_b.append(blu)
            value_r = sorted(value_r)
            value_g = sorted(value_g)
            value_b = sorted(value_b)
            result_row.append([int((value_b[0]+value_b[-1])/2),int((value_g[0]+value_g[-1])/2),int((value_r[0]+value_r[-1])/2)])
        result.append(result_row)
    return result
            
# executable main func
def main(kernel_size=3): #default kernel size 3 by 3
    images, image_names = read_all_images()
    images = wrap_image(images)
    index = 0
    for image in images:
        mean_result = mean_filter(image,kernel_size)
        write_image(mean_result,image_names[index], 'mean')
        median_result = median_filter(image,kernel_size)
        write_image(median_result, image_names[index], 'median')
        mid_point_result = mid_point_filter(image,kernel_size)
        write_image(mid_point_result, image_names[index], 'mid_point')

        index+=1

main(kernel_size=3)


import os
import sys
import numpy as np
from tqdm import tqdm
import cv2
from socket import gethostname
from DTE.imresize_DTE import imresize

dataset_root_path = '/home/ybahat/Datasets' if gethostname() == 'ybahat-System-Product-Name' else '/home/tiras/datasets' if 'tiras' in os.getcwd() else '/home/ybahat/data/Databases'
# input_folder = os.path.join(dataset_root_path,'DIV2K/DIV2K_train_HR_sub')
# save_LR_folder = os.path.join(dataset_root_path,'DIV2K/DIV2K_train_HR_sub_bicLRx4')
scale_factor = 4
dataset_name = 'DIV2K_train'#'Set14'
data_category_string = '_sub'#'_train'
input_folder = os.path.join(dataset_root_path,'%s/%s%s_HR'%(dataset_name,dataset_name,data_category_string))
save_HR_folder = os.path.join(dataset_root_path,'%s/%s%s_HRx%d'%(dataset_name,dataset_name,data_category_string,scale_factor))
save_LR_folder = os.path.join(dataset_root_path,'%s/%s%s_bicLRx%d'%(dataset_name,dataset_name,data_category_string,scale_factor))

up_scale = scale_factor
mod_scale = scale_factor

def mod_img(image,modulu):
    if image.ndim<3:
        image = image.reshape(list(image.shape)+[1])
    im_shape = image.shape[:2]
    im_shape -= np.mod(im_shape,modulu)
    return image[:im_shape[0],:im_shape[1],:]

assert save_LR_folder is None or not os.path.exists(save_LR_folder),'Folder [{:s}] already exists. Exit...'.format(save_LR_folder)
assert save_HR_folder is None or not os.path.exists(save_HR_folder),'Folder [{:s}] already exists. Exit...'.format(save_HR_folder)
if save_LR_folder is not None:
    os.makedirs(save_LR_folder)
    print('mkdir [{:s}] ...'.format(save_LR_folder))
if save_HR_folder is not None:
    os.makedirs(save_HR_folder)
    print('mkdir [{:s}] ...'.format(save_HR_folder))

# img_list = []
# for file_name in os.listdir(input_folder):
#     img_list.append(os.path.join(input_folder,file_name))
progress_bar = tqdm(os.listdir(input_folder))
for file_name in progress_bar:
    cur_im = mod_img(cv2.imread(os.path.join(input_folder,file_name)),mod_scale)
    cv2.imwrite(os.path.join(save_HR_folder,file_name),cur_im)
    if save_LR_folder is not None:
        # cur_im = cv2.resize(cur_im,dsize=(0,0),fx=1/up_scale,fy=1/up_scale,interpolation = cv2.INTER_CUBIC)
        cur_im = imresize(cur_im,scale_factor=[1/float(up_scale)])
        cv2.imwrite(os.path.join(save_LR_folder,file_name),cur_im)



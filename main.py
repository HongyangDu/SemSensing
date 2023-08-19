import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import time
import math
import numpy as np
from numpy import *
import scipy.io as sio
from statistics import mean
from PnP_DIP import *
from utils import *
import cv2

sample = 'Demo'
save_path = './Result/result'+ sample + '/'
if not os.path.exists(save_path):
    os.makedirs(save_path)
index = int('01')
# SP = sio.loadmat('AReal.mat')['AReal']
SP = sio.loadmat('AmReN.mat')['AmReN']
_, _, sp_nC = SP.shape

# Compress
Com_Length = 10

SPS = []
for i in range(Com_Length):
    SPS.append(SP[:,:,i])
X_ori = np.array(SPS)
X_ori = X_ori.transpose((1, 2 ,0))
r, c, nC = X_ori.shape
Ammax = X_ori.max()
Ammin = X_ori.min()
X_ori = X_ori / Ammax
shift_step = 40 # Change DIP_denoising.py % Line 34 outshift = shift_torch(model_out, 3)
X_ori_shift = shift(X_ori, shift_step)
rs, cs, nCs = X_ori_shift.shape

# =================== Random Get Phi ===================
N = 2**4
nums = np.linspace(0.1, 1, num=N, dtype=float)
Phi = np.zeros(X_ori_shift.shape)
Phi = Phi.reshape(-1)
from tqdm import tqdm
for i in tqdm(range(len(Phi))):
    ind = np.random.randint(0, len(nums), 1)
    Phi[i] = nums[ind]
Phi = Phi.reshape(X_ori_shift.shape)
# =================== Random Get Phi ===================
# =================== Random Get Phi by Shift===================
# N = 8
# nums = np.linspace(0.1, 1, num=N, dtype=float)
# X_one = X_ori[:,:,1];
# Phi = np.zeros(X_one.shape)
# Phi = Phi.reshape(-1)
# from tqdm import tqdm
# for i in tqdm(range(len(Phi))):
#     ind = np.random.randint(0, len(nums), 1)
#     Phi[i] = nums[ind]
# Phi = Phi.reshape(X_one.shape)
# Phi = shiftH(Phi, shift_step,nC)
# =================== Random Get Phi by Shift===================
# If wannt to use own H
# Phi = sio.loadmat('NCodeH.mat')['NCodeH'] # 10 compress length
# Phi = shift(Phi, shift_step)
# =========================================================

# =================== Encode ===================
sio.savemat(save_path + 'CodeH.mat',{'Phi': Phi})
Phi_sum = np.sum(Phi**2,2)
Phi_sum[Phi_sum==0]=1

y = A(X_ori_shift,Phi)
sio.savemat(save_path + 'Compressive.mat',{'y': y})
print('Encoding is done, please check the Compressive.mat')
# =================== Initial Setting ===================
# tvdip_num = 60
# mu = 0.01
# eta = 0
# denoiser = 'DIP'
# iter_num = tvdip_num
# tv_weight = 0.1
# tv_iter_num = 5
# dip_iter = [500]*10 + [700]*20 +[1200]*30
# shift_step = 2
# rho = 0.01
# =================== Check Security ===================
# N = 2**4
# nums = np.linspace(0.1, 1, num=N, dtype=float)
# Phi = np.zeros(X_ori_shift.shape)
# Phi = Phi.reshape(-1)
# from tqdm import tqdm
# for i in tqdm(range(len(Phi))):
#     ind = np.random.randint(0, len(nums), 1)
#     Phi[i] = nums[ind]
# Phi = Phi.reshape(X_ori_shift.shape)
# =================== Check Security ===================

# =================== Decoding ===================
tvdip_num = 60
eta = 0
mu = 0.01
rho = 0.01
denoiser = 'DIP'
iter_num = tvdip_num
tv_weight = 0.1
tv_iter_num = 5#5
multichannel = True

dip_iter = [500]*10 + [700]*20 +[1200]*30 # real

ch = nC
x_rec = admm_dip(y, Phi, Phi_sum, eta, mu, rho,denoiser, iter_num, tv_weight, tv_iter_num,multichannel, shift_step,dip_iter, index, X_ori, save_path,ch)

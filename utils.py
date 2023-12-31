''' Utilities '''
import math
import numpy as np
import torch
import scipy.io as sio

'''
Forward model of snapshot compressive imaging (SCI), where multiple coded
frames are collapsed into a snapshot measurement.
'''
def A(x, Phi):
    return np.sum(x*Phi, axis=2)  # element-wise product

def At(y, Phi):
    '''
    Tanspose of the forward model. 
    '''
    return np.multiply(np.repeat(y[:,:,np.newaxis],Phi.shape[2],axis=2), Phi)

def psnr_block(ref, img):
    psnr = 0
    r,c,n = img.shape
    PIXEL_MAX = ref.max()
    for i in range(n):
        mse = np.mean( (ref[:,:,i] - img[:,:,i]) ** 2 )
        psnr += 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return psnr/n

def psnr_torch(ref, img):
    psnr = 0
    r, c, n = img.shape
    for i in range(r):
        mse = torch.mean( (ref[i,:,:] - img[i,:,:]) ** 2 )
        psnr += 20 * torch.log10(1 / mse.sqrt())
    return psnr/(r)

def shift_back(inputs,step):
    [row,col,nC] = inputs.shape
    for i in range(nC):
        inputs[:,:,i] = np.roll(inputs[:,:,i],(-1)*step*i,axis=1)
    output = inputs[:,0:col-step*(nC-1),:]
    return output

def shift(inputs,step):
    [row,col,nC] = inputs.shape
    output = np.zeros((row, col+(nC-1)*step, nC))
    for i in range(nC):
        output[:,i*step:i*step+col,i] = inputs[:,:,i]
    return output

def getgap(inputs):
    [row,col,nC] = inputs.shape
    output = np.zeros((row-1,col,nC))
    for i in range(nC):
        for ir in range(row-1):
            t1 = inputs[:,ir + 1,i]
            t2 = inputs[:,ir ,i]
            # to = [t1[it]-t2[it] for it in range(0,len(t1))]
            to = t1 - t2
            output[ir, :, i] = to
    return output

def shiftH(inputs,step,nC):
    [row,col] = inputs.shape
    output = np.zeros((row, col+(nC-1)*step, nC))
    for i in range(nC):
        output[:,i*step:i*step+col,i] = inputs[:,:]
    return output

def A_torch(x,Phi):
    temp = x*Phi
    y = torch.sum(temp,1)
    return y

def At_torch(y,Phi):
    temp = torch.unsqueeze(y, 1).repeat(1,Phi.shape[1],1,1)
    x = temp*Phi
    return x

def shift_torch(inputs,step):
    [bs, nC, row, col] = inputs.shape
    output = torch.zeros(bs, nC, row, col+(nC-1)*step)
    for i in range(nC):
        output[:, i, :, i*step:i*step+col] = inputs[:, i,:,:]
    return output.cuda()

def shift_back_torch(inputs, step):          # input [bs,256,310]  output [bs, 28, 256, 256]
    [bs, nC, row, col] = inputs.shape
    output = torch.zeros(bs, nC, row, col-(nC-1)*step).cuda().float()
    for i in range(nC):
        output[:,i,:,:] = inputs[:, i, :, step*i:step*i+col-(nC-1)*step]
    return output


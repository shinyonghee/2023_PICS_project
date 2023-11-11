import matplotlib.pyplot as plt
import matplotlib.scale as scale
from mpl_toolkits.mplot3d import axes3d
import pandas as pd

from circuit_analysis import simulate
import random
import numpy as np
import csv
import os
import time
import math
topic_list=['FOM', 'PM', 'UBW', 'power', 'ts', 'DC_gain' ]
Low= 200e-9; High=8000e-9

def edit_FOM(w1):
    num=500 # should be modified

    topic="new_FOM"
    global time_dir
    csv_dir = f"csv/{time_dir}"
    global plot_dir
    csv_dir = f"csv/{time_dir}"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    
    filename = 'w1_%.3e.csv'%w1   
    data=pd.read_csv(f'{csv_dir}/{filename}')
    num_result=5
    X=data['w2']
    Y=data['w3']
    result=[[] for i in range(num_result)]
    Z={}
    for i in topic_list:
        Z[i]=list(data[i])
    # result=np.zeros((num,1))
    for i in range(num):
        for j in range(num_result):
            result[j].append((FOM(Z['PM'][i], Z['UBW'][i], Z['power'][i], Z['ts'][i], Z['DC_gain'][i]))[j])
    X=np.array(X)
    Y=np.array(Y)
    result=np.array(result)
    power=np.array(data['power'])
    FOM1=np.array(data['FOM'])

    fig=plt.figure(figsize=(16,10))
    for i in range(num_result):
        
        ax = fig.add_subplot(position[i], projection = '3d')

        sc=ax.scatter(X,Y,result[i], s=15, c=result[i], cmap='coolwarm')
        # cbar = plt.colorbar(sc)
        ax.set_zlim(-200,200)   
        if i==0: ax.set_zlim(-100,0) 
        ax.set_xlabel('W2')
        ax.set_ylabel('W3')
        ax.set_zlabel(i)
        A=result[i]
        plt.title(f'result{i}:{name[i]} '+ ', W1=%.3e, mean: %.3e'%(w1, np.mean(A))+"""
                  """+"max: %.3e"%np.max(A))
        # if(i==0): print(np.min(A), np.max(A), np.mean(A))
        plot_filename = topic+ ', w1_%.3e'%w1 
    plt.savefig(f"{plot_dir}/{plot_filename}.png", dpi=300)
    
    # plt.show()
    plt.clf()

position=[231,232,233,234, 235]   
name=["TOTAL", "UBW", "power", "ts", "DC_gain"]

def FOM(PM, UBW, power, ts, DC_gain):
    result1 =  100*math.log(10*UBW/218596568.9, 10)#/163243273.8
    result2 = -300*math.log(10*power/0.000833898, 10)#/0.000455899
    result3= -160*math.log(10*ts/1.13201E-08, 10)#/9.99672E-09
    result4= 50*math.log(10*DC_gain/8.400556199, 10)#/1.900599041

    # result1=(UBW-218596568.9)/163243273
    # result2=(power-0.000833898)/0.000455899
    # result3 = (ts-1.13201E-08)/9.99672E-09
    # result4= (DC_gain-8.400556199)/1.900599041

    result=result1+result2+result3+result4
    

    if(PM>60): result=result+100
    else: result = result-100
    # print(result)
    return result, result1, result2, result3, result4
   
    
if __name__=='__main__':
    time_dir=time.strftime('%m.%d_%H.%M.%S') 
    plot_dir = f"plot_new_FOM/{time_dir}"
    time_dir="11.09_23.11.04"
    for i in range(200,1000, 100):
        edit_FOM(i*1e-9)

    
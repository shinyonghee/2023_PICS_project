import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pandas as pd

from circuit_analysis import simulate
import random
import numpy as np
import csv
import os
import time

topic_list=['FOM', 'PM', 'UBW', 'power', 'ts', 'DC_gain' ]
Low= 200e-9; High=8000e-9

def csv_write(num, w1=-1):
    csv_dir = f"csv/{time_dir}"
    filename = 'w1_%.3e.csv'%w1   
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    data = np.zeros((num, len(topic_list)+3))

    # data=[
    #       [w1],
    #       [w2],
    #       [w3],
    #       [FOM],
    #        ...
    #           ]

    f=open(f'{csv_dir}/{filename}','w',newline='')
    wr=csv.writer(f)
    wr.writerow(['w1','w2','w3']+topic_list)
    
    for i in range(num):
        w2=random.uniform(Low, High)
        w3=random.uniform(Low, High)
        data[i][0]=w1 
        data[i][1]=w2
        data[i][2]=w3
        
        
        # (PM, UBW, power)
        flag=True
        while(flag):
            try:
                result=simulate(float(w1),float(w2),float(w3))
                flag=False
            except:
                print("Error: ", end="")
                print(w1,w2,w3)
                w2=random.uniform(Low, High)
                w3=random.uniform(Low, High)  
        for j in range(len(topic_list)):
            data[i][j+3]=result[j]
        wr.writerow(data[i])
                
    f.close()

def plot(topic, w1):
    global time_dir
    plot_dir = f"plot/{time_dir}/{topic}"
    csv_dir = f"csv/{time_dir}"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    
    filename = 'w1_%.3e.csv'%w1   
    data=pd.read_csv(f'{csv_dir}/{filename}')

    X=data['w2']
    Y=data['w3']
    Z=data[topic]

    fig=plt.figure(topic)
    ax = fig.add_subplot(projection = '3d')

    ax.scatter(X,Y,Z, marker='o', s=15, c='darkgreen')

        
    ax.set_xlabel('W2')
    ax.set_ylabel('W3')
    ax.set_zlabel(topic)
    plt.title(topic+ ', W1=%.3e, [%.3e, %.3e]'%(w1, Z.min(), Z.max()))
    plot_filename = topic+ ', w1_%.3e.csv'%w1 
    plt.savefig(f"{plot_dir}/{plot_filename}.png", dpi=300)

    plt.clf()


    
if __name__=='__main__':
    time_dir=time.strftime('%m.%d_%H.%M.%S') 
    # time_dir="11.09_22.19.17"
    for i in range(200,1000,100):
        w1=i*1e-9
        csv_write(100, w1)
        for topic_ in topic_list:
            plot(topic_, w1)
 

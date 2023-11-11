# Pyspice (Python) code to simulate MOSFET Amplifier Circuit
######################################################################
# env: circuit_analysis: conda
# last updated: 2023.11.01.
# STANDARD DECLARATIONS
# ------------------------
import warnings
from PySpice.Probe.WaveForm import WaveForm

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="PySpice.Probe.WaveForm")


import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
import math
#from engineering_notation import EngNumber

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Unit import *
import random

do_print = False
do_plot= False
output_cap = 1e-6@u_pF
w0=200e-9
def draw_bode(analysis, UBW):
    figure, axes = plt.subplots(2, figsize=(20, 10))
    plt.title("Bode Diagram of a one-stage amp")
    bode_diagram(axes=axes,
                frequency=analysis.frequency,
                gain=20*np.log10(np.absolute(analysis.out)),
                phase=np.angle(analysis.out, deg=False),
                marker='.',
                color='blue',
                linestyle='-',
    )
    for ax in axes:
        ax.axvline(x=UBW, color='red')
    plt.tight_layout()
    plt.show()

def simulate(w1=200E-9,w2=200E-9,w3=200E-9):
    myL=0.13E-6 #fixed
    global w0
    # CIRCUIT NETLIST
    # ------------------------

    circuit = Circuit('Common-Source MOSFET Amplifier')

    # Define amplitude and frequency of input sinusoid
    amp=0.01@u_mV
    freq=1@u_kHz
    # Define transient simulation step time and stop time
    steptime=100@u_us
    finaltime = 0.01@u_s
    voltage_provide = 1.3@u_V
    # Define MOSFET models
    # https://ltwiki.org/LTspiceHelp/LTspiceHelp/M_MOSFET.htm
    # https://ltwiki.org/index.php?title=Standard.mos

    # simplified model
    #circuit.model('2N00', 'NMOS', Kp=0.13, Vto=2.475)

    # simplified model with channel length and width
    # circuit.model('N1', 'NMOS',level=54, L=myL, W=w1)
    # circuit.model('N2', 'NMOS', level=54,L=myL, W=w2)
    # circuit.model('P3', 'PMOS', level=54, L=myL, W=w3)
    circuit.model('N0', 'NMOS', level=54, L=myL, W=w0)
    circuit.model('N1', 'NMOS', level=54, L=myL, W=w1)
    circuit.model('N2', 'NMOS', level=54, L=myL, W=w2)
    circuit.model('P3', 'PMOS', level=54, L=myL, W=w3)

    # M <name> <drain node> <gate node> <source node> <bulk/substrate node>
    source = circuit.SinusoidalVoltageSource(3, 'input', 'V2') #amplitude=0.1@u_mV)
    circuit.V('power','VP',circuit.gnd, voltage_provide)
    circuit.R(1, 'VP', 'M1D', 10@u_kOhm)
    circuit.MOSFET(1, 'M1D', 'M1D', circuit.gnd, circuit.gnd, model='N0')
    circuit.MOSFET(2, 'M2D', 'M1D', circuit.gnd, circuit.gnd, model='N1')
    circuit.MOSFET(3, 'M3D', 'input', 'M2D', 'M2D', model='N2')
    circuit.MOSFET(4, 'out', 'V1', 'M2D', 'M2D', model='N2')
    circuit.V(1, 'V1', circuit.gnd, 0.8@u_V)
    circuit.V(2, 'V2', circuit.gnd, 0.8@u_V)
    circuit.MOSFET(5, 'M3D', 'M3D', 'VP', 'VP', model='P3')
    circuit.MOSFET(6, 'out', 'M3D', 'VP', 'VP', model='P3')
    circuit.C(1, 'out', circuit.gnd, output_cap)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    simulator.save_currents = True
    analysis = simulator.ac(start_frequency=1@u_Hz, stop_frequency=100@u_GHz, number_of_points=10,  variation='dec')
    
    # evaluate UBW, PM, DC_gain, ts
    UBW=0
    PM=0
    DC_gain=float(np.absolute(analysis.out)[0])
    for i in range(len(np.absolute(analysis.out))):
        if np.absolute(analysis.out)[i]<1:
            UBW=float(analysis.frequency[i])
            PM=np.angle(analysis.out, deg=False)[i]*180/math.pi
            break
    PM=PM+180
    if(do_plot): draw_bode(analysis, UBW)
    ts=get_ts(w1,w2,w3)
    analysis2= simulator.operating_point()
    
    current = abs(float(analysis2.branches['vpower']))
    power = float(voltage_provide*current)

    
    if(do_print):
        print("="*20+"result"+"="*20)
        print(f"DC gain: {DC_gain} [V/V]")
        print(f"Phase Margin: {PM} [degree]")
        print("Power: %.5e [W]" %power)
        print("Unity-gain bandwidth: %.5e [Hz]"%UBW)
        print(f"1% settling time: {ts} [s]")
        print(f"FOM: {FOM(PM, UBW, power, ts)}")
        print("="*46)
    
    
    # topic_list=['FOM', 'PM', 'UBW', 'power', 'ts']
    return FOM(PM,UBW,power, ts, DC_gain), PM, UBW, power, ts, DC_gain


def get_ts(w1=200E-9,w2=200E-9,w3=200E-9):
    myL=0.13E-6 #fixed
    # CIRCUIT NETLIST
    # ------------------------
    global w0
    circuit = Circuit('Common-Source MOSFET Amplifier')

    # Define amplitude and frequency of input sinusoid
    amp=0.01@u_mV
    freq=1@u_kHz
    # Define transient simulation step time and stop time
    steptime=1@u_ns
    finaltime = 1@u_us
    voltage_provide=1.3@u_V
    # Define MOSFET models
    # https://ltwiki.org/LTspiceHelp/LTspiceHelp/M_MOSFET.htm
    # https://ltwiki.org/index.php?title=Standard.mos

    # simplified model
    #circuit.model('2N00', 'NMOS', Kp=0.13, Vto=2.475)

    # simplified model with channel length and width
    # circuit.model('N1', 'NMOS',level=54, L=myL, W=w1)
    # circuit.model('N2', 'NMOS', level=54,L=myL, W=w2)
    # circuit.model('P3', 'PMOS', level=54, L=myL, W=w3)
    circuit.model('N0', 'NMOS', level=54, L=myL, W=w0)
    circuit.model('N1', 'NMOS', level=54, L=myL, W=w1)
    circuit.model('N2', 'NMOS', level=54, L=myL, W=w2)
    circuit.model('P3', 'PMOS', level=54, L=myL, W=w3)

    # M <name> <drain node> <gate node> <source node> <bulk/substrate node>
    #source = circuit.SinusoidalVoltageSource(3, 'input', 'V2') #amplitude=0.1@u_mV)
    circuit.PulseVoltageSource(3, 'input', 'V2', initial_value=-0.1, pulsed_value=0.1, pulse_width=1e-2, period=1e-2, rise_time= 1@u_ps, delay_time=0)
    circuit.V('power','VP',circuit.gnd, voltage_provide)
    circuit.R(1, 'VP', 'M1D', 10@u_kOhm)
    circuit.MOSFET(1, 'M1D', 'M1D', circuit.gnd, circuit.gnd, model='N0')
    circuit.MOSFET(2, 'M2D', 'M1D', circuit.gnd, circuit.gnd, model='N1')
    circuit.MOSFET(3, 'M3D', 'input', 'M2D', 'M2D', model='N2')
    circuit.MOSFET(4, 'out', 'V1', 'M2D', 'M2D', model='N2')
    circuit.V(1, 'V1', circuit.gnd, 0.8@u_V)
    circuit.V(2, 'V2', circuit.gnd, 0.8@u_V)
    circuit.MOSFET(5, 'M3D', 'M3D', 'VP', 'VP', model='P3')
    circuit.MOSFET(6, 'out', 'M3D', 'VP', 'VP', model='P3')
    circuit.C(1, 'out', circuit.gnd, output_cap)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=finaltime)


    final_value=analysis['out'][-1]
    t_s=-1
    for i in range(len(analysis['out'])):
        if abs(analysis['out'][i]-final_value)<0.01*final_value and t_s==-1:
            t_s=analysis.time[i]
        elif abs(analysis['out'][i]-final_value)>0.01*final_value:
            t_s=-1
    if(do_plot):
        figure, axe = plt.subplots(figsize=(11, 6))

        plt.title('MOSFET Amplifier Voltages')
        plt.xlabel('Time [s]')
        plt.ylabel('Voltage [V]')
        plt.grid()
        plot(analysis['out'], 'r', axis=axe)
        plot(analysis['input'], 'g', axis=axe) 


        axe.axvline(x=float(t_s), color='blue') 

        plt.show()
    return float(t_s)



def FOM5(PM, UBW, power,ts=0):
    result1 = -10*math.log(power*1e4, 10)
    result2 =  math.log(UBW*1e-6, 10)
    # result3= 2*math.log(ts*1e8, 10)
    # print(result1,result2,result3)
    result=result1+result2
    if(PM>60): result=result
    else: result = result-50
    return result

def FOM1(PM, UBW, power,ts=0):
    result1 = -10*math.log(power*1e1, 10)
    result2 =  10*math.log(UBW*1e-6, 10)
    # result3= -5*math.log(ts*1e7, 10)
    print(result1,result2)
    result=result1+result2
    if(PM>60): result=result+50
    else: result = result-50
    return result

def FOM_presented(PM, UBW, power, ts):
    result1 = -30*math.log(power*1e3, 10)
    result2 =  10*math.log(UBW*1e-6, 10)
    result=result1+result2
    if(PM>60): result=result+50
    else: result = result-50
    return result


def FOM_(PM, UBW, power, ts):
    result1 =  100*math.log(UBW/218596568.9, 10)/0.75
    result2 = -100*math.log(power/0.000833898, 10)/0.55
    result3= -100*math.log(ts/1.13201E-08, 10)/0.88
    result=result1+result2+result3
    # 

    if(PM>60): result=result+100
    else: result = result-100
    # print(result)
    return result

def FOM(PM, UBW, power, ts, DC_gain):
    result1 =  100*math.log(10*UBW/218596568.9, 10)#/163243273.8
    result2 = -300*math.log(10*power/0.000833898, 10)#/0.000455899
    result3= -150*math.log(10*ts/1.13201E-08, 10)#/9.99672E-09
    result4= 120*math.log(10*DC_gain/8.400556199, 10)#/1.900599041

    result=result1+result2+result3+result4
    

    if(PM>60): result=result+100
    else: result = result-100
    # print(result)
    return result
   
if __name__=='__main__':
    # simulate(random.uniform(200e-9, 3000e-9), random.uniform(200e-9, 3000e-9), random.uniform(200e-9, 3000e-9))
    # print(simulate(7.78342104e-07 4.56479308e-06 8.47126245e-07))
    # get_ts(300e-9,9.519691e-07, 7.821263e-06)
    # for i in range(100):
    #     w1=i*1e-9
    #     simulate(random.uniform(200e-9, 3000e-9), random.uniform(200e-9, 3000e-9), random.uniform(200e-9, 3000e-9))
    print(simulate( 4.606278935596872e-06, 2e-07, 4.560121343600643e-06))




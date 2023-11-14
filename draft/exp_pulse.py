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
# Define the circuit
circuit = Circuit('Exponential Example')
# circuit.PulseVoltageSource(1, 'exp', circuit.gnd, initial_value=-0.1, pulsed_value=0.1, pulse_width=1e-2, period=1e-2, rise_time= 1@u_ps, delay_time=0)
circuit.PulseVoltageSource(3, 'input1', circuit.gnd, initial_value=0, pulsed_value=0.01, pulse_width=1e-2, period=1e-2, rise_time= 1@u_ps, delay_time=0)
steptime=1@u_ps
finaltime = 1@u_us
# Define the exponential source for a rising waveform
circuit.V(4, 'input2', circuit.gnd,'pulse(0 0.02 0 0 1e-20 0 1e-2)')  # pulse(input, low, high, delay, rise_time, fall_time, width)
# circuit.V('input', 'in', circuit.gnd, 'pulse(0 5 0 1u 1u 1u 2u)')  # pulse(input, low, high, delay, rise_time, fall_time, width)

# Perform a transient analysis

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=steptime, end_time=finaltime) #we don't consider under 1e-6 [s] 

# Plot the results
time = analysis.time
voltage = analysis['input1']
voltage2=analysis['input2']
figure, axe = plt.subplots(figsize=(11, 6))
plot(analysis['input1'], 'r', axis=axe)
plot(analysis['input2'], 'g', axis=axe) 
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Exponential Rising Waveform')
plt.grid(True)
plt.show()


# circuit.V(3, 'input', 'V2','pulse(0 5 0 1u 1u 1u 2u)')  # pulse(input, low, high, delay, rise_time, fall_time, width)
# circuit.V('input', 'in', circuit.gnd, 'pulse(0 5 0 1u 1u 1u 2u)')  # pulse(input, low, high, delay, rise_time, fall_time, width)
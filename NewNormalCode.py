import math
import numpy as np
from matplotlib import pyplot as plt

# Constants
V_mp = 2.4
I_mp = 0.5
Diag_Germany = math.sqrt(876 * 876 + 640 * 640)
P_mp = V_mp * I_mp
N_c = 7
P_u3 = P_mp * N_c
Eff = 0.8
P_diodess_less = 0.45
G = 398600.5
r = 6378.14
W_rasp_peak = 10
W_rasp_av = 8
Camera_Energy = 5.5 # W/h

#Coef_weight = 15.3044 / 1024

Coef_weight = 0.0203  #15.3044 / 1024

Coef_number_clasters = 91.36 / (1024 * 676)

Coef_claster_time = 676 / 6.28

#(Coef_number_clasters * Coef_claster_time)

G_coef = 6.67430e-2
M_earth = 5.972e24

S_band_trasmit = 17000 / 1000
S_band_receive = 1830 / 1000
S_band_trasmit_receive = 18830 / 1000
UHF_receive = 138 / 1000
UHF_transmit = 6112 / 1000

S_band_av = 3769 / 1000
UHF_av = 168 / 1000

OCS = (4978 / 1000) * (60/95)
EPS = (40 / 1000) * (60/95)
OBC = (14 / 1000) * (60/95)
ADCS = (470 / 1000) * (60/95)
GPS = (25/1000) * (60/95)
ISL = (168/1000) * (60/95)
PAN = (168/1000) * (60/95)

OCS_peak = (38650 / 1000) * (60/95)
EPS_peak = EPS
OBC_peak = (50/1000) * (60/95)
ADCS_peak = (5373/1000) * (60/95)
GPS_peak = (165/1000) * (60/95)
ISL_peak = 0
PAN_peak = PAN



#print((OCS+EPS+OBC+ADCS)*95/60)

h = [r + i for i in range(150, 2000)]
Height_under_the_Earth = [i for i in range(150, 2000)]
energy_to_transmit_image = []

P_solar_battery = P_u3 * Eff - P_diodess_less

P_average = []
Time_under_Germany = []
T_Period_of_flight_for_every = []
T_Sunny = []
Time_to_transmit_image = []



for height in h:
    T_Period_of_flight = 2 * math.pi * np.sqrt(pow(height, 3) / G) / 60
    T_Period_of_flight_for_every.append(T_Period_of_flight)
    Speed_of_satellites = np.sqrt(G_coef * M_earth / height) / 1000000000
    #print(Speed_of_satellites)
    Time_under_Germany.append(Diag_Germany / Speed_of_satellites / 60)
    #print(Diag_Germany / Speed_of_satellites / 60)
    T_Sunny_period = T_Period_of_flight * (1 - math.asin(r / height) / math.pi)
    T_Sunny.append(T_Sunny_period)
    P_average.append(P_solar_battery * T_Sunny_period / 60)
    #if (height - r) == 500:
        #print(T_Sunny_period)
        #print(T_Period_of_flight)
        #print(P_solar_battery)
        #print(P_solar_battery * T_Sunny_period / 60)

# Photo related calculations
S_Germany = 876 * 640
Pixels_based = 4096
Length_based = 19.6
Height_based = 500
K_based = Length_based / Height_based
bait = 28
coef_for_clasters = (735 / 200)
claster_info_one_string = 34 / 1024 / 1024 # length of string with GPS coor, size of claster, and 3 extra for type of claster

Weight_of_image = []
Time_to_compute = []
discharge_per_cycle = []

discharge_per_cycle_only_flight = []

Energy_per_rasp_average = []
discharge_Energy_per_rasp_average = []
Energy_per_rasp_peak = []
discharge_Energy_per_rasp_peak = []

energy_to_transmit_image = []

v_information_S_band = 0.5 # Мбайт/сек, 4 Мбит/сек
v_information_UHF_band = 0.125 # Мбайт/сек, 1Мбит/сек

Energy_Safe_Mode_average = []
discharge_Energy_Safe_Mode_average = []
Energy_Safe_Mode_peak = []
discharge_Energy_Safe_Mode_peak = []




Energy_Nominal_Mode_average = []
discharge_Energy_Nominal_Mode_average = []
Energy_Nominal_Mode_peak = []
discharge_Energy_Nominal_Mode_peak = []



Dis_Safe_Mode=[]
Dis_Nominal_Mode=[]

Energy_without_cameras = []
Energy_only_photos = []
i = 0
for length in h:
    Energy_to_Camera = Camera_Energy / 60 * Time_under_Germany[i]
    #print(Time_under_Germany[i], Energy_to_Camera)
    #print(Energy_to_Camera)

    height = length - r
    pixels = height * K_based
    square = pixels / Pixels_based
    height_pix = math.ceil(Diag_Germany / square)
    weight = Pixels_based * height_pix * bait / 1024 / 1024 / 1024
    Weight_of_image.append(weight)
    print((length - r), weight * 1024)
    timer = weight / (Coef_number_clasters * Coef_claster_time) / 60
    timer_transmit = weight / Coef_claster_time / 60
    #print(timer)
    Time_to_compute.append(timer)

    Time_to_transmit_image.append(((weight * 1024)/ (v_information_UHF_band)) / 60 / 60)
    energy_transmit = (weight / Coef_claster_time) * (claster_info_one_string / v_information_UHF_band) * (UHF_transmit) / 60 / 60 + (weight / Coef_claster_time) * (claster_info_one_string / v_information_S_band) * (S_band_trasmit) / 60 / 60

    #if length - r == 500:
        #print(timer * W_rasp_av / 60)

    #energy_transmit = (weight / coef_for_clasters) / claster_info_one_string * v_information_UHF_band * UHF_transmit / 60 / 60
    energy_to_transmit_image.append(energy_transmit)

    #Average_var =

    Energy_per_rasp_average.append(timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit + (OCS + EPS + OBC + ADCS + GPS + ISL + PAN) / 60 * T_Period_of_flight_for_every[i])
    Energy_per_rasp_peak.append(timer * W_rasp_peak / 60 + Energy_to_Camera + energy_transmit + (OCS_peak + EPS_peak + OBC_peak + ADCS_peak + GPS_peak + ISL_peak + PAN_peak) / 60 * T_Period_of_flight_for_every[i])

    discharge_Energy_per_rasp_average.append(P_average[i] - Energy_per_rasp_average[i])
    discharge_Energy_per_rasp_peak.append(P_average[i] - Energy_per_rasp_peak[i])


    Energy_without_cameras.append((OCS + EPS + OBC + ADCS + GPS + ISL + PAN) / 60 * T_Period_of_flight_for_every[i])
    Energy_only_photos.append(timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit)
    discharge = P_average[i] - (timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit + (OCS + EPS + OBC + ADCS) / 60 * T_Period_of_flight_for_every[i])
    discharge_per_cycle.append(discharge)

    Energy_Safe_Mode_average.append((OBC + EPS + PAN) / 60 * T_Period_of_flight_for_every[i])
    Energy_Safe_Mode_peak.append((OBC_peak + EPS_peak + PAN_peak) / 60 * T_Period_of_flight_for_every[i])

    discharge_Energy_Safe_Mode_average.append(P_average[i] - Energy_Safe_Mode_average[i])
    discharge_Energy_Safe_Mode_peak.append(P_average[i] - Energy_Safe_Mode_peak[i])




    Energy_Nominal_Mode_average.append(timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit + (OBC + EPS + ADCS + GPS + PAN) / 60 * T_Period_of_flight_for_every[i])
    Energy_Nominal_Mode_peak.append(timer * W_rasp_peak / 60 + Energy_to_Camera + energy_transmit + (OBC_peak + EPS_peak + ADCS_peak + GPS_peak + PAN_peak) / 60 * T_Period_of_flight_for_every[i])


    discharge_Energy_Nominal_Mode_average.append(P_average[i] - Energy_Nominal_Mode_average[i])
    discharge_Energy_Nominal_Mode_peak.append(P_average[i] - Energy_Nominal_Mode_peak[i])
    #print((OCS + EPS + OBC + ADCS) / 60 * T_Period_of_flight_for_every[i])

    discharge_per_cycle_only_flight.append(P_average[i] - (OCS + EPS + OBC + ADCS + GPS + ISL + PAN) / 60 * T_Period_of_flight_for_every[i])
    i += 1


#print(len(T_Period_of_flight))

#print("Height", "Emergency", "Safe", "Nominal")

#i = 0
#while i < len(P_average):
    #print(f"{i + 150:.4f} {T_Period_of_flight_for_every[i]:.4f} {T_Sunny[i]:.4f} {P_average[i]:.4f}")
    #print(f"{i + 150:.4f} {discharge_Energy_per_rasp_peak[i]:.4f} {discharge_Energy_Safe_Mode_peak[i]:.4f} {discharge_Energy_Nominal_Mode_peak[i]:.4f}")
    #print(i + P_average)
    #i = i + 100


#print(len(P_average))

#print(P_average[1849], 2000)

#print(2000, T_Period_of_flight_for_every[1849], T_Sunny[1849], P_average[1849])
#print(f"{2000:.4f} {discharge_Energy_per_rasp_peak[1849]:.4f} {discharge_Energy_Safe_Mode_peak[1849]:.4f} {discharge_Energy_Nominal_Mode_peak[1849]:.4f}")



#discharge_peak_nominal = math.ceil(discharge_Energy_Nominal_Mode_peak / discharge_Energy_Safe_Mode_peak)
#discharge_average_nominal = math.ceil(discharge_Energy_Nominal_Mode_average / discharge_Energy_Safe_Mode_average)

#discharge_peak_all = math.ceil(discharge_Energy_per_rasp_peak / discharge_Energy_Safe_Mode_peak)
#discharge_average_all = math.ceil(discharge_Energy_per_rasp_average / discharge_Energy_Safe_Mode_average)

#print=discharge_peak_all

variables = {
    #'discharge_Energy_per_rasp_average': discharge_Energy_per_rasp_average,
    #'discharge_Energy_Nominal_Mode_average': discharge_Energy_Nominal_Mode_average,
    #'discharge_Energy_per_rasp_peak': discharge_Energy_per_rasp_peak,
    #'discharge_Energy_Nominal_Mode_peak': discharge_Energy_Nominal_Mode_peak,
    #'Energy_per_rasp_average': Energy_per_rasp_average,
    #'Energy_Nominal_Mode_average': Energy_Nominal_Mode_average,
    #'Energy_per_rasp_peak': Energy_per_rasp_peak,
    #'Energy_Nominal_Mode_peak': Energy_Nominal_Mode_peak,
    'Discharge for nominal average mode': discharge_Energy_Nominal_Mode_average,
    'Discharge for nominal peak mode': discharge_Energy_Nominal_Mode_peak,
    'Discharge for all average mode': discharge_Energy_per_rasp_average,
    'Discharge for all peak mode': discharge_Energy_per_rasp_peak
}

# Finding the first index where the value is >= 0
for name, values in variables.items():
    found = False
    for idx, value in enumerate(values):
        if value >= 0:
            #print(f"First index where {name} >= 0: Height_under_the_Earth = {Height_under_the_Earth[idx]}")
            #print(P_average + Height_under_the_Earth)
            found = True
            break
    if not found:
        print(f"No positive values for {name}")



# Verify lengths of lists before plotting
#print("Length of h:", len(h))
#print("Length of Energy_per_rasp:", len(Energy_per_rasp))
#print("Length of Weight_of_image:", len(Weight_of_image))
#print("Length of Time_to_compute:", len(Time_to_compute))
#print("Length of discharge_per_cycle:", len(discharge_per_cycle))
#print(discharge_per_cycle_only_flight)
#print(P_average)


plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Time_to_transmit_image, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Height of satellites in km')
plt.ylabel('Time to transmit in hours')
plt.title('Dependence of image transmission time via UHF channel on height of satellite')
plt.legend()
plt.grid(True)
plt.show()



#plt.figure(figsize=(10, 6))
#plt.plot(Height_under_the_Earth, Energy_per_rasp_average, linestyle='-', color='b', label='Everything working average')

#plt.plot(Height_under_the_Earth, Energy_Safe_Mode_average, linestyle='--', color='r', label='Safe mode average')

#plt.plot(Height_under_the_Earth, Energy_Nominal_Mode_average, linestyle='--', color='y', label='Nominal mode average')


#plt.xlabel('Altitude (Kilometers)')
#plt.ylabel('Energy per satellite')
#plt.title('Energy Comparison')
#plt.legend()
#plt.grid(True)

#plt.show()

#==============


#=============

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_per_rasp_average, linestyle='-', color='b', label='Everything working average')

plt.plot(Height_under_the_Earth, Energy_Safe_Mode_average, linestyle='--', color='r', label='Safe mode average')

plt.plot(Height_under_the_Earth, Energy_Nominal_Mode_average, linestyle='--', color='y', label='Nominal mode average')


plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per satellite')
plt.title('Power Comparison for average mode')
plt.legend()
plt.grid(True)

plt.show()

#==============


plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_per_rasp_peak, linestyle='-', color='b', label='Everything working peak')

plt.plot(Height_under_the_Earth, Energy_Safe_Mode_peak, linestyle='--', color='r', label='Safe mode peak')

plt.plot(Height_under_the_Earth, Energy_Nominal_Mode_peak, linestyle='--', color='y', label='Nominal mode peak')


plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per satellite')
plt.title('Power Comparison for average mode for peak mode')
plt.legend()
plt.grid(True)

plt.show()

#==============

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, discharge_Energy_per_rasp_average, linestyle='-', color='b', label='Discharge Everything working average')

plt.plot(Height_under_the_Earth, discharge_Energy_Safe_Mode_average, linestyle='--', color='r', label='Discharge Safe mode average')

plt.plot(Height_under_the_Earth, discharge_Energy_Nominal_Mode_average, linestyle='--', color='y', label='Discharge Nominal mode average')


plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per satellite')
plt.title('Discharge Comparison average mode')
plt.legend()
plt.grid(True)

plt.show()

#==============


plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, discharge_Energy_per_rasp_peak, linestyle='-', color='b', label='Discharge Everything working peak')

plt.plot(Height_under_the_Earth, discharge_Energy_Safe_Mode_peak, linestyle='--', color='r', label='Discharge Safe mode peak')

plt.plot(Height_under_the_Earth, discharge_Energy_Nominal_Mode_peak, linestyle='--', color='y', label='Discharge Nominal mode peak')


plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per satellite')
plt.title('Discharge Comparison peak mode')
plt.legend()
plt.grid(True)

plt.show()

#==============


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_per_rasp_average, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Raspberry PI')
plt.title('Energy per Satellite with NN model all is on, average')
plt.legend()
plt.grid(True)
plt.show()
#===============================

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_per_rasp_peak, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Raspberry PI')
plt.title('Energy per Satellite with NN model all is on, peak')
plt.legend()
plt.grid(True)
plt.show()

#===============================

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_Safe_Mode_average, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Raspberry PI')
plt.title('Energy per Satellite with NN model safe mode is on, average')
plt.legend()
plt.grid(True)
plt.show()

#===============================

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_Safe_Mode_peak, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Raspberry PI')
plt.title('Energy per Satellite with NN model safe mode all is on, peak')
plt.legend()
plt.grid(True)
plt.show()

#===============================

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_Nominal_Mode_average, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Raspberry PI')
plt.title('Energy per Satellite with NN model nominal mode all is on, average')
plt.legend()
plt.grid(True)
plt.show()

#===============================

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_Nominal_Mode_peak, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Raspberry PI')
plt.title('Energy per Satellite with NN model nominal mode all is on, peak')
plt.legend()
plt.grid(True)
plt.show()




#==============================

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_without_cameras, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Satellite without Raspberry and camera')
plt.title('Energy Only flight')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_only_photos, linestyle='-', color='b', label='Energy per Raspberry PI')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Satellite only with Raspberry PI and camera')
plt.title('Energy Only Raspberry PI and camera')
plt.legend()
plt.grid(True)
#plt.gca().invert_xaxis()
plt.show()

#++++++
plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Energy_without_cameras, linestyle='-', color='b', label='Energy per satellite without Raspberry PI and camera')
#plt.gca().invert_yaxis()  # Инвертировать ось Y

plt.plot(Height_under_the_Earth, Energy_only_photos, linestyle='--', color='r', label='Energy per Satellite only with Raspberry PI and camera')
#plt.gca().invert_yaxis()  # Инвертировать ось Y

plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Energy per Raspberry PI')
plt.title('Consideration of the dependence of power generation on solar panels and power consumed by the satellite')
plt.legend()
plt.grid(True)

# Инвертировать ось X, если нужно
#plt.gca().invert_xaxis()

plt.show()
#++++++

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Weight_of_image, linestyle='-', color='b', label='Weight of Image')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Weight of Image (GB)')
plt.title('Weight of Image')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, Time_to_compute, linestyle='-', color='b', label='Time to Compute')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Time to Compute (minutes)')
plt.title('Time to Compute')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, discharge_per_cycle, linestyle='-', color='b', label='Discharge per Cycle')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Discharge per Cycle (W)')
plt.title('Discharge per Cycle')
plt.legend()
plt.grid(True)
plt.show()



plt.figure(figsize=(10, 6))
plt.plot(Height_under_the_Earth, discharge_per_cycle_only_flight, linestyle='-', color='b', label='Discharge per Cycle')
plt.xlabel('Altitude (Kilometers)')
plt.ylabel('Discharge per Cycle (W)')
plt.title('Charge per Cycle only flight')
plt.legend()
plt.grid(True)
plt.show()

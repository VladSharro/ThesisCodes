import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog

# Constants (initial default values)
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

V_mp_default = 2.4
I_mp_default = 0.5
Diag_Germany_default = math.sqrt(876 * 876 + 640 * 640)
N_c_default = 7
Eff_default = 0.8
P_diodess_less_default = 0.45
G_default = 398600.5
G_coef = 6.67430e-2
M_earth = 5.972e24
r_default = 6378.14
W_rasp_peak_default = 10
W_rasp_av_default = 8
Camera_Energy_default = 5.5  # W/h
S_Germany = 876 * 640
Pixels_based_nominal = 4096 #possible to change

Length_based = 19.6 #possible to change
Height_based = 500 #possible to change

S_band_trasmit = 17000 / 1000
S_band_receive = 1830 / 1000
S_band_trasmit_receive = 18830 / 1000
UHF_receive = 138 / 1000
UHF_transmit = 6112 / 1000


bait = 28
coef_for_clasters = (735 / 200)
claster_info_one_string = 34 / 1024 / 1024

Coef_number_clasters = 91.36 / (1024 * 676)
Coef_claster_time = 676 / 11.25 #6.28, 94.19


v_information_S_band = 0.5 # Мбайт/сек, 4 Мбит/сек
v_information_UHF_band = 0.125 # Мбайт/сек, 1Мбит/сек




def calculate_graph_data():
    i = 0

    # Retrieve variables from entry fields
    V_mp = float(v_mp_entry.get())
    I_mp = float(i_mp_entry.get())
    Diag_Germany = float(diag_entry.get())
    N_c = int(n_c_entry.get())
    Eff = float(eff_entry.get())
    P_diodess_less = float(diode_entry.get())
    G = float(g_entry.get())
    r = float(r_entry.get())
    W_rasp_peak = float(w_rasp_peak_entry.get())
    W_rasp_av = float(w_rasp_av_entry.get())
    Camera_Energy = float(camera_energy_entry.get())
    #print(Camera_Energy)
    Length_b = float(Length_ba.get())
    Height_b = float(Height_ba.get())

    S_band_t = float(S_band_tr.get())
    S_band_r = float(S_band_re.get())
    S_band_tra = float(S_band_trasmit_re.get())
    UHF_r = float(UHF_re.get())
    UHF_t = float(UHF_tr.get())

    Pixels_based = float(Pixels_input.get())

    v_information_S = float(v_information_S_ba.get())
    v_information_UHF = float(v_information_UHF_ba.get())



    K_based = Length_b / Height_b

    # Recalculate derived constants
    P_mp = V_mp * I_mp
    P_u3 = P_mp * N_c
    P_solar_battery = P_u3 * Eff - P_diodess_less

    #print(P_solar_battery)

    # Calculate data for plotting
    h_values = [i for i in range(150, 2000)]
    Height_under_the_Earth = []
    T_Period_of_flight_for_every = []
    T_Sunny = []
    P_average = []
    P_peak = []
    Camera_operation_time = []
    Weight_of_image = []
    Time_to_compute = []
    Time_under_Germany = []

    Energy_per_rasp_average = []
    discharge_Energy_per_rasp_average = []
    Energy_per_rasp_peak = []
    discharge_Energy_per_rasp_peak = []

    Energy_Safe_Mode_average = []
    discharge_Energy_Safe_Mode_average = []
    Energy_Safe_Mode_peak = []
    discharge_Energy_Safe_Mode_peak = []

    Energy_Nominal_Mode_average = []
    discharge_Energy_Nominal_Mode_average = []
    Energy_Nominal_Mode_peak = []
    discharge_Energy_Nominal_Mode_peak = []

    Energy_server_satellite_average = []
    Energy_server_satellite_peak = []
    Energy_photo_with_server_average = []
    Energy_photo_with_server_peak = []






    Energy_without_cameras = []
    Energy_only_photos = []

    discharge_per_cycle = []

    discharge_per_cycle_only_flight = []

    energy_to_transmit_image = []

    for height in h_values:
        Speed_of_satellites = np.sqrt(G_coef * M_earth / (height + r_default)) / 1000000000

        #print(Speed_of_satellites)
        Time_under_Germany.append(Diag_Germany / Speed_of_satellites / 60)
        #print(Camera_Energy)
        Energy_to_Camera = Camera_Energy / 60 * Time_under_Germany[i]

        #print(Energy_to_Camera)

        pixels = height * K_based
        square = pixels / Pixels_based
        height_pix = math.ceil(Diag_Germany / square)
        weight = Pixels_based * height_pix * bait / 1024 / 1024 / 1024
        Weight_of_image.append(weight)
        timer = weight / (Coef_number_clasters * Coef_claster_time) / 60
        timer_transmit = weight / Coef_claster_time / 60
        Time_to_compute.append(timer)

        energy_transmit_UHF = (weight / Coef_claster_time) * (claster_info_one_string / v_information_UHF) * (
            UHF_transmit) / 60 / 60

        energy_transmit_S_Band = (weight / Coef_claster_time) * (
                                      claster_info_one_string / v_information_S) * (S_band_t) / 60 / 60


        energy_to_transmit_image.append(energy_transmit_S_Band)

        Height_under_the_Earth.append(height)
        T_Period_of_flight = 2 * math.pi * np.sqrt(pow(height + r_default, 3) / G) / 60
        T_Period_of_flight_for_every.append(T_Period_of_flight)
        T_Sunny_period = T_Period_of_flight * (1 - math.asin(r_default / (height + r_default)) / math.pi)
        print(T_Sunny_period)
        T_Sunny.append(T_Sunny_period)
        P_avg = P_solar_battery * T_Sunny_period / 60
        P_average.append(P_avg)
        #print(height, P_avg)
        #P_peak.append(P_solar_battery)
        Camera_operation_time.append(P_avg - Camera_Energy)

        Energy_per_rasp_average.append(timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit_S_Band + (
                    OCS + EPS + OBC + ADCS + GPS + ISL + PAN) / 60 * T_Period_of_flight_for_every[i])
        Energy_per_rasp_peak.append(timer * W_rasp_peak / 60 + Energy_to_Camera + energy_transmit_S_Band + (
                    OCS_peak + EPS_peak + OBC_peak + ADCS_peak + GPS_peak + ISL_peak + PAN_peak) / 60 *
                                    T_Period_of_flight_for_every[i])

        #print(Energy_to_Camera)

        #print(Energy_per_rasp_peak)

        discharge_Energy_per_rasp_average.append(P_avg - Energy_per_rasp_average[i])
        discharge_Energy_per_rasp_peak.append(P_avg - Energy_per_rasp_peak[i])

        Energy_without_cameras.append((OCS + EPS + OBC + ADCS + GPS + ISL + PAN) / 60 * T_Period_of_flight_for_every[i])
        Energy_only_photos.append(timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit_S_Band)
        discharge = P_average[i] - (
                    timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit_S_Band + (OCS + EPS + OBC + ADCS) / 60 *
                    T_Period_of_flight_for_every[i])
        discharge_per_cycle.append(discharge)

        Energy_Safe_Mode_average.append((OBC + EPS + PAN) / 60 * T_Period_of_flight_for_every[i]) #OBC + EPS + PAN
        Energy_Safe_Mode_peak.append((OBC_peak + EPS_peak + PAN_peak) / 60 * T_Period_of_flight_for_every[i]) #OBC_peak + EPS_peak + PAN_peak

        discharge_Energy_Safe_Mode_average.append(P_average[i] - Energy_Safe_Mode_average[i])
        discharge_Energy_Safe_Mode_peak.append(P_average[i] - Energy_Safe_Mode_peak[i])

        Energy_Nominal_Mode_average.append(
            timer * W_rasp_av / 60 + Energy_to_Camera + energy_transmit_S_Band + (OBC + EPS + ADCS + GPS + PAN) / 60 *
            T_Period_of_flight_for_every[i])
        Energy_Nominal_Mode_peak.append(timer * W_rasp_peak / 60 + Energy_to_Camera + energy_transmit_S_Band + (
                    OBC_peak + EPS_peak + ADCS_peak + GPS_peak + PAN_peak) / 60 * T_Period_of_flight_for_every[i])

        discharge_Energy_Nominal_Mode_average.append(P_average[i] - Energy_Nominal_Mode_average[i])
        discharge_Energy_Nominal_Mode_peak.append(P_average[i] - Energy_Nominal_Mode_peak[i])
        # print((OCS + EPS + OBC + ADCS) / 60 * T_Period_of_flight_for_every[i])

        discharge_per_cycle_only_flight.append(
            P_average[i] - (OCS + EPS + OBC + ADCS + GPS + ISL + PAN) / 60 * T_Period_of_flight_for_every[i])
        i += 1

    return h_values, P_average, Camera_operation_time, T_Period_of_flight_for_every, Energy_per_rasp_average, Energy_Safe_Mode_average, Energy_Nominal_Mode_average, Energy_per_rasp_peak, Energy_Safe_Mode_peak, Energy_Nominal_Mode_peak, discharge_Energy_per_rasp_average, discharge_Energy_Safe_Mode_average, discharge_Energy_Nominal_Mode_average, discharge_Energy_per_rasp_peak, discharge_Energy_Safe_Mode_peak, discharge_Energy_Nominal_Mode_peak




def plot_graph(graph_type):
    h_values, P_average, Camera_operation_time, T_Period_of_flight_for_every, Energy_per_rasp_average, Energy_Safe_Mode_average, Energy_Nominal_Mode_average, Energy_per_rasp_peak, Energy_Safe_Mode_peak, Energy_Nominal_Mode_peak, discharge_Energy_per_rasp_average, discharge_Energy_Safe_Mode_average, discharge_Energy_Nominal_Mode_average, discharge_Energy_per_rasp_peak, discharge_Energy_Safe_Mode_peak, discharge_Energy_Nominal_Mode_peak = calculate_graph_data()

    # Clear the current figure
    fig.clear()

    if graph_type == "Average Power":
        ax = fig.add_subplot(111)
        ax.plot(h_values, P_average, color='b', label='Average Power')
        #print(len(P_average))
        #print(P_average[])
        #i = 0
        #while i < len(P_average):
        #    print(i, P_average[i])
        #    i = i + 1


        ax.set_title('Average Power vs Altitude')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Average Power (W)')
        ax.legend()


    elif graph_type == "Camera Operation Time":
        ax = fig.add_subplot(111)
        ax.plot(h_values, Camera_operation_time, color='g', label='Camera Operation Time')
        ax.set_title('Camera Operation Time vs Altitude')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Camera Operation Time (hours)')
        ax.legend()


    elif graph_type == "Orbit Period":
        ax = fig.add_subplot(111)
        ax.plot(h_values, T_Period_of_flight_for_every, color='m', label='Orbit Period')
        ax.set_title('Orbit Period vs Altitude')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Orbit Period (minutes)')
        ax.legend()


    elif graph_type == "Energy Average":
        ax = fig.add_subplot(111)
        ax.plot(h_values, Energy_per_rasp_average, linestyle='-', color='b', label='Everything working average')
        ax.plot(h_values, Energy_Safe_Mode_average, linestyle='--', color='r', label='Safe mode average')
        ax.plot(h_values, Energy_Nominal_Mode_average, linestyle='--', color='y', label='Nominal mode average')
        ax.set_title('Energy Consumption vs Altitude (Average)')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Energy (W)')
        ax.legend()


    elif graph_type == "Energy Average":
        ax = fig.add_subplot(111)
        ax.plot(h_values, Energy_per_rasp_average, linestyle='-', color='b', label='Everything working average')
        ax.plot(h_values, Energy_Safe_Mode_average, linestyle='--', color='r', label='Safe mode average')
        ax.plot(h_values, Energy_Nominal_Mode_average, linestyle='--', color='y', label='Nominal mode average')
        ax.set_title('Energy Consumption vs Altitude (Peak)')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Energy (W)')
        ax.legend()



    elif graph_type == "Energy Peak":
        ax = fig.add_subplot(111)
        ax.plot(h_values, Energy_per_rasp_peak, linestyle='-', color='b', label='Everything working peak')
        ax.plot(h_values, Energy_Safe_Mode_peak, linestyle='--', color='r', label='Safe mode peak')
        ax.plot(h_values, Energy_Nominal_Mode_peak, linestyle='--', color='y', label='Nominal mode peak')
        ax.set_title('Energy Consumption vs Altitude (Peak)')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Energy (W)')
        ax.legend()


    elif graph_type == "Discharge Average":
        ax = fig.add_subplot(111)
        ax.plot(h_values, discharge_Energy_per_rasp_average, linestyle='-', color='b', label='Everything working average')
        ax.plot(h_values, discharge_Energy_Safe_Mode_average, linestyle='--', color='r', label='Safe mode average')
        ax.plot(h_values, discharge_Energy_Nominal_Mode_average, linestyle='--', color='y', label='Nominal mode average')
        ax.set_title('Discharge Energy Consumption vs Altitude (Average)')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Energy (W)')
        ax.legend()


    elif graph_type == "Discharge Peak":
        ax = fig.add_subplot(111)
        ax.plot(h_values, discharge_Energy_per_rasp_peak, linestyle='-', color='b', label='Everything working peak')
        ax.plot(h_values, discharge_Energy_Safe_Mode_peak, linestyle='--', color='r', label='Safe mode peak')
        ax.plot(h_values, discharge_Energy_Nominal_Mode_peak, linestyle='--', color='y', label='Nominal mode peak')
        ax.set_title('Discharge Energy Consumption vs Altitude (Peak)')
        ax.set_xlabel('Altitude (km)')
        ax.set_ylabel('Energy (W)')
        ax.legend()

    # Make sure to redraw the figure
    fig.canvas.draw()


def save_graph():
    # Open a file dialog for saving the figure
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
    if file_path:
        fig.savefig(file_path)
        print(f"Graph saved as {file_path}")

# Setting up the Tkinter window
root = tk.Tk()
root.title("Satellite Energy Simulation")

# Set up the figure for matplotlib
fig = plt.Figure(figsize=(8, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=16)

# Create input fields for variables
ttk.Label(root, text="V_mp (V):").grid(row=0, column=0)
v_mp_entry = ttk.Entry(root)
v_mp_entry.insert(0, V_mp_default)
v_mp_entry.grid(row=0, column=1)

ttk.Label(root, text="I_mp (A):").grid(row=1, column=0)
i_mp_entry = ttk.Entry(root)
i_mp_entry.insert(0, I_mp_default)
i_mp_entry.grid(row=1, column=1)

ttk.Label(root, text="Diagonal Germany (km):").grid(row=2, column=0)
diag_entry = ttk.Entry(root)
diag_entry.insert(0, Diag_Germany_default)
diag_entry.grid(row=2, column=1)

ttk.Label(root, text="N_c:").grid(row=3, column=0)
n_c_entry = ttk.Entry(root)
n_c_entry.insert(0, N_c_default)
n_c_entry.grid(row=3, column=1)

ttk.Label(root, text="Efficiency:").grid(row=4, column=0)
eff_entry = ttk.Entry(root)
eff_entry.insert(0, Eff_default)
eff_entry.grid(row=4, column=1)

ttk.Label(root, text="P_diodess_less (W):").grid(row=5, column=0)
diode_entry = ttk.Entry(root)
diode_entry.insert(0, P_diodess_less_default)
diode_entry.grid(row=5, column=1)

ttk.Label(root, text="G (km^3/s^2):").grid(row=6, column=0)
g_entry = ttk.Entry(root)
g_entry.insert(0, G_default)
g_entry.grid(row=6, column=1)

ttk.Label(root, text="Radius of Earth (km):").grid(row=7, column=0)
r_entry = ttk.Entry(root)
r_entry.insert(0, r_default)
r_entry.grid(row=7, column=1)

ttk.Label(root, text="W_rasp_peak (W):").grid(row=8, column=0)
w_rasp_peak_entry = ttk.Entry(root)
w_rasp_peak_entry.insert(0, W_rasp_peak_default)
w_rasp_peak_entry.grid(row=8, column=1)

ttk.Label(root, text="W_rasp_av (W):").grid(row=9, column=0)
w_rasp_av_entry = ttk.Entry(root)
w_rasp_av_entry.insert(0, W_rasp_av_default)
w_rasp_av_entry.grid(row=9, column=1)

ttk.Label(root, text="Camera Energy (W/h):").grid(row=10, column=0)
camera_energy_entry = ttk.Entry(root)
camera_energy_entry.insert(0, Camera_Energy_default)
camera_energy_entry.grid(row=10, column=1)
#---
ttk.Label(root, text="Length_based:").grid(row=11, column=0)
Length_ba = ttk.Entry(root)
Length_ba.insert(0, Length_based)
Length_ba.grid(row=11, column=1)

ttk.Label(root, text="Height_based:").grid(row=12, column=0)
Height_ba = ttk.Entry(root)
Height_ba.insert(0, Height_based)
Height_ba.grid(row=12, column=1)

ttk.Label(root, text="S_band_trasmit:").grid(row=13, column=0)
S_band_tr = ttk.Entry(root)
S_band_tr.insert(0, S_band_trasmit)
S_band_tr.grid(row=13, column=1)

ttk.Label(root, text="S_band_receive:").grid(row=14, column=0)
S_band_re = ttk.Entry(root)
S_band_re.insert(0, S_band_receive)
S_band_re.grid(row=14, column=1)

ttk.Label(root, text="S_band_trasmit_receive:").grid(row=15, column=0)
S_band_trasmit_re = ttk.Entry(root)
S_band_trasmit_re.insert(0, S_band_trasmit_receive)
S_band_trasmit_re.grid(row=15, column=1)

ttk.Label(root, text="UHF_receive:").grid(row=16, column=0)
UHF_re = ttk.Entry(root)
UHF_re.insert(0, UHF_receive)
UHF_re.grid(row=16, column=1)

ttk.Label(root, text="UHF_transmit:").grid(row=17, column=0)
UHF_tr = ttk.Entry(root)
UHF_tr.insert(0, UHF_transmit)
UHF_tr.grid(row=17, column=1)

ttk.Label(root, text="v_information_S_band:").grid(row=18, column=0)
v_information_S_ba = ttk.Entry(root)
v_information_S_ba.insert(0, v_information_S_band)
v_information_S_ba.grid(row=18, column=1)

ttk.Label(root, text="v_information_UHF_band:").grid(row=19, column=0)
v_information_UHF_ba = ttk.Entry(root)
v_information_UHF_ba.insert(0, v_information_UHF_band)
v_information_UHF_ba.grid(row=19, column=1)


ttk.Label(root, text="Pixels:").grid(row=20, column=0)
Pixels_input = ttk.Entry(root)
Pixels_input.insert(0, Pixels_based_nominal)
Pixels_input.grid(row=20, column=1)
#----

# Create buttons for graph selection
average_power_button = ttk.Button(root, text="Average Power", command=lambda: plot_graph("Average Power"))
average_power_button.grid(row=21, column=0, columnspan=2)

peak_power_button = ttk.Button(root, text="Energy Average", command=lambda: plot_graph("Energy Average"))
peak_power_button.grid(row=22, column=0, columnspan=2)

camera_time_button = ttk.Button(root, text="Camera Operation Time", command=lambda: plot_graph("Camera Operation Time"))
camera_time_button.grid(row=23, column=0, columnspan=2)

orbit_period_button = ttk.Button(root, text="Orbit Period", command=lambda: plot_graph("Orbit Period"))
orbit_period_button.grid(row=21, column=1, columnspan=2)

average_power_button = ttk.Button(root, text="Energy Peak Photo Sat", command=lambda: plot_graph("Energy Peak"))
average_power_button.grid(row=25, column=0, columnspan=2)

average_power_button = ttk.Button(root, text="Energy Average Photo Sat", command=lambda: plot_graph("Energy Average"))
average_power_button.grid(row=24, column=0, columnspan=2)

average_power_button = ttk.Button(root, text="Discharge Average Photo Sat", command=lambda: plot_graph("Discharge Average"))
average_power_button.grid(row=24, column=1, columnspan=2)

average_power_button = ttk.Button(root, text="Discharge Peak Photo Sat", command=lambda: plot_graph("Discharge Peak"))
average_power_button.grid(row=25, column=1, columnspan=2)

# Create a save button
save_button = ttk.Button(root, text="Save Graph", command=save_graph)
save_button.grid(row=22, column=1, columnspan=2)

root.mainloop()

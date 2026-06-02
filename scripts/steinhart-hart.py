import pandas as pd
import plotly.express as px
import numpy as np

from scripts.lib import mymath
from scripts.lib.mymath import Number, c_to_kelvin

def plot_resistance(T_values: list[Number], ADC_values: list[Number], r_fixed: int):
    C = mymath.calc_C_steinhart_hart(T_values, ADC_values, r_fixed)
    B = mymath.calc_B_steinhart_hart(C, T_values, ADC_values, r_fixed)
    A = mymath.calc_A_steinhart_hart(B, C, T_values, ADC_values, r_fixed)
    # A = -0.010105530969460576
    # B = 0.0018846914061233005
    # C = -0.000005041558483186885
    rs = np.geomspace(2000,20000, 20)
    ts = [mymath.calc_steinhart_hart(r, A,B,C) for r in rs]
    tcs = [mymath.kelvin_to_c(k) for k in ts]
    fig = px.line(x=tcs, y=rs, title=f"ADC ({r_fixed/1000}kΩ fixed resistor)",labels={'x': 'Temperature (℃)', 'y': 'Resistance'}, markers=True)
    fig.update_layout(font_size=18)
    fig.show()

def plot_ADC(T_values: list[Number], ADC_values: list[Number], r_fixed: int):
    C = mymath.calc_C_steinhart_hart(T_values, ADC_values, r_fixed)
    B = mymath.calc_B_steinhart_hart(C, T_values, ADC_values, r_fixed)
    A = mymath.calc_A_steinhart_hart(B, C, T_values, ADC_values, r_fixed)
    # A = -0.010105530969460576
    # B = 0.0018846914061233005
    # C = -0.000005041558483186885
    tcs = range(0,150,5)
    ts = [c_to_kelvin(c) for c in tcs]
    rs = [mymath.calc_steinhart_hart_inverse_analytical(t, A, B, C) for t in tcs]
    y = [mymath.calc_ADCtherm_voltage_divider(r, r_fixed) for r in rs]
    fig = px.line(x=tcs, y=y, title=f"ADC ({r_fixed/1000}kΩ fixed resistor)",labels={'x': 'Temperature (℃)', 'y': 'ADC'}, markers=True)
    fig.update_layout(font_size=18)
    fig.show()


if __name__ == '__main__':
    df_20k = pd.DataFrame({
        'Temperatures': [21.5, 54.6, 89.6],
        'ADC': [1500, 985, 757]
    })
    df_47k = pd.DataFrame({
        'Temperatures': [21.5, 54.8, 90.3],
        'ADC': [953, 568, 402]
    })
    df_100k = pd.DataFrame({
        'Temperatures': [21.5, 55.1, 90],
        'ADC': [612, 323, 192]
    })

    #plot_resistance([c_to_kelvin(t) for t in df_20k['Temperatures']], df_20k['ADC'], 20000)
    #plot_ADC([c_to_kelvin(t) for t in df_47k['Temperatures']], df_47k['ADC'], 47000)
    
    coeffs = np.polyfit([21.5, 54.6, 89.6], [1500, 985, 757], deg=3)
    poly = np.poly1d(coeffs)
# print(f'Reading {ADC_52_POINT_6_DEG_100k}')
# with open(ADC_52_POINT_6_DEG_100k, 'r', encoding='utf-8') as f:
#     data = f.readlines()
#     y = [int(d) for d in data]
#     avg = round(average(y), 0)
#     x = [s * 0.5 for s in range(0, len(y))]
#     fig = px.line(y=y, x=x, title="52.6°C ADC readings (100kΩ resistor)",
#                   labels={'x': 'Time (s)', 'y': 'ADC value (0 to 4095)'}, markers=True)
#     fig.add_hline(y=avg, line_dash="dash", line_color="red", annotation_text=f"Average = {avg}")
#     fig.update_layout(font_size=18)
#     fig.show()

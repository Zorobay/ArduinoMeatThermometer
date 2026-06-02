import click
import numpy as np
import pyqtgraph as pg
import pandas as pd
import plotly.express as px


@click.command()
@click.argument('filename', type=click.File('r'))
def run(filename: str):
    df = pd.read_csv(filename, sep=';')
    temp_rows = df[df['Temp'].notna()]
    
    data = {}
    for i, row in temp_rows.iterrows():
        temp = row['Temp']
        window = df.loc[i-4:i+4, 'ADC']
        data[temp] = window.mean()
        
    adcs = []
    temps = []
    for t,a in data.items():
        temps.append(t)
        adcs.append(a)
        
    coeffs = np.polyfit(temps, adcs, deg=4)
    poly = np.poly1d(coeffs)
    
    xs = np.linspace(0, 140, 100)
    ys = poly(xs)
    fig = px.line(x=xs, y=ys, labels={'x': 'Temperature', 'y': 'ADC'})
    
    # Add calibration points as a scatter trace
    fig.add_scatter(x=temps, y=adcs, mode='markers',
                    marker=dict(size=8, color='red'),
                    name='Calibration points')
    fig.show()
        
if __name__ == '__main__':
    run()
from typing import Sequence

import click
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def polynomial_pretty_str(coeffs: Sequence[float], deg: int) -> str:
    def var(i: int) -> str:
        if i < deg -1:
            return f'x^{deg-i}'
        elif i < deg:
            return 'x'
        return ''
    parts = [f'{c:.2f}{var(i)}' for i, c in enumerate(coeffs)]
    return ' + '.join(parts)
    
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
        
    deg = 3
    coeffs = np.polyfit(temps, adcs, deg=deg)
    poly = np.poly1d(coeffs)
    poly_str = polynomial_pretty_str(coeffs, deg)
    
    xs = np.linspace(0, 140, 100)
    ys = poly(xs)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = xs, y = ys, name = f'${poly_str}$'))
    
    # Add calibration points as a scatter trace
    fig.add_scatter(x=temps, y=adcs, mode='markers',
                    marker=dict(size=8, color='red'),
                    name='Calibration points')
    
    fig.update_layout(title=f'Polyfit of degree {deg}', xaxis_title= 'Temperature ℃', yaxis_title= 'ADC value')
    fig.show()
        
if __name__ == '__main__':
    run()
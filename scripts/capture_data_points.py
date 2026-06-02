import csv
import sys
import platform
from datetime import datetime

import pyqtgraph as pg
import serial
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton

def get_serial_port() -> serial.serialjava.Serial:
    name = 'COM3' if platform.system() == 'Windows' else '/dev/ttyUSB0'
    return serial.Serial(name, 115200, timeout=1)


def write_csv_data(data: dict[float, tuple[float, float]]):
    rows = []
    for x, tup in data.items():
        rows.append([x, tup[0], tup[1]])

    filename = datetime.now().isoformat().replace(':', '_') + '.csv'
    headings = ['Time', 'ADC', 'Temp']
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headings)
        writer.writerows(rows)
    print(f"Wrote output to {filename}")


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        layout.addLayout(bottom_layout)

        self.temp_button = QPushButton("Add Temperature")
        self.temp_input = QLineEdit()
        bottom_layout.addWidget(self.temp_input)
        bottom_layout.addWidget(self.temp_button)
        self.temp_button.clicked.connect(self._on_temperature_added)
        self.temp_input.returnPressed.connect(self._on_temperature_added)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self._on_stop_button_clicked)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._read_serial)
        self.update_timer.start(100)
        self.ser = get_serial_port()
        self.x = []
        self.y = []
        self.data = {}
        self.plot = self.plot_widget.plot(self.x, self.y, pen='y')

    def add_plot_point(self, y):
        self.y.append(y)
        if len(self.x) > 0:
            x = self.x[-1] + 0.5
        else:
            x = 0
        self.x.append(x)
        self.plot.setData(self.x, self.y)
        self.data[x] = (y, None)

    def add_temp_marker(self, temp: float):
        x = self.x[-1]
        line = pg.InfiniteLine(
            pos=x,
            angle=90,
            pen=pg.mkPen('r', width=2),
            label=f'{temp}℃',
        )
        self.plot_widget.addItem(line)
        if not self.data[x]:
            raise Exception(f"No data at x = {x}")

        y,_ = self.data[x]
        self.data[x] = y,temp

    def _read_serial(self):
        line = self.ser.readline().decode('utf-8').strip()
        if line and line.isnumeric():
            self.add_plot_point(int(line))

    def _on_temperature_added(self):
        temp_input = self.temp_input.text().strip()
        if temp_input:
            temp_input = temp_input.replace(',','.')
            temp_input = float(temp_input)
            self.add_temp_marker(temp_input)

    def _on_stop_button_clicked(self):
        print("Stopping...")
        print()
        print(f"Data points: {len(self.data)}")
        print()
        for x, tup in self.data.items():
            y = tup[0]
            temp = tup[1]
            print(f"x = {x}, y = {y}, temp = {temp}")

        self.update_timer.stop()
        write_csv_data(self.data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.resize(1200,600)
    central_widget = CentralWidget()
    window.setCentralWidget(central_widget)
    window.show()
    app.exec()

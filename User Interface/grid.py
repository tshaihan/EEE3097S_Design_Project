import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import signal_acquisition
import gcc_phat
import synchronization
import triangulation
import time_delay_estimation

c = 343

def plot_empty_grid():
    fig, ax = plt.subplots()
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True)
    return fig

def plot_point(fig, x, y):
    ax = fig.gca()
    ax.plot(x, y, marker='o', markersize=8, color='red', label='Sound source')
    ax.legend()
    return fig

def plot_calibration(fig):
    ax = fig.gca()
    ax.plot(0.4, 0.25, marker='*', markersize=8, color='green', label='Calibration Signal')
    ax.legend()
    return fig

def main():
    fig = plot_empty_grid()



    layout = [
        [sg.Text('X:', size=(5, 1)), sg.Text('0.23', size=(10, 1))],
        [sg.Text('Y:', size=(5, 1)), sg.Text('0.46', size=(10, 1))],
        [sg.Button('Plot'), sg.Button('Exit')],
        [sg.Canvas(key='canvas')],
    ]

    window = sg.Window('XY Grid Plotter', layout, resizable=True, finalize=True)

    canvas_elem = window['canvas']
    canvas = canvas_elem.Widget

    canvas_elem.Widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_elem.Widget.draw()
    canvas_elem.Widget.get_tk_widget().pack(side='top', fill='both', expand=1)
    fig = plot_calibration(fig)
    canvas_elem.Widget.draw()

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == 'Plot':
            try:
                x = 0.23
                y = 0.46
                
                # subprocess.run("bash main.sh", shell=True)
                
                signals,fs = signal_acquisition.acquire_signals(['recording_1.wav','recording_2.wav'])
                [[delay1, delay2, delay3, delay4], [sig1, sig2, sig3, sig4]] = synchronization.synchronize(signals[0],signals[3],signals[1],signals[2],signals[0][:int(6*fs)],fs)
                [tdoa12, tdoa13, tdoa14] = time_delay_estimation.tdoa(sig1, sig2, sig3, sig4)

                position = triangulation.triangulate([0,0],[0.8,0],[0,0.5],[0.8,0.5],abs(tdoa12*c/fs),abs(tdoa13*c/fs),abs(tdoa14*c/fs))

                x = position[0]
                y = position[1]


                if 0 <= x <= 0.8 and 0 <= y <= 0.5:
                    fig = plot_point(fig, x, y)
                    canvas_elem.Widget.draw()

                else:
                    sg.popup_error('Invalid input. X and Y values must be within the specified range.')

            except ValueError:
                sg.popup_error('Invalid input. Please enter valid numeric values for X and Y.')

    window.close()

if __name__ == '__main__':
    main()

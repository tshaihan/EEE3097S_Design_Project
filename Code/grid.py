import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import signal_acquisition
import gcc_phat
import synchronization
import triangulation
import time_delay_estimation
import numpy as np

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

def clear(fig):
    ax = fig.gca()
    ax.cla()
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True)

def generate_sync(a, b, t, fs):

    # Create subplots for the four graphs
    fig, axs = plt.subplots(4, 2, figsize=(10, 8))
    axs[0, 0].plot(t, a[0])
    tb1 = np.linspace(0, len(b[0]/fs), len(b[0]))
    axs[0, 1].plot(tb1, b[0])
    axs[1, 0].plot(t, a[1])
    tb2 = np.linspace(0, len(b[1]/fs), len(b[1]))
    axs[1, 1].plot(tb2, b[1])
    axs[2, 0].plot(t, a[2])
    tb3 = np.linspace(0, len(b[2]/fs), len(b[2]))
    axs[2, 1].plot(tb3, b[2])
    axs[3, 0].plot(t, a[3])
    tb4 = np.linspace(0, len(b[3]/fs), len(b[3]))
    axs[3, 1].plot(tb4, b[3])

    # Embed the graphs in a PySimpleGUI window
    layout = [
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('Close')]
    ]

    window = sg.Window('Graph Plots', layout, finalize=True)
    canvas_elem = window['-CANVAS-']
    canvas = FigureCanvasTkAgg(fig, canvas_elem.Widget)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Close':
            break

    window.close()

def main():
    fig = plot_empty_grid()

    layout = [
        [sg.Text('X:', size=(5, 1)), sg.Text(key='x_value', size=(10, 1))],
        [sg.Text('Y:', size=(5, 1)), sg.Text(key='y_value', size=(10, 1))],
        [sg.Button('Record')],
        [sg.Text(key='msg', size=(20, 1))],
        [sg.Button('Plot'), sg.Button('Exit')], [sg.Button('Reset')],
        [sg.Canvas(key='canvas')],
        [sg.Button('Synchronisation plots')]
    ]

    window = sg.Window('EEE3097S Design Project', layout, resizable=True, finalize=True, element_justification='center')

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
        elif event == 'Record':
            window['msg'].update(value='Signal is recording!')
            subprocess.run("bash main.sh", shell=True)
            window['msg'].update(value='Signal has been recorded!')
        elif event == 'Plot':
            try:

                signals,fs = signal_acquisition.acquire_signals(['recording_1.wav','recording_2.wav'])
                [[delay1, delay2, delay3, delay4], [sig1, sig2, sig3, sig4]] = synchronization.synchronize(signals[0],signals[1],signals[2],signals[3],signals[0][:int(6*fs)], 6, fs)
                [tdoa12, tdoa13, tdoa14] = time_delay_estimation.tdoa(sig1, sig2, sig3, sig4, fs)

                position = triangulation.triangulate([0,0],[0,0.5],[0.8,0.5],[0.8,0],tdoa12*c,tdoa13*c,tdoa14*c)

                x = position[0]
                y = position[1]

                window['x_value'].update(value=f'{x:.3f}')
                window['y_value'].update(value=f'{y:.3f}')

                a = [signals[0], signals[1], signals[2], signals[3]]
                b = [sig1, sig2, sig3, sig4]
                t = np.linspace(0, len(signals[0]/fs), len(signals[0]))

                if 0 <= x <= 0.8 and 0 <= y <= 0.5:
                    fig = plot_point(fig, x, y)
                    canvas_elem.Widget.draw()

                else:
                    sg.popup_error('Invalid input. X and Y values must be within the specified range.')

            except ValueError:
                 sg.popup_error('Invalid input. Please enter valid numeric values for X and Y.')
        elif event == 'Synchronisation plots':
            generate_sync(a, b, t, fs)
        elif event == 'Reset':
            clear(fig)
            canvas_elem.Widget.draw()
            fig = plot_calibration(fig)
            canvas_elem.Widget.draw()
    window.close()

if __name__ == '__main__':
    main()

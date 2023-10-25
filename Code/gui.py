import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_acquisition import acquire_signals
from time_delay_estimation import estimate_delays
from triangulation import triangulate


# Initialises the grid
def init_grid(fig):
    ax = fig.gca()
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.grid(True)
    ax.plot(0.4, 0.25, marker='s', markersize=8, color='red', label='Calibration Position')
    ax.legend()
    return fig


# Plots point on the grid
def plot_point(fig, x, y):
    ax = fig.gca()
    ax.plot(x, y, marker='o', markersize=8, label='Estimated Source Position')
    ax.legend()
    return fig


# Clears the grid
def reset_grid(fig):
    ax = fig.gca()
    ax.cla()
    init_grid(fig)
    return fig


# Creates plots of acquired audio signals
def signal_acquisition_plots(raw_signals, processed_signals, t):
    fig, ax = plt.subplots(4, 2)
    fig.suptitle('Raw and Processed Audio Signals Acquired')
    fig.supxlabel('Time (s)')
    fig.supylabel('Amplitude')
    ax[0, 0].set_title('Raw Signals')
    ax[0, 1].set_title('Processed Signals')
    for i in range(4):
        ax[i, 0].plot(t, raw_signals[i])
        ax[i, 0].set_ylabel('Mic {}'.format(i + 1))
        ax[i, 1].plot(t, processed_signals[i])
        ax[i, 1].set_ylabel('Mic {}'.format(i + 1))
    fig.tight_layout()

    # Embed the graphs in a PySimpleGUI window
    layout = [[sg.Canvas(key='-CANVAS-')], [sg.Button('Close')]]
    window = sg.Window('Signal Acquisition Plots', layout, resizable=True, finalize=True)
    canvas_elem = window['-CANVAS-']
    canvas = FigureCanvasTkAgg(fig, canvas_elem.Widget)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Close':
            break
    window.close()


# Creates plots of GCC-PHAT applied to the calibration signals
def synchronisation_plots(cross_correlations, lags):
    fig, ax = plt.subplots(4)
    fig.suptitle('GCC-PHAT of the Audio Signals with respect to the Calibration Signal from Mic 1')
    fig.supxlabel('Time Lags (s)')
    fig.supylabel('Amplitude')
    for i in range(4):
        ax[i].plot(lags, cross_correlations[i])
        ax[i].set_ylabel('Mic {}'.format(i + 1))
    fig.tight_layout()

    # Embed the graphs in a PySimpleGUI window
    layout = [[sg.Canvas(key='-CANVAS-')], [sg.Button('Close')]]
    window = sg.Window('Synchronisation Plots', layout, resizable=True, finalize=True)
    canvas_elem = window['-CANVAS-']
    canvas = FigureCanvasTkAgg(fig, canvas_elem.Widget)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Close':
            break
    window.close()


# Creates plots of GCC-PHAT applied to the source signals
def time_delay_estimation_plots(cross_correlations, lags):
    fig, ax = plt.subplots(4)
    fig.suptitle('GCC-PHAT of the Audio Signals with respect to the Source Signal from Mic 1')
    fig.supxlabel('Time Lags (s)')
    fig.supylabel('Amplitude')
    for i in range(4):
        ax[i].plot(lags, cross_correlations[i])
        ax[i].set_ylabel('Mic {}'.format(i + 1))
    fig.tight_layout()

    # Embed the graphs in a PySimpleGUI window
    layout = [[sg.Canvas(key='-CANVAS-')], [sg.Button('Close')]]
    window = sg.Window('Time Delay Estimation Plots', layout, resizable=True, finalize=True)
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
    # Creates the grid
    localisation = False
    fig, ax = plt.subplots()
    init_grid(fig)

    # Sets GUI layout
    layout = [
        [sg.Button('Start Localisation'), sg.Button('Reset Grid'), sg.Button('Exit')],
        [sg.Text(key='msg', size=(50, 1))],
        [sg.Text('Estimated Synchronisation Delays (ms):', size=(50, 1))],
        [sg.Text(key='sync1', size=(10, 1)), sg.Text(key='sync2', size=(10, 1)), sg.Text(key='sync3', size=(10, 1)),
         sg.Text(key='sync4', size=(10, 1))],
        [sg.Text('Estimated ToA Delays (ms):', size=(50, 1))],
        [sg.Text(key='toa1', size=(10, 1)), sg.Text(key='toa2', size=(10, 1)), sg.Text(key='toa3', size=(10, 1)),
         sg.Text(key='toa4', size=(10, 1))],
        [sg.Text('Estimated TDoA Values (ms):', size=(50, 1))],
        [sg.Text(key='tdoa12', size=(10, 1)), sg.Text(key='tdoa13', size=(10, 1)), sg.Text(key='tdoa14', size=(10, 1))],
        [sg.Text('Initial Source Position Estimate (m):', size=(50, 1))],
        [sg.Text(key='x0', size=(10, 1)), sg.Text(key='y0', size=(10, 1))],
        [sg.Text('Estimated Source Position (m):', size=(50, 1))],
        [sg.Text(key='x', size=(10, 1)), sg.Text(key='y', size=(10, 1))],
        [sg.Button('Signal Acquisition Plots'), sg.Button('Synchronisation Plots'),
         sg.Button('Time Delay Estimation Plots')],
        [sg.Canvas(key='canvas')]
    ]

    window = sg.Window('EEE3097S Design Project: Group 2', layout, resizable=True, finalize=True,
                       element_justification='center')
    canvas_elem = window['canvas']
    canvas = canvas_elem.Widget
    canvas_elem.Widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_elem.Widget.get_tk_widget().pack(side='top', fill='both', expand=1)
    canvas_elem.Widget.draw()

    # Defines functions for the GUI buttons
    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        elif event == 'Start Localisation':
            # Records Audio Signals
            window['msg'].update(value='Recording Signals')
            window.refresh()
            subprocess.run("bash main.sh", shell=True)

            # Extracts and processes signals
            window['msg'].update(value='Processing Signals')
            window.refresh()
            raw_signals, processed_signals, cal_signals, src_signals, fs = acquire_signals(['recording_1.wav', 'recording_2.wav'])
            t = np.linspace(0, len(raw_signals[0]) / fs, len(raw_signals[0]))

            # Determines synchronisation delays relative to the calibration signal of Mic 1
            window['msg'].update(value='Estimating Synchronisation Delays')
            window.refresh()
            sync_delays, sync_cross_correlations, sync_lags = estimate_delays(cal_signals, cal_signals[0], fs, 10)
            window['sync1'].update(value=f'{sync_delays[0] * 1000:.3f}')
            window['sync2'].update(value=f'{sync_delays[1] * 1000:.3f}')
            window['sync3'].update(value=f'{sync_delays[2] * 1000:.3f}')
            window['sync4'].update(value=f'{sync_delays[3] * 1000:.3f}')

            # Determines ToA delays relative to the source signal of Mic 1
            window['msg'].update(value='Estimating ToA Delays')
            window.refresh()
            toa_delays, toa_cross_correlations, toa_lags = estimate_delays(src_signals, src_signals[0], fs, 10)
            window['toa1'].update(value=f'{toa_delays[0] * 1000:.3f}')
            window['toa2'].update(value=f'{toa_delays[1] * 1000:.3f}')
            window['toa3'].update(value=f'{toa_delays[2] * 1000:.3f}')
            window['toa4'].update(value=f'{toa_delays[3] * 1000:.3f}')

            # Determines the TDoA values relative to the source signal of Mic1
            tdoa = ((toa_delays[0] - toa_delays) - (sync_delays[0] - sync_delays))[1:]
            window['tdoa12'].update(value=f'{tdoa[0] * 1000:.3f}')
            window['tdoa13'].update(value=f'{tdoa[1] * 1000:.3f}')
            window['tdoa14'].update(value=f'{tdoa[2] * 1000:.3f}')

            # Estimates the source position
            window['msg'].update(value='Triangulating Source Position')
            window.refresh()
            p, p0 = triangulate([0, 0], [0, 0.5], [0.8, 0.5], [0.8, 0], tdoa[0], tdoa[1], tdoa[2], 343)
            x, y = np.round(p, 3)
            x0, y0 = np.round(p0, 3)
            window['x'].update(value=f'{x:.3f}')
            window['y'].update(value=f'{y:.3f}')
            window['x0'].update(value=f'{x0:.3f}')
            window['y0'].update(value=f'{y0:.3f}')

            # Displays the result
            localisation = True
            window['msg'].update(value='Localisation Complete')
            if 0 <= x <= 0.8 and 0 <= y <= 0.5:
                fig = plot_point(fig, x, y)
                canvas_elem.Widget.draw()

            else:
                sg.popup_error('Estimated Source Position is Outside Grid')

        elif event == 'Signal Acquisition Plots':
            if localisation:
                signal_acquisition_plots(raw_signals, processed_signals, t)
            else:
                sg.popup_error('No Localisation Data')

        elif event == 'Synchronisation Plots':
            if localisation:
                synchronisation_plots(sync_cross_correlations, sync_lags[0])
            else:
                sg.popup_error('No Localisation Data')

        elif event == 'Time Delay Estimation Plots':
            if localisation:
                time_delay_estimation_plots(toa_cross_correlations, toa_lags[0])
            else:
                sg.popup_error('No Localisation Data')

        elif event == 'Reset Grid':
            reset_grid(fig)
            canvas_elem.Widget.draw()

    window.close()


if __name__ == '__main__':
    main()

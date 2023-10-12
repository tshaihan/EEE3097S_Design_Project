import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_acquisition import acquire_signals
from synchronisation import synchronise, shift
from time_delay_estimation import tdoa
from triangulation import triangulate


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


def plot_point(fig, x, y):
    ax = fig.gca()
    ax.plot(x, y, marker='o', markersize=8, label='Estimated Source Position')
    ax.legend()
    return fig


def reset_grid(fig):
    ax = fig.gca()
    ax.cla()
    init_grid(fig)
    return fig


def signal_acquisition_plots(raw_signals, t1, src_signals, ref_signals, t2):
    fig, ax = plt.subplots(4, 3)
    for i in range(4):
        ax[i, 0].plot(t1, raw_signals[i])
        ax[i, 1].plot(t2, src_signals[i])
        ax[i, 2].plot(t2, ref_signals[i])

    # Embed the graphs in a PySimpleGUI window
    layout = [[sg.Canvas(key='-CANVAS-')], [sg.Button('Close')]]
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


def synchronisation_plots(src_signals, sync_src_signals, t, cross_correlations, lags):
    fig, ax = plt.subplots(4, 3)
    for i in range(4):
        ax[i, 0].plot(t, src_signals[i])
        ax[i, 1].plot(t, sync_src_signals[i])
    for i in range(2):
        ax[i, 2].plot(lags, cross_correlations[i])

    # Embed the graphs in a PySimpleGUI window
    layout = [[sg.Canvas(key='-CANVAS-')], [sg.Button('Close')]]
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


def time_delay_estimation_plots(cross_correlations, lags):
    fig, ax = plt.subplots(3)
    for i in range(3):
        ax[i].plot(lags, cross_correlations[i])

    # Embed the graphs in a PySimpleGUI window
    layout = [[sg.Canvas(key='-CANVAS-')], [sg.Button('Close')]]
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
    localisation = False
    fig, ax = plt.subplots()
    init_grid(fig)

    layout = [
        [sg.Button('Start Localisation'), sg.Button('Reset Grid'), sg.Button('Exit')],
        [sg.Text(key='msg', size=(20, 1))],
        [sg.Text('Estimated Synchronisation Delay (ms):', size=(50, 1))],
        [sg.Text(key='sync_delay', size=(10, 1))],
        [sg.Text('Estimated TDoA Delays (ms):', size=(50, 1))],
        [sg.Text(key='tdoa12', size=(10, 1)), sg.Text(key='tdoa13', size=(10, 1)), sg.Text(key='tdoa14', size=(10, 1))],
        [sg.Text('Estimated Source Position (m):', size=(50, 1))],
        [sg.Text(key='x_value', size=(10, 1)), sg.Text(key='y_value', size=(10, 1))],
        [sg.Button('Signal Acquisition Plots'), sg.Button('Synchronisation Plots'), sg.Button('Time Delay Estimation Plots')],
        [sg.Canvas(key='canvas')]
    ]

    window = sg.Window('EEE3097S Design Project: Group 2', layout, resizable=True, finalize=True, element_justification='center')
    canvas_elem = window['canvas']
    canvas = canvas_elem.Widget
    canvas_elem.Widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_elem.Widget.get_tk_widget().pack(side='top', fill='both', expand=1)
    canvas_elem.Widget.draw()

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        elif event == 'Start Localisation':
            window['msg'].update(value='Recording Signals')
            # subprocess.run("bash main.sh", shell=True)

            window['msg'].update(value='Processing Signals')
            src_signals, ref_signals, fs, raw_signals, raw_fs = acquire_signals(['recording_1.wav', 'recording_2.wav'])
            t1 = np.linspace(0, len(raw_signals[0]) / raw_fs, len(raw_signals[0]))
            t2 = np.linspace(0, len(src_signals[0]) / fs, len(src_signals[0]))

            window['msg'].update(value='Synchronizing Signals')
            _, sync_delays, sync_cross_correlations, sync_lags = (
                synchronise([src_signals[0], src_signals[2], src_signals[3]],
                            [ref_signals[0], ref_signals[2], ref_signals[3]], fs, allow_shift=False))
            sync_delay = np.mean(sync_delays)
            sync_src_signals = np.copy(src_signals)
            sync_src_signals[2] = shift(sync_src_signals[2], sync_delays[0], fs)
            sync_src_signals[3] = shift(sync_src_signals[3], sync_delays[1], fs)
            window['sync_delay'].update(value=f'{sync_delay*1000:.3f}')

            window['msg'].update(value='Estimating Time Delays')
            tdoa_delays, tdoa_cross_correlations, tdoa_lags = tdoa(sync_src_signals, fs)
            window['tdoa12'].update(value=f'{tdoa_delays[0]*1000:.3f}')
            window['tdoa13'].update(value=f'{tdoa_delays[1]*1000:.3f}')
            window['tdoa14'].update(value=f'{tdoa_delays[2]*1000:.3f}')

            window['msg'].update(value='Triangulating Source Position')
            c = 343
            d12, d13, d14 = tdoa_delays * c
            p, p0 = triangulate([0, 0], [0, 0.5], [0.8, 0.5], [0.8, 0], d12, d13, d14)
            x, y = np.round(p, 3)
            x0, y0 = np.round(p0, 3)
            window['msg'].update(value='Localisation Complete')
            localisation = True

            if 0 <= x <= 0.8 and 0 <= y <= 0.5:
                fig = plot_point(fig, x, y)
                canvas_elem.Widget.draw()
                window['x_value'].update(value=f'{x:.3f}')
                window['y_value'].update(value=f'{y:.3f}')
            else:
                sg.popup_error('Estimated Source Position is Outside Grid')
                window['x_value'].update(value='')
                window['y_value'].update(value='')


        elif event == 'Signal Acquisition Plots':
            if localisation:
                signal_acquisition_plots(raw_signals, t1, src_signals, ref_signals, t2)
            else:
                sg.popup_error('No Localisation Data')

        elif event == 'Synchronisation Plots':
            if localisation:
                synchronisation_plots(src_signals, sync_src_signals, t2, sync_cross_correlations, sync_lags[0])
            else:
                sg.popup_error('No Localisation Data')

        elif event == 'Time Delay Estimation Plots':
            if localisation:
                time_delay_estimation_plots(tdoa_cross_correlations, tdoa_lags[0])
            else:
                sg.popup_error('No Localisation Data')

        elif event == 'Reset Grid':
            reset_grid(fig)
            canvas_elem.Widget.draw()

    window.close()


if __name__ == '__main__':
    main()

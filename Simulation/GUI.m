classdef GUI < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                    matlab.ui.Figure
        MDSHAIHANISLAMLabel         matlab.ui.control.Label
        TILALMUKHTARLabel           matlab.ui.control.Label
        AIMEESIMONSLabel            matlab.ui.control.Label
        GROUP2Label                 matlab.ui.control.Label
        EEE3097SSIMULATIONLabel     matlab.ui.control.Label
        TabGroup                    matlab.ui.container.TabGroup
        SimulateTab                 matlab.ui.container.Tab
        HelptextTextArea            matlab.ui.control.TextArea
        HelpButton                  matlab.ui.control.Button
        YCoordinateEditField        matlab.ui.control.NumericEditField
        YCoordinateEditFieldLabel   matlab.ui.control.Label
        XCoordinateEditField        matlab.ui.control.NumericEditField
        XCoordinateEditFieldLabel   matlab.ui.control.Label
        FindSoundSourceButton       matlab.ui.control.Button
        Label                       matlab.ui.control.Label
        Label_2                     matlab.ui.control.Label
        X_PredictedLabel            matlab.ui.control.Label
        Y_PredictedLabel            matlab.ui.control.Label
        UIAxes                      matlab.ui.control.UIAxes
        EditTab                     matlab.ui.container.Tab
        SyncerrorEditField          matlab.ui.control.NumericEditField
        SyncerrorEditFieldLabel     matlab.ui.control.Label
        MicposerrorEditField        matlab.ui.control.NumericEditField
        MicposerrorEditFieldLabel   matlab.ui.control.Label
        CalposerrorEditField        matlab.ui.control.NumericEditField
        CalposerrorEditFieldLabel   matlab.ui.control.Label
        PassbandfreqEditField       matlab.ui.control.NumericEditField
        PassbandfreqEditFieldLabel  matlab.ui.control.Label
        SNREditField                matlab.ui.control.NumericEditField
        SNREditFieldLabel           matlab.ui.control.Label
        SamplerateEditField         matlab.ui.control.NumericEditField
        SamplerateEditFieldLabel    matlab.ui.control.Label
        MaxcalfreqEditField         matlab.ui.control.NumericEditField
        MaxcalfreqEditFieldLabel    matlab.ui.control.Label
        MaxsrcfreqEditField         matlab.ui.control.NumericEditField
        MaxsrcfreqEditFieldLabel    matlab.ui.control.Label
        SpeedofsoundEditField       matlab.ui.control.NumericEditField
        SpeedofsoundEditFieldLabel  matlab.ui.control.Label
        OptionalparametersLabel     matlab.ui.control.Label
    end

    
    properties (Access = private)
        m1_x = 0.0
        m1_y = 0.0

        m2_x = 0.0
        m2_y = 0.5


        m3_x = 0.8
        m3_y = 0.0


        m4_x = 0.8
        m4_y = 0.5
    end
    
    methods (Access = private)
        
        function Initialise_Mics(app)
        
        plot(app.UIAxes,app.m1_x*1.25,app.m1_y*2, 'o', 'Color','r')
        hold(app.UIAxes, 'on');

        plot(app.UIAxes,app.m2_x*1.25,app.m2_y*2, 'o', 'Color','r')
        hold(app.UIAxes, 'on');

        plot(app.UIAxes,app.m3_x*1.25,app.m3_y*2, 'o', 'Color','b')
        hold(app.UIAxes, 'on');

        plot(app.UIAxes,app.m4_x*1.25,app.m4_y*2, 'o', 'Color','b')
        hold(app.UIAxes, 'on');
            
        end
    end
    

    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app)
            Initialise_Mics(app); 
            plot(app.UIAxes,0.5,0.5,"*")
            hold(app.UIAxes,"on")
            text(app.UIAxes,0.52,0.5,'CS','fontsize' , 10)
            hold(app.UIAxes,"on");
            lgd = legend(app.UIAxes,{'Mic 1', 'Mic 2', 'Mic 3', 'Mic 4', 'Calibration Signal'}, 'Location', 'southeastoutside');
            title(lgd, "Legend")

        end

        % Button pushed function: FindSoundSourceButton
        function FindSoundSourceButtonPushed(app, event)
            x_s = app.XCoordinateEditField.Value;
            y_s = app.YCoordinateEditField.Value;

            c = app.SpeedofsoundEditField.Value;
            srcFreq = app.MaxsrcfreqEditField.Value;
            calFreq = app.MaxcalfreqEditField.Value;
            samplerate = app.SamplerateEditField.Value;
            snr = app.SNREditField.Value;
            pbfreq = app.PassbandfreqEditField.Value;
            calposerror = app.CalposerrorEditField.Value;
            micposerror = app.MicposerrorEditField.Value;
            syncerror = app.SyncerrorEditField.Value;

            if (x_s>0.8||x_s<0)||(y_s>0.5||y_s<0)
                f = msgbox("Position out of bounds, please stay within the grid","Error","error");
            else 
                plot(app.UIAxes, x_s*1.25, y_s*2,'*')
                hold(app.UIAxes, 'on');
    
                coords = simulation(x_s,y_s, snr, samplerate, pbfreq, syncerror,  calposerror, micposerror, srcFreq, calFreq, c, [x_s, y_s], [x_s/2, y_s/2], [0, 0], [0, 0.5], [0.8, 0], [0.8, 0.5]);
    
                plot(app.UIAxes,coords(1)*1.25,coords(2)*2,"-s")
                hold(app.UIAxes,'on')
                    
                lgd = legend(app.UIAxes,{'Mic 1', 'Mic 2', 'Mic 3', 'Mic 4', 'Calibration Signal', 'Actual Position', 'Estimated Position'}, 'Location', 'southeastoutside');
                title(lgd, "Legend")

                app.Label.Text = string(coords(1));
                app.Label_2.Text = string(coords(2));
            end
        end

        % Button pushed function: HelpButton
        function HelpButtonPushed(app, event)
            app.HelptextTextArea.Visible = "on";
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Position = [100 100 1095 622];
            app.UIFigure.Name = 'MATLAB App';

            % Create TabGroup
            app.TabGroup = uitabgroup(app.UIFigure);
            app.TabGroup.Position = [27 12 999 469];

            % Create SimulateTab
            app.SimulateTab = uitab(app.TabGroup);
            app.SimulateTab.Title = 'Simulate';

            % Create UIAxes
            app.UIAxes = uiaxes(app.SimulateTab);
            title(app.UIAxes, 'A1 Grid')
            xlabel(app.UIAxes, 'x')
            ylabel(app.UIAxes, 'y')
            zlabel(app.UIAxes, 'z')
            app.UIAxes.XTick = [0 0.125 0.25 0.375 0.5 0.625 0.75 0.875 1];
            app.UIAxes.XTickLabelRotation = 0;
            app.UIAxes.XTickLabel = {'0'; '0.1'; '0.2'; '0.3'; '0.4'; '0.5'; '0.6'; '0.7'; '0.8'};
            app.UIAxes.YTick = [0 0.2 0.4 0.6 0.8 1];
            app.UIAxes.YTickLabelRotation = 0;
            app.UIAxes.YTickLabel = {'0'; '0.1'; '0.2'; '0.3'; '0.4'; '0.5'};
            app.UIAxes.XGrid = 'on';
            app.UIAxes.YGrid = 'on';
            app.UIAxes.Clipping = 'off';
            app.UIAxes.Position = [259 97 725 334];

            % Create Y_PredictedLabel
            app.Y_PredictedLabel = uilabel(app.SimulateTab);
            app.Y_PredictedLabel.Position = [35 213 70 22];
            app.Y_PredictedLabel.Text = 'y estimate';

            % Create X_PredictedLabel
            app.X_PredictedLabel = uilabel(app.SimulateTab);
            app.X_PredictedLabel.Position = [35 246 70 22];
            app.X_PredictedLabel.Text = 'x estimate';

            % Create Label_2
            app.Label_2 = uilabel(app.SimulateTab);
            app.Label_2.Position = [150 211 53 22];
            app.Label_2.Text = '';

            % Create Label
            app.Label = uilabel(app.SimulateTab);
            app.Label.Position = [150 245 50 22];
            app.Label.Text = '';

            % Create FindSoundSourceButton
            app.FindSoundSourceButton = uibutton(app.SimulateTab, 'push');
            app.FindSoundSourceButton.ButtonPushedFcn = createCallbackFcn(app, @FindSoundSourceButtonPushed, true);
            app.FindSoundSourceButton.Position = [70 292 118 23];
            app.FindSoundSourceButton.Text = 'Find Sound Source';

            % Create XCoordinateEditFieldLabel
            app.XCoordinateEditFieldLabel = uilabel(app.SimulateTab);
            app.XCoordinateEditFieldLabel.HorizontalAlignment = 'right';
            app.XCoordinateEditFieldLabel.Position = [26 392 76 22];
            app.XCoordinateEditFieldLabel.Text = 'x coordinate';

            % Create XCoordinateEditField
            app.XCoordinateEditField = uieditfield(app.SimulateTab, 'numeric');
            app.XCoordinateEditField.Position = [117 392 100 22];

            % Create YCoordinateEditFieldLabel
            app.YCoordinateEditFieldLabel = uilabel(app.SimulateTab);
            app.YCoordinateEditFieldLabel.HorizontalAlignment = 'right';
            app.YCoordinateEditFieldLabel.Position = [27 352 75 22];
            app.YCoordinateEditFieldLabel.Text = 'y coordinate';

            % Create YCoordinateEditField
            app.YCoordinateEditField = uieditfield(app.SimulateTab, 'numeric');
            app.YCoordinateEditField.Position = [117 352 100 22];

            % Create HelpButton
            app.HelpButton = uibutton(app.SimulateTab, 'push');
            app.HelpButton.ButtonPushedFcn = createCallbackFcn(app, @HelpButtonPushed, true);
            app.HelpButton.Position = [25 177 100 23];
            app.HelpButton.Text = 'Help';

            % Create HelptextTextArea
            app.HelptextTextArea = uitextarea(app.SimulateTab);
            app.HelptextTextArea.Editable = 'off';
            app.HelptextTextArea.Visible = 'off';
            app.HelptextTextArea.Placeholder = 'Welcome to the simulation program! This program simulates four different microphones, each placed on each corner of the grid, working together to detect a sound source within placed at a location of your choice in the grid. To set the position of the sound source, change the values of the x- and y-coordinates, and press the "Find Sound Source" button. The coordinates of the sound, as detected by the microphones will be displayed. To change other parameters, click on the "Edit" tab.';
            app.HelptextTextArea.Position = [12 14 248 150];

            % Create EditTab
            app.EditTab = uitab(app.TabGroup);
            app.EditTab.Title = 'Edit';

            % Create OptionalparametersLabel
            app.OptionalparametersLabel = uilabel(app.EditTab);
            app.OptionalparametersLabel.FontSize = 18;
            app.OptionalparametersLabel.FontWeight = 'bold';
            app.OptionalparametersLabel.Position = [16 391 180 41];
            app.OptionalparametersLabel.Text = 'Simulation Parameters';

            % Create SpeedofsoundEditFieldLabel
            app.SpeedofsoundEditFieldLabel = uilabel(app.EditTab);
            app.SpeedofsoundEditFieldLabel.HorizontalAlignment = 'right';
            app.SpeedofsoundEditFieldLabel.Position = [16 361 89 22];
            app.SpeedofsoundEditFieldLabel.Text = 'Speed of Sound (m/s)';

            % Create SpeedofsoundEditField
            app.SpeedofsoundEditField = uieditfield(app.EditTab, 'numeric');
            app.SpeedofsoundEditField.Position = [120 361 100 22];
            app.SpeedofsoundEditField.Value = 343;

            % Create MaxsrcfreqEditFieldLabel
            app.MaxsrcfreqEditFieldLabel = uilabel(app.EditTab);
            app.MaxsrcfreqEditFieldLabel.HorizontalAlignment = 'right';
            app.MaxsrcfreqEditFieldLabel.Position = [34 331 71 22];
            app.MaxsrcfreqEditFieldLabel.Text = 'Maximum Source Frequency (Hz)';

            % Create MaxsrcfreqEditField
            app.MaxsrcfreqEditField = uieditfield(app.EditTab, 'numeric');
            app.MaxsrcfreqEditField.Position = [120 331 100 22];
            app.MaxsrcfreqEditField.Value = 100;

            % Create MaxcalfreqEditFieldLabel
            app.MaxcalfreqEditFieldLabel = uilabel(app.EditTab);
            app.MaxcalfreqEditFieldLabel.HorizontalAlignment = 'right';
            app.MaxcalfreqEditFieldLabel.Position = [35 299 70 22];
            app.MaxcalfreqEditFieldLabel.Text = 'Maximum Calibration Frequency (Hz)';

            % Create MaxcalfreqEditField
            app.MaxcalfreqEditField = uieditfield(app.EditTab, 'numeric');
            app.MaxcalfreqEditField.Position = [120 299 100 22];
            app.MaxcalfreqEditField.Value = 1000;

            % Create SamplerateEditFieldLabel
            app.SamplerateEditFieldLabel = uilabel(app.EditTab);
            app.SamplerateEditFieldLabel.HorizontalAlignment = 'right';
            app.SamplerateEditFieldLabel.Position = [35 266 70 22];
            app.SamplerateEditFieldLabel.Text = 'Sample Rate (Hz)';

            % Create SamplerateEditField
            app.SamplerateEditField = uieditfield(app.EditTab, 'numeric');
            app.SamplerateEditField.Position = [120 266 100 22];
            app.SamplerateEditField.Value = 48000;

            % Create SNREditFieldLabel
            app.SNREditFieldLabel = uilabel(app.EditTab);
            app.SNREditFieldLabel.HorizontalAlignment = 'right';
            app.SNREditFieldLabel.Position = [75 232 30 22];
            app.SNREditFieldLabel.Text = 'SNR';

            % Create SNREditField
            app.SNREditField = uieditfield(app.EditTab, 'numeric');
            app.SNREditField.Position = [120 232 100 22];
            app.SNREditField.Value = 65;

            % Create PassbandfreqEditFieldLabel
            app.PassbandfreqEditFieldLabel = uilabel(app.EditTab);
            app.PassbandfreqEditFieldLabel.HorizontalAlignment = 'right';
            app.PassbandfreqEditFieldLabel.Position = [23 199 82 22];
            app.PassbandfreqEditFieldLabel.Text = 'Filter Cuttoff Frequency (Hz)';

            % Create PassbandfreqEditField
            app.PassbandfreqEditField = uieditfield(app.EditTab, 'numeric');
            app.PassbandfreqEditField.Position = [120 199 100 22];
            app.PassbandfreqEditField.Value = 15000;

            % Create CalposerrorEditFieldLabel
            app.CalposerrorEditFieldLabel = uilabel(app.EditTab);
            app.CalposerrorEditFieldLabel.HorizontalAlignment = 'right';
            app.CalposerrorEditFieldLabel.Position = [31 163 74 22];
            app.CalposerrorEditFieldLabel.Text = 'Calibration Position Error Factor (m)';

            % Create CalposerrorEditField
            app.CalposerrorEditField = uieditfield(app.EditTab, 'numeric');
            app.CalposerrorEditField.Position = [120 163 100 22];
            app.CalposerrorEditField.Value = 0.001;

            % Create MicposerrorEditFieldLabel
            app.MicposerrorEditFieldLabel = uilabel(app.EditTab);
            app.MicposerrorEditFieldLabel.HorizontalAlignment = 'right';
            app.MicposerrorEditFieldLabel.Position = [29 129 75 22];
            app.MicposerrorEditFieldLabel.Text = 'Mic Position Error Factor (m)';

            % Create MicposerrorEditField
            app.MicposerrorEditField = uieditfield(app.EditTab, 'numeric');
            app.MicposerrorEditField.Position = [119 129 100 22];
            app.MicposerrorEditField.Value = 0.001;

            % Create SyncerrorEditFieldLabel
            app.SyncerrorEditFieldLabel = uilabel(app.EditTab);
            app.SyncerrorEditFieldLabel.HorizontalAlignment = 'right';
            app.SyncerrorEditFieldLabel.Position = [45 96 60 22];
            app.SyncerrorEditFieldLabel.Text = 'Latency (s)';

            % Create SyncerrorEditField
            app.SyncerrorEditField = uieditfield(app.EditTab, 'numeric');
            app.SyncerrorEditField.Position = [120 96 100 22];
            app.SyncerrorEditField.Value = 0.01;

            % Create EEE3097SSIMULATIONLabel
            app.EEE3097SSIMULATIONLabel = uilabel(app.UIFigure);
            app.EEE3097SSIMULATIONLabel.FontSize = 18;
            app.EEE3097SSIMULATIONLabel.Position = [27 584 208 23];
            app.EEE3097SSIMULATIONLabel.Text = 'EEE3097S SIMULATION';

            % Create GROUP2Label
            app.GROUP2Label = uilabel(app.UIFigure);
            app.GROUP2Label.FontSize = 14;
            app.GROUP2Label.Position = [28 558 68 22];
            app.GROUP2Label.Text = 'GROUP 2';

            % Create AIMEESIMONSLabel
            app.AIMEESIMONSLabel = uilabel(app.UIFigure);
            app.AIMEESIMONSLabel.FontSize = 14;
            app.AIMEESIMONSLabel.Position = [27 538 108 22];
            app.AIMEESIMONSLabel.Text = 'AIMEE SIMONS';

            % Create TILALMUKHTARLabel
            app.TILALMUKHTARLabel = uilabel(app.UIFigure);
            app.TILALMUKHTARLabel.FontSize = 14;
            app.TILALMUKHTARLabel.Position = [27 518 114 22];
            app.TILALMUKHTARLabel.Text = 'TILAL MUKHTAR';

            % Create MDSHAIHANISLAMLabel
            app.MDSHAIHANISLAMLabel = uilabel(app.UIFigure);
            app.MDSHAIHANISLAMLabel.FontSize = 14;
            app.MDSHAIHANISLAMLabel.Position = [27 498 139 22];
            app.MDSHAIHANISLAMLabel.Text = 'MD SHAIHAN ISLAM';

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = GUI

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            % Execute the startup function
            runStartupFcn(app, @startupFcn)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end
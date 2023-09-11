classdef app1 < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                   matlab.ui.Figure
        Y_PredictedLabel           matlab.ui.control.Label
        X_PredictedLabel           matlab.ui.control.Label
        Label_2                    matlab.ui.control.Label
        Label                      matlab.ui.control.Label
        YCoordinateEditField       matlab.ui.control.NumericEditField
        YCoordinateEditFieldLabel  matlab.ui.control.Label
        XCoordinateEditField       matlab.ui.control.NumericEditField
        XCoordinateEditFieldLabel  matlab.ui.control.Label
        FindSoundSourceButton      matlab.ui.control.Button
        UIAxes                     matlab.ui.control.UIAxes
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
            hold(app.UIAxes,"on")
        end

        % Button pushed function: FindSoundSourceButton
        function FindSoundSourceButtonPushed(app, event)
            x_s = app.XCoordinateEditField.Value;
            y_s = app.YCoordinateEditField.Value;

            if (x_s>0.8||x_s<0)||(y_s>0.5||y_s<0)
                f = msgbox("Position out of bounds, please stay within the grid","Error","error");
            else 
                plot(app.UIAxes, x_s*1.25, y_s*2,'*')
                hold(app.UIAxes, 'on');
    
                coords = simulation(x_s,y_s);
    
                plot(app.UIAxes,coords(1)*1.25,coords(2)*2,"-s")
                hold(app.UIAxes,'on')
    
                app.Label.Text = string(coords(1));
                app.Label_2.Text = string(coords(2));
            end



            


        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Position = [100 100 640 317];
            app.UIFigure.Name = 'MATLAB App';

            % Create UIAxes
            app.UIAxes = uiaxes(app.UIFigure);
            title(app.UIAxes, 'A1 Grid')
            xlabel(app.UIAxes, 'X')
            ylabel(app.UIAxes, 'Y')
            zlabel(app.UIAxes, 'Z')
            app.UIAxes.XTick = [0 0.125 0.25 0.375 0.5 0.625 0.75 0.875 1];
            app.UIAxes.XTickLabelRotation = 0;
            app.UIAxes.XTickLabel = {'0'; '0.1'; '0.2'; '0.3'; '0.4'; '0.5'; '0.6'; '0.7'; '0.8'};
            app.UIAxes.YTick = [0 0.2 0.4 0.6 0.8 1];
            app.UIAxes.YTickLabelRotation = 0;
            app.UIAxes.YTickLabel = {'0'; '0.1'; '0.2'; '0.3'; '0.4'; '0.5'};
            app.UIAxes.XGrid = 'on';
            app.UIAxes.YGrid = 'on';
            app.UIAxes.Position = [212 10 408 282];

            % Create FindSoundSourceButton
            app.FindSoundSourceButton = uibutton(app.UIFigure, 'push');
            app.FindSoundSourceButton.ButtonPushedFcn = createCallbackFcn(app, @FindSoundSourceButtonPushed, true);
            app.FindSoundSourceButton.Position = [50 139 118 23];
            app.FindSoundSourceButton.Text = 'Find Sound Source';

            % Create XCoordinateEditFieldLabel
            app.XCoordinateEditFieldLabel = uilabel(app.UIFigure);
            app.XCoordinateEditFieldLabel.HorizontalAlignment = 'right';
            app.XCoordinateEditFieldLabel.Position = [6 239 76 22];
            app.XCoordinateEditFieldLabel.Text = 'X-Coordinate';

            % Create XCoordinateEditField
            app.XCoordinateEditField = uieditfield(app.UIFigure, 'numeric');
            app.XCoordinateEditField.Position = [97 239 100 22];

            % Create YCoordinateEditFieldLabel
            app.YCoordinateEditFieldLabel = uilabel(app.UIFigure);
            app.YCoordinateEditFieldLabel.HorizontalAlignment = 'right';
            app.YCoordinateEditFieldLabel.Position = [7 199 75 22];
            app.YCoordinateEditFieldLabel.Text = 'Y-Coordinate';

            % Create YCoordinateEditField
            app.YCoordinateEditField = uieditfield(app.UIFigure, 'numeric');
            app.YCoordinateEditField.Position = [97 199 100 22];

            % Create Label
            app.Label = uilabel(app.UIFigure);
            app.Label.Position = [130 92 50 22];
            app.Label.Text = '';

            % Create Label_2
            app.Label_2 = uilabel(app.UIFigure);
            app.Label_2.Position = [130 58 53 22];
            app.Label_2.Text = '';

            % Create X_PredictedLabel
            app.X_PredictedLabel = uilabel(app.UIFigure);
            app.X_PredictedLabel.Position = [50 92 70 22];
            app.X_PredictedLabel.Text = 'X_Predicted';

            % Create Y_PredictedLabel
            app.Y_PredictedLabel = uilabel(app.UIFigure);
            app.Y_PredictedLabel.Position = [50 58 70 22];
            app.Y_PredictedLabel.Text = 'Y_Predicted';

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = app1

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
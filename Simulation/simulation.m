%% main function
function [estCoords, syncError, tdoaError, coordError] = simulation(x, y, varargin)
    p = inputParser;
    
    % Required parameters
    addRequired(p, 'x');                    % x coordinate of source signal
    addRequired(p, 'y');                    % y coordinate of source signal
    
    % Optional parameters
    addOptional(p, 'snr', 65);              % signal SNR (dBW)
    addOptional(p, 'sampleRate', 48000);    % signal sample rate (Hz)
    addOptional(p, 'cutoffFreq', 10000);    % cutoff frequency of lp filter (Hz)
    addOptional(p, 'latency', 0.01);        % delay due to signal desync (s)
    addOptional(p, 'calPosError', 0.005);   % error factor of calibration signal position (m)
    addOptional(p, 'micPosError', 0.005);   % error factor of mic position (m)
    addOptional(p, 'srcFreq', 100);         % max frequency of source chirp signal (Hz)
    addOptional(p, 'calFreq', 1000);        % max frequency of calibration chirp signal (Hz)
    addOptional(p, 'c', 343);               % speed of sound (m/s)
    addOptional(p, 'grid', [0.8, 0.5]);     % grid dimensions (m)
    addOptional(p, 'cal', [0.4, 0.25])      % position of calibration signal (m)
    addOptional(p, 'mic1', [0, 0]);         % position of mic 1 (m)
    addOptional(p, 'mic2', [0, 0.5]);       % position of mic 2 (m)
    addOptional(p, 'mic3', [0.8, 0]);       % position of mic 3 (m)
    addOptional(p, 'mic4', [0.8, 0.5]);     % position of mic 4 (m)
    
    % Assign input parameters
    parse(p, x, y, varargin{:});
    x = p.Results.x;
    y = p.Results.y;
    snr = p.Results.snr;
    sampleRate = p.Results.sampleRate;
    cutoffFreq = p.Results.cutoffFreq;
    latency = p.Results.latency;
    calPosError = p.Results.calPosError;
    micPosError = p.Results.micPosError;
    srcFreq = p.Results.srcFreq;
    calFreq = p.Results.calFreq;
    c = p.Results.c;
    grid = p.Results.grid;
    cal = p.Results.cal;
    mic1 = p.Results.mic1;
    mic2 = p.Results.mic2;
    mic3 = p.Results.mic3;
    mic4 = p.Results.mic4;
    
    % Apply error to calibration signal and mic positions
    cal = cal+(calPosError*randn(1, 2));
    mic1 = mic1+(micPosError*randn(1, 2));
    mic2 = mic2+(micPosError*randn(1, 2));
    mic3 = mic3+(micPosError*randn(1, 2));
    mic4 = mic4+(micPosError*randn(1, 2));
    
    % Calculate ideal source TOA values for each mic
    srcToa1 = sqrt((x-mic1(1))^2+(y-mic1(2))^2)/c;
    srcToa2 = sqrt((x-mic2(1))^2+(y-mic2(2))^2)/c;
    srcToa3 = sqrt((x-mic3(1))^2+(y-mic3(2))^2)/c;
    srcToa4 = sqrt((x-mic4(1))^2+(y-mic4(2))^2)/c;

    % Calculate known ideal calibration TOA values for each mic
    calToa1 = sqrt((mic1(1)-cal(1))^2+(mic1(2)-cal(2))^2)/c; 
    calToa2 = sqrt((mic2(1)-cal(1))^2+(mic2(2)-cal(2))^2)/c;
    calToa3 = sqrt((mic3(1)-cal(1))^2+(mic3(2)-cal(2))^2)/c;
    calToa4 = sqrt((mic4(1)-cal(1))^2+(mic4(2)-cal(2))^2)/c;
    
    % Generate signals
    t = linspace(0, 5, 5*sampleRate); % 5 second signals
    srcSig = cos(2*pi*srcFreq/10*t.^2); % 0-srcFreq Hz chirp
    calSig = cos(2*pi*calFreq/10*t.^2); % 0-calFreq Hz chirp
    calDelay = 2; % Start calibration signal 2s after recording
    srcDelay = 2; % Start source signal 2s after calibration signal
    sig1 = generateSignal(srcSig, calSig, srcToa1, calToa1, srcDelay, calDelay, 0, sampleRate, snr);
    sig2 = generateSignal(srcSig, calSig, srcToa2, calToa2, srcDelay, calDelay, 0, sampleRate, snr);
    sig3 = generateSignal(srcSig, calSig, srcToa3, calToa3, srcDelay, calDelay, latency, sampleRate, snr);
    sig4 = generateSignal(srcSig, calSig, srcToa4, calToa4, srcDelay, calDelay, latency, sampleRate, snr);
    [sig1, sig2, sig3, sig4] = equalizeLengths(sig1, sig2, sig3, sig4);

    % Lowpass filter signals
    [sig1, sig2, sig3, sig4] = lowpassFilter(sig1, sig2, sig3, sig4, cutoffFreq, sampleRate);

    % Synchronize signals
    [sig1, sig2, sig3, sig4, estDelays] = synchronize(calSig, sig1, sig2, sig3, sig4, calToa1, calToa2, calToa3, calToa4, sampleRate);
    
    % Time delay estimation
    [tdoa12, tdoa13, tdoa14] = tdoa(sig1, sig2, sig3, sig4, sampleRate);
    
    % Triangulation
    estCoords = triangulate(grid, mic1, mic2, mic3, mic4, tdoa12, tdoa13, tdoa14, c);
    estCoords = round(estCoords, 3);

    % Calculate Errors
    delaysTdoa = [0, latency, latency];
    estDelaysTdoa = estDelays(1)-[estDelays(2), estDelays(3), estDelays(4)];
    syncError = delaysTdoa - estDelaysTdoa;
    tdoaError = [(srcToa1-srcToa2)-tdoa12, (srcToa1-srcToa3)-tdoa13, (srcToa1-srcToa4)-tdoa14];
    coordError = [x-estCoords(1), y-estCoords(2)];
end

% Equalizes the lengths of the signals
function [sig1, sig2, sig3, sig4] = equalizeLengths(sig1, sig2, sig3, sig4)
    sigLen = max([length(sig1), length(sig2), length(sig3), length(sig4)]);
    sig1(sigLen) = 0;
    sig2(sigLen) = 0;
    sig3(sigLen) = 0;
    sig4(sigLen) = 0;
end

%% Signal Acquisition
% Generates signal with calibration and source signals
function sig = generateSignal(srcSig, calSig, srcToa, calToa, srcDelay, calDelay, recordingDelay, sampleRate, snr)
    % Determines length of signal
    sigLen = length(calSig) + length(srcSig) + round((srcToa+calToa+srcDelay+calDelay-recordingDelay+1)*sampleRate);
    sig = zeros(sigLen, 1);
    % Adds calibration signal
    % calDelay - delay between recording command and calibration signal start
    % recordingDelay - delay between recording command and recording start
    start = round((calToa+calDelay-recordingDelay)*sampleRate);
    stop = start + length(calSig) - 1;
    sig(start:stop) = calSig;
    % Adds source signal
    % srcDelay - delay between calibration signal and source signal starts
    start = stop + round((srcToa+srcDelay-calToa)*sampleRate);
    stop = start + length(srcSig) - 1;
    sig(start:stop) = srcSig;
    % Adds Gaussian white noise to signal
    sig = awgn(sig, snr, pow2db(bandpower(sig)));
end

% Applies a lowpass filter to signals
function [sig1, sig2, sig3, sig4] = lowpassFilter(sig1, sig2, sig3, sig4, cutoff, sampleRate)
    sig1 = lowpass(sig1, cutoff, sampleRate);
    sig2 = lowpass(sig2, cutoff, sampleRate);
    sig3 = lowpass(sig3, cutoff, sampleRate);
    sig4 = lowpass(sig4, cutoff, sampleRate);
end

%% Synchronization
% Synchronizes signals
function [sig1, sig2, sig3, sig4, delays] = synchronize(calSig, sig1, sig2, sig3, sig4, calToa1, calToa2, calToa3, calToa4, sampleRate)
    % Length of calibration signal with 10ms tolerance
    calLen = length(calSig) + 0.01*sampleRate;
    % Aligns the calibration signal format to the received signals
    calSig = transpose(calSig);
    calSig(length(sig1)) = 0;
    
    % Determines the estimated desync delays using calibration TOAs
    delay1 = round(gccphat(sig1, calSig) - calToa1*sampleRate);
    delay2 = round(gccphat(sig2, calSig) - calToa2*sampleRate);
    delay3 = round(gccphat(sig3, calSig) - calToa3*sampleRate);
    delay4 = round(gccphat(sig4, calSig) - calToa4*sampleRate);
    
    % Removes estimated desync delays
    sig1 = shiftSig(sig1, delay1);
    sig2 = shiftSig(sig2, delay2);
    sig3 = shiftSig(sig3, delay3);
    sig4 = shiftSig(sig4, delay4);
    
    % Remove calibration signal

    sig1(1:round(calLen+calToa1*sampleRate)) = 0;
    sig2(1:round(calLen+calToa2*sampleRate)) = 0;
    sig3(1:round(calLen+calToa3*sampleRate)) = 0;
    sig4(1:round(calLen+calToa4*sampleRate)) = 0;

    % Equalize signal lengths
    [sig1, sig2, sig3, sig4] = equalizeLengths(sig1, sig2, sig3, sig4);
    % Return estimated delays
    delays = [delay1, delay2, delay3, delay4]/sampleRate;
end

% Shifts the signal's start
function sig = shiftSig(sig, shift)
    if shift>=0
        sig = sig(shift:end);
    else
        sig = [zeros(abs(shift), 1); sig];
    end
end

%% Time Delay Estimation
% Estimates the TDOA values of the signals
function [tdoa12, tdoa13, tdoa14] = tdoa(sig1, sig2, sig3, sig4, sampleRate)
    tdoa12 = gccphat(sig1, sig2, sampleRate);
    tdoa13 = gccphat(sig1, sig3, sampleRate);
    tdoa14 = gccphat(sig1, sig4, sampleRate);
end

%% Triangulation
% Estimates the position of the source signal
function coords = triangulate(grid, m1, m2, m3, m4, t12, t13, t14, c)
    % Non-Linear LSE
    x = grid/2; % Uses center as initial point
    xdata = [m1(1), m1(2), m2(1), m2(2), m3(1), m3(2), m4(1), m4(2)];
    ydata = [t12*c, t13*c, t14*c];
    coords = lsqcurvefit(@func, x, xdata, ydata);
end

% Non-Linear LSE Optimization Function
function ydata = func(x, xdata)
    d12 = sqrt((xdata(1)-x(1))^2+(xdata(2)-x(2))^2)-sqrt((xdata(3)-x(1))^2+(xdata(4)-x(2))^2);
    d13 = sqrt((xdata(1)-x(1))^2+(xdata(2)-x(2))^2)-sqrt((xdata(5)-x(1))^2+(xdata(6)-x(2))^2);
    d14 = sqrt((xdata(1)-x(1))^2+(xdata(2)-x(2))^2)-sqrt((xdata(7)-x(1))^2+(xdata(8)-x(2))^2);
    ydata = [d12, d13, d14];
end

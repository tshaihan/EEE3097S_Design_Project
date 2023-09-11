%% main function
function [estimatedCoords] = main(x, y, varargin)
    p = inputParser
    
    % Required parameters
    addRequired(p, 'x');                    % x coordinate of source signal
    addRequired(p, 'y');                    % y coordinate of source signal
    
    % Optional parameters
    addOptional(p, 'c', 343);               % speed of sound in m/s
    addOptional(p, 'srcFreq', 100);         % max frequency of source chirp signal
    addOptional(p, 'calFreq', 1000);        % max frequency of calibration chirp signal
    addOptional(p, 'sampleRate', 48000);    % signal sample rate in Hz 
    addOptional(p, 'snr', 65);              % signal SNR in dBW
    addOptional(p, 'passFreq', 15000);      % position of 
    addOptional(p, 'cal', [x/2, y/2])       % position of calibration signal
    addOptional(p, 'mic1', [0, 0]);         % position of mic 1
    addOptional(p, 'mic2', [0, 0.5]);       % position of mic 2
    addOptional(p, 'mic3', [0.8, 0]);       % position of mic 3
    addOptional(p, 'mic4', [0.8, 0.5]);     % position of mic 4
    addOptional(p, 'calPosError', 0.001);   % error factor of calibration signal position
    addOptional(p, 'micPosError', 0.001);   % error factor of mic position
    addOptional(p, 'syncError', 0.01);      % error factor of signal synchronization
    
    % Assign input parameters
    parse(p, x, y, varargin{:});
    x = p.Results.x;
    y = p.Results.y;
    c = p.Results.c;
    srcFreq = p.Results.srcFreq;
    calFreq = p.Results.calFreq;
    sampleRate = p.Results.sampleRate;
    snr = p.Results.snr;
    passFreq = p.Results.passFreq;
    cal = p.Results.cal;
    mic1 = p.Results.mic1;
    mic2 = p.Results.mic2;
    mic3 = p.Results.mic3;
    mic4 = p.Results.mic4;
    calPosError = p.Results.calPosError;
    micPosError = p.Results.micPosError;
    syncError = p.Results.syncError;
    
    % Apply error to calibration signal and mic positions
    cal = cal+(calPosError*randn(1, 2));
    mic1 = mic1+(micPosError*randn(1, 2));
    mic2 = mic2+(micPosError*randn(1, 2));
    mic3 = mic3+(micPosError*randn(1, 2));
    mic4 = mic4+(micPosError*randn(1, 2));
    
    % Calculate source and calibration signal TOA values for each mic
    srcToa1 = sqrt((x-mic1(1))^2+(y-mic1(2))^2)/c;
    srcToa2 = sqrt((x-mic2(1))^2+(y-mic2(2))^2)/c;
    srcToa3 = sqrt((x-mic3(1))^2+(y-mic3(2))^2)/c;
    srcToa4 = sqrt((x-mic4(1))^2+(y-mic4(2))^2)/c;
    calToa1 = sqrt((mic1(1)-cal(1))^2+(mic1(2)-cal(2))^2)/c; 
    calToa2 = sqrt((mic2(1)-cal(1))^2+(mic2(2)-cal(2))^2)/c;
    calToa3 = sqrt((mic3(1)-cal(1))^2+(mic3(2)-cal(2))^2)/c;
    calToa4 = sqrt((mic4(1)-cal(1))^2+(mic4(2)-cal(2))^2)/c;
    
    %  Generate signals
    t = linspace(0, 5, 5*sampleRate);
    srcSig = cos(2*pi*srcFreq*t.^2);
    calSig = cos(2*pi*calFreq*t.^2);
    delay = round(rand(1, 2).*sampleRate*syncError);
    sig1 = generateSignal(srcSig, calSig, srcToa1, calToa1, sampleRate, delay(1),snr);
    sig2 = generateSignal(srcSig, calSig, srcToa2, calToa2, sampleRate, delay(1),snr);
    sig3 = generateSignal(srcSig, calSig, srcToa3, calToa3, sampleRate, delay(2),snr);
    sig4 = generateSignal(srcSig, calSig, srcToa4, calToa4, sampleRate, delay(2),snr);
    [sig1, sig2, sig3, sig4] = alignLengths(sig1, sig2, sig3, sig4);

    % Lowpass filter signals
    [sig1, sig2, sig3, sig4] = lowpassFilter(sig1, sig2, sig3, sig4, passFreq, sampleRate);

    % Synchronize signals
    [sig1, sig2, sig3, sig4] = synchronize(calSig, sig1, sig2, sig3, sig4);
    
    % Time delay estimation
    [tdoa12, tdoa13, tdoa14] = tdoa(sig1, sig2, sig3, sig4, sampleRate);
    
    % Triangulation
    estimatedCoords = triangulate(mic1, mic2, mic3, mic4, tdoa12, tdoa13, tdoa14, c);
end

% Equalizes the lengths of the signals
function [sig1, sig2, sig3, sig4] = alignLengths(sig1, sig2, sig3, sig4)
    sigLen = max([length(sig1), length(sig2), length(sig3), length(sig4)]);
    sig1(sigLen) = 0;
    sig2(sigLen) = 0;
    sig3(sigLen) = 0;
    sig4(sigLen) = 0;
end

%% Signal Acquisition
% Generates signal with calibration and source signals
function sig = generateSignal(srcSig, calSig, srcToa, calToa, sampleRate, syncError, snr)
    duration = syncError + length(calSig) + length(srcSig) + round((srcToa+calToa+2)*sampleRate); 
    sig = zeros(duration, 1);
    start = syncError + round(calToa*sampleRate);
    stop = start + length(calSig) - 1;
    sig(start:stop) = calSig;
    start = stop + round((srcToa+1)*sampleRate);
    stop = start + length(srcSig) - 1;
    sig(start:stop) = srcSig;
    sig = awgn(sig, snr, pow2db(bandpower(sig))); % Adds Gaussian white noise to signals
end

% Applies a lowpass filter to signals
function [sig1, sig2, sig3, sig4] = lowpassFilter(sig1, sig2, sig3, sig4, fpass, sampleRate)
    sig1 = lowpass(sig1, fpass, sampleRate);
    sig2 = lowpass(sig2, fpass, sampleRate);
    sig3 = lowpass(sig3, fpass, sampleRate);
    sig4 = lowpass(sig4, fpass, sampleRate);
end

%% Synchronization
% Synchronizes signals
function [sig1, sig2, sig3, sig4] = synchronize(calSig, sig1, sig2, sig3, sig4)
    calLen = length(calSig)+1;
    calSig = transpose(calSig);
    calSig(length(sig1)) = 0;
    
    delay1 = gccphat(sig1, calSig);
    delay2 = gccphat(sig2, calSig);
    delay3 = gccphat(sig3, calSig);
    delay4 = gccphat(sig4, calSig);

    sig1 = sig1(delay1+calLen:end);
    sig2 = sig2(delay2+calLen:end);
    sig3 = sig3(delay3+calLen:end);
    sig4 = sig4(delay4+calLen:end);

    [sig1, sig2, sig3, sig4] = alignLengths(sig1, sig2, sig3, sig4);
end

%% Time Delay Estimation
% Estimates the TDOA values of the signals
function [tdoa12, tdoa13, tdoa14] = tdoa(sig1, sig2, sig3, sig4, sampleRate);
    tdoa12 = gccphat(sig1, sig2, sampleRate);
    tdoa13 = gccphat(sig1, sig3, sampleRate);
    tdoa14 = gccphat(sig1, sig4, sampleRate);
end

%% Triangulation
% Estimates the position of the source signal
function coords = triangulate(m1, m2, m3, m4, t12, t13, t14, c)
    % Linear LSE
    A = [
        [m2(1) - m1(1), m2(2) - m1(2), -t12*c]
        [m3(1) - m1(1), m3(2) - m1(2), -t13*c]
        [m4(1) - m1(1), m4(2) - m1(2), -t14*c]
        ];
    b = [
        -(t12*c)^2 - m1(1)^2 - m1(2)^2 + m2(1)^2 + m2(2)^2
        -(t13*c)^2 - m1(1)^2 - m1(2)^2 + m3(1)^2 + m3(2)^2
        -(t14*c)^2 - m1(1)^2 - m1(2)^2 + m4(1)^2 + m4(2)^2
        ];
    coords = 0.5*lsqr(A, b);

    % Non-Linear LSE Refinement
    x = [coords(1), coords(2)];
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

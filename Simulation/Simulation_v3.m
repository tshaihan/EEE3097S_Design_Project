%% main function
function [coords] = main(x, y)
    c = 343;
    sampleRate = 48000;
    
    src = [x, y];
    cal =  [0.4, 0.25];
    mic1 = [0,0];
    mic2 = [0, 0.5];
    mic3 = [0.8, 0];
    mic4 = [0.8, 0.5];
    
    srcToa1 = sqrt((x-mic1(1))^2+(y-mic1(2))^2)/c;
    srcToa2 = sqrt((x-mic2(1))^2+(y-mic2(2))^2)/c;
    srcToa3 = sqrt((x-mic3(1))^2+(y-mic3(2))^2)/c;
    srcToa4 = sqrt((x-mic4(1))^2+(y-mic4(2))^2)/c;
    
    calToa1 = sqrt((mic1(1)-cal(1))^2+(mic1(2)-cal(2))^2)/c; 
    calToa2 = sqrt((mic2(1)-cal(1))^2+(mic2(2)-cal(2))^2)/c;
    calToa3 = sqrt((mic3(1)-cal(1))^2+(mic3(2)-cal(2))^2)/c;
    calToa4 = sqrt((mic4(1)-cal(1))^2+(mic4(2)-cal(2))^2)/c;
    
    %  Generate Signals
    t = linspace(0, 5, 5*sampleRate);
    srcSig = cos(2*pi*10*t);
    calSig = cos(2*pi*1000*t.^2);
    syncError = round(rand(1, 2).*sampleRate*1);
    sig1 = generateSignal(srcSig, calSig, srcToa1, calToa1, sampleRate, syncError(1));
    sig2 = generateSignal(srcSig, calSig, srcToa2, calToa2, sampleRate, syncError(1));
    sig3 = generateSignal(srcSig, calSig, srcToa3, calToa3, sampleRate, syncError(2));
    sig4 = generateSignal(srcSig, calSig, srcToa4, calToa4, sampleRate, syncError(2));
    [sig1, sig2, sig3, sig4] = alignLengths(sig1, sig2, sig3, sig4);
   

    % Synchronize Signals
    [sig1, sig2, sig3, sig4] = synchronize(calSig, sig1, sig2, sig3, sig4);
    
    %Adding noise
    [sig1,sig2,sig3,sig4] = noisy(sig1,sig2,sig3,sig4); 


    %Filter signals
    [sig1, sig2, sig3, sig4] = low_pass(sig1, sig2, sig3, sig4);
    
    % Time Delay Estimation
    tdoa12 = gccphat(sig1, sig2, sampleRate);
    tdoa13 = gccphat(sig1, sig3, sampleRate);
    tdoa14 = gccphat(sig1, sig4, sampleRate);
    
    % Triangulation
    coords = triangulate(mic1, mic2, mic3, mic4, tdoa12, tdoa13, tdoa14, c)
end

%% Synchronization
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

%% Signal Acquisition
function sig = generateSignal(srcSig, calSig, srcToa, calToa, sampleRate, syncError)
    duration = syncError + length(calSig) + length(srcSig) + round((srcToa+calToa+2)*sampleRate); 
    sig = zeros(duration, 1);
    start = syncError + round(calToa*sampleRate);
    stop = start + length(calSig) - 1;
    sig(start:stop) = calSig;
    start = stop + round((srcToa+1)*sampleRate);
    stop = start + length(srcSig) - 1;
    sig(start:stop) = srcSig;
end

function [sig1, sig2, sig3, sig4] = alignLengths(sig1, sig2, sig3, sig4)
    sigLen = max([length(sig1), length(sig2), length(sig3), length(sig4)]);
    sig1(sigLen) = 0;
    sig2(sigLen) = 0;
    sig3(sigLen) = 0;
    sig4(sigLen) = 0;
end

%% Triangulation
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

    % Non-Linear LSE
    x = [coords(1), coords(2)];
    xdata = [m1(1), m1(2), m2(1), m2(2), m3(1), m3(2), m4(1), m4(2)];
    ydata = [t12*c, t13*c, t14*c];
    coords = lsqcurvefit(@func, x, xdata, ydata);
end

function ydata = func(x, xdata)
    d12 = sqrt((xdata(1)-x(1))^2+(xdata(2)-x(2))^2)-sqrt((xdata(3)-x(1))^2+(xdata(4)-x(2))^2);
    d13 = sqrt((xdata(1)-x(1))^2+(xdata(2)-x(2))^2)-sqrt((xdata(5)-x(1))^2+(xdata(6)-x(2))^2);
    d14 = sqrt((xdata(1)-x(1))^2+(xdata(2)-x(2))^2)-sqrt((xdata(7)-x(1))^2+(xdata(8)-x(2))^2);
    ydata = [d12, d13, d14];
end



%% Signal Preprocessing

%Add Noise
function [sig1,sig2,sig3,sig4] = noisy(sig1,sig2,sig3,sig4)
noise = 0.05*rand(size(sig1));
sig1 = sig1 + noise;
sig2 = sig2 + noise;
sig3 = sig3 + noise;
sig4 = sig4 + noise;
end

%Filter signal
function [sig1, sig2, sig3, sig4] = low_pass(sig1, sig2, sig3, sig4)
    sig1 = lowpass(sig1,10,0.5*48000);
    sig2 = lowpass(sig2,10,0.5*48000);
    sig3 = lowpass(sig3,10,0.5*48000);
    sig4 = lowpass(sig4,10,0.5*48000);
    


   
end

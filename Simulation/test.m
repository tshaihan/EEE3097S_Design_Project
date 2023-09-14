function test
    fileID = fopen('results.csv','w');
    fprintf(fileID, 'Default Parameters\n');
    fprintf(fileID, 'x; y; x estimate; y estimate; sync error; TDOA error; position error\n');
    for i = 1:17
        for j = 1:11
            [coords, syncError, tdoaError, coordError] = simulation((i-1)/20, (j-1)/20);
            fprintf(fileID, '%f; %f; %f; %f;', (i-1)/20, (j-1)/20, coords(1), coords(2));
            posError = sqrt(coordError(1)^2+coordError(2)^2);
            fprintf(fileID, '%f; %f; %f\n', mean(syncError), mean(tdoaError), posError);
        end
    end

    fprintf(fileID, 'SNR\n');
    fprintf(fileID, 'x; y; x estimate; y estimate; sync error; TDOA error; position error; SNR\n');
    snr = 40;
    for i = 1:21
        [coords, syncError, tdoaError, coordError] = simulation(0.5, 0.25, snr);
        fprintf(fileID, '0.5; 0.25; %f; %f;', coords(1), coords(2));
        posError = sqrt(coordError(1)^2+coordError(2)^2);
        fprintf(fileID, '%f; %f; %f; %d\n', mean(syncError), mean(tdoaError), posError, snr);
        snr = snr + 2;
    end
    
    fprintf(fileID, 'Cutoff Frequency\n');
    fprintf(fileID, 'x; y; x estimate; y estimate; sync error; TDOA error; position error; cutoff frequeny\n');
    cutoff = 3000;
    for i = 1:18
        [coords, syncError, tdoaError, coordError] = simulation(0.5, 0.25, 65, 48000, cutoff);
        fprintf(fileID, '0.5; 0.25; %f; %f;', coords(1), coords(2));
        posError = sqrt(coordError(1)^2+coordError(2)^2);
        fprintf(fileID, '%f; %f; %f; %d\n', mean(syncError), mean(tdoaError), posError, cutoff);
        cutoff = cutoff + 1000;
    end
    
    fprintf(fileID, 'Latency\n');
    fprintf(fileID, 'x; y; x estimate; y estimate; sync error; TDOA error; position error; latency\n');
    latency = 0.001;
    for i = 1:11
        [coords, syncError, tdoaError, coordError] = simulation(0.5, 0.25, 65, 48000, 10000, latency);
        fprintf(fileID, '0.5; 0.25; %f; %f;', coords(1), coords(2));
        posError = sqrt(coordError(1)^2+coordError(2)^2);
        fprintf(fileID, '%f; %f; %f; %f\n', mean(syncError), mean(tdoaError), posError, latency);
        latency = latency * 2;
    end
    
    fprintf(fileID, 'Calibration Signal Position Error Factor\n');
    fprintf(fileID, 'x; y; x estimate; y estimate; sync error; TDOA error; position error; calibration signal position error factor\n');
    calPosError = 0.001;
    for i = 1:20
        for j = 1:3
            [coords(j,:), syncError(j,:), tdoaError(j,:), coordError(j,:)] = simulation(0.5, 0.25, 65, 48000, 10000, 0.01, calPosError);
        end
        fprintf(fileID, '0.5; 0.25; %f; %f;', mean(coords(:,1)), mean(coords(:,2)));
        posError = sqrt(mean(coordError(:,1))^2+mean(coordError(:,2))^2);
        fprintf(fileID, '%f; %f; %f; %f\n', mean(syncError,'all'), mean(tdoaError,'all'), posError, calPosError);
        calPosError = calPosError + 0.001;
    end

    fprintf(fileID, 'Mic Position Error Factor\n');
    fprintf(fileID, 'x; y; x estimate; y estimate; sync error; TDOA error; position error; mic position error factor\n');
    micPosError = 0.001;
    for i = 1:20
        for j = 1:3
            [coords(j,:), syncError(j,:), tdoaError(j,:), coordError(j,:)] = simulation(0.5, 0.25, 65, 48000, 10000, 0.01, 0.001, micPosError);
        end
        fprintf(fileID, '0.5; 0.25; %f; %f;', mean(coords(:,1)), mean(coords(:,2)));
        posError = sqrt(mean(coordError(:,1))^2+mean(coordError(:,2))^2);
        fprintf(fileID, '%f; %f; %f; %f\n', mean(syncError,'all'), mean(tdoaError,'all'), posError, micPosError);
        micPosError = micPosError + 0.001;
    end

    fprintf(fileID, 'Source Signal Frequency\n');
    fprintf(fileID, 'x; y; x estimate; y estimate; sync error; TDOA error; position error; source signal frequency\n');
    srcFreq = 10;
    for i = 1:11
        [coords, syncError, tdoaError, coordError] = simulation(0.5, 0.25, 65, 48000, 10000, 0.01, 0.001, 0.001, srcFreq);
        fprintf(fileID, '0.5; 0.25; %f; %f;', coords(1), coords(2));
        posError = sqrt(coordError(1)^2+coordError(2)^2);
        fprintf(fileID, '%f; %f; %f; %d\n', mean(syncError), mean(tdoaError), posError, srcFreq);
        srcFreq = srcFreq*2;
    end
    fclose(fileID);
end
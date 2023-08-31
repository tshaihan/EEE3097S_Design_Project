function main(x1,x2)%main function
[r,z] = coordinates(x1,x2)
[m1,m2,m3,m4] = delayMics(r,z)
t = linspace(0,1,100)
[q1,q2,q3,q4,t1,t2,t3,t4] = correlation(m1,m2,m3,m4)
[time1, time2, time3, time4] = findTimes(q1,q2,q3,q4,t1,t2,t3,t4)
end


function [x,y] = coordinates(x1,x2)
    x = x1
    y = x2
end

function [m1,m2,m3,m4] = delayMics(x,y)
    t = linspace(0,1,100)


    d1 =  sqrt((x-0)^2+(y-0)^2)
    t1 = d1/340
    m1 = sin(2*pi*200*(t-t1))%sinewave for mic1

    d2 =  sqrt((x-0)^2+(y-0.5)^2)
    t2 = d2/340
    m2 = sin(2*pi*200*(t-t2))%sinewave for mic2

    d3 =  sqrt((x-0.8)^2+(y-0.5)^2)
    t3 = d3/340
    m3 = sin(2*pi*200*(t-t3))%sinewave for mic3

    d4 =  sqrt((x-0.8)^2+(y-0)^2)
    t4 = d4/340
    m4 = sin(2*pi*200*(t-t4))%sinewave for mic4
end

function [q1,q2,q3,q4,t1,t2,t3,t4] = correlation(m1,m2,m3,m4)
    [q1,t1] = xcorr(m1,m2)%crosscorrelation between mic 1 and mic 2
    [q2,t2]= xcorr(m3,m4)%crosscorrelation between mic 3 and mic 4
    [q3,t3] = xcorr(m1,m4)%crosscorrelation between mic 1 and mic 4
    [q4,t4] = xcorr(m2,m3)%crosscorrelation between mic 2 and mic 3
end

function [time1, time2, time3, time4] = findTimes(q1,q2,q3,q4,t1,t2,t3,t4)
    time1 = abs(t1(q1==max(q1)))*0.01%time difference between 1 and mic 2
    time2 = abs(t2(q2==max(q2)))*0.01%time difference between 3 and mic 4
    time3 = abs(t3(q3==max(q3)))*0.01%time difference between 1 and mic 4
    time4 = abs(t4(q4==max(q4)))*0.01%time difference between 2 and mic 3
end







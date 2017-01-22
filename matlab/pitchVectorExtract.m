function result = pitchVectorExtract(sound_file_name)

    [y,fs] = audioread(sound_file_name);
%     sound(y,fs); % listen to that song
%     y = y/mean(y);

    info = audioinfo(sound_file_name);
    t = 0:seconds(1/fs):seconds(info.Duration);
    t = t(1:end-1);

    %1
%     c = spCepstrum(y, fs, 'hamming', 'plot');
%     pause

%     %2
%     c = spCepstrum(y, fs, 'hamming', 'plot');
%     f0 = spPitchCepstrum(c, fs)
%
    %3
%     figure;
    cd pitchVectorLib
    [F0, T, C] = spPitchTrackCepstrum(y, fs, 1000, 500, 'hamming'); %, 'plot'
    cd ..
%     pause
%     %4
%     r = spCorr(y, fs, [], 'plot');

    % Normalize the pitch vectors
%     F0 = F0/mean(F0);
%     F0 = normr(F0);
    result = F0;
    size(F0)
    return;

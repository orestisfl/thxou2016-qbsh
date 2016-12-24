function feature_vector = recorderUserSinging()
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
song_names = ['Twinkle, Twinkle, Little Star   ';
    'Old MacDonald Had a Farm        ';
    'Happy Birthday                  ';
    'Brother John (Are you sleeping?)';
    'London Bridge Is Falling Down   ';
    'Oh du lieber Augustin           '
    ];
recObj = audiorecorder;
disp('Start singing.');
recordblocking(recObj, 8);
disp('End of Recording.');
% play(recObj);
y = getaudiodata(recObj);
audiowrite('mytry.wav',y,8000);
pitch_vector_mine = pitchVectorExtract('mytry.wav');
index_array = myNeuralNetworkFunction6classes(pitch_vector_mine');
[maxprop,index] = max(index_array);
song_names(index,:)
maxprop
end


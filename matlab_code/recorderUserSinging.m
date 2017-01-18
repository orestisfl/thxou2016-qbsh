function feature_vector = recorderUserSinging()
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

% List of the song names
song_names = [
%     'Ten Little Indians              '; % 00011 - 96
    'Twinkle, Twinkle, Little Star   '; % 00014 - 159
    'Old MacDonald Had a Farm        '; % 00017 - 152
    'Happy Birthday                  '; % 00020 - 170
    'Brother John (Are you sleeping?)'; % 00022 - 173
    'Clay Doll (Niwawa)              '; % 00024 - 121
    'Jasmine                         '; % 00029 - 150
    'London Bridge Is Falling Down   '; % 00030 - 145
    'Home, Sweet Home                '; % 00034 - 137
    'Oh du lieber Augustin           '  % 00039 - 147 
    ];                                  %TODO This Old Man	126
recObj = audiorecorder;
disp('Start singing.');
recordblocking(recObj, 8);
disp('End of Recording.');
% play(recObj);
y = getaudiodata(recObj);
audiowrite('mytry.wav',y,8000);
pitch_vector_mine = pitchVectorExtract('mytry.wav');

% Here goes the neural network function
index_array = myNeuralNetworkFunction10classes(pitch_vector_mine')
[maxprop,index] = max(index_array);
song_names(index,:)
maxprop
end


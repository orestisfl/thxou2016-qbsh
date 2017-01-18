function [final,final_features,final_labels] = creationOfDataSet()
    folder_names = [%'00011';
        '00014';'00017';'00020';'00022';'00024'; ...
        '00029';'00030';'00034';'00039']
    final = data_fuser(folder_names);
    
    % Shuffle the final matrix
    final = final(randperm(size(final,1)),:);
    final_features = final(:,1:(end-1));
    final_labels = final(:,end);
    size(folder_names,1);
    final_labels = converterFromLabelToTarget(final_labels, size(folder_names,1));

function final_matrix = data_fuser(folder_names)
    nclasses = size(folder_names,1);
    final_matrix = creationOfData(folder_names(1,:),1);
    for i = 2:nclasses
        matrix = creationOfData(folder_names(i,:),i);
        final_matrix = [final_matrix;matrix];
    end
    
function final_matrix = creationOfData(audio_id,class_id)
    folder_name = strcat('../database/',audio_id,'/*.wav')
    files = dir(folder_name);
    counter = 1;
    number_of_features = 14; %TODO change it to get length of Extractor
    for file = files'
        file.name
        sound_file_name = strcat('../database/',audio_id,'/',file.name);
        final_matrix(counter,1:number_of_features) = pitchVectorExtract(sound_file_name);
        final_matrix(counter,(number_of_features+1)) = class_id;%TODO chane it back to a string
        counter = counter + 1
    end
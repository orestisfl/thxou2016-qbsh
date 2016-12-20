function final_matrix = first_function()
    folder_name1 = '00020';
    folder_name2 = '00014';
    folder_name3 = '00017';
    final_matrix = data_fuser(folder_name1,folder_name2,folder_name3);
    %shuffle the final matrix
    final_matrix = final_matrix(randperm(size(final_matrix,1)),:);
    %     shuffledArray = orderedArray(randperm(size(orderedArray,1)),:);

function final_matrix = data_fuser(folder_name1,folder_name2,folder_name3)
%     folder_name1 = '00020';
%     folder_name2 = '00014';
    matrix1 = creationOfData(folder_name1,0);
    matrix2 = creationOfData(folder_name2,1);
    matrix3 = creationOfData(folder_name3,2);
    final_matrix = [matrix1;matrix2;matrix3];
%     %shuffle the final matrix
%     shuffledArray = orderedArray(randperm(size(orderedArray,1)),:);
    
function reduced_array = reduceDimensions(preproc_array,nu)
    %TODO
    a=0

function final_matrix = creationOfData(audio_id,class_id)
    folder_name = strcat('../database/',audio_id,'/*.wav')
    files = dir(folder_name);
    counter = 1;
    number_of_features = 797; %TODO change it to get length of Extractor
%     final_matrix = zeros(length(files),number_of_features);
    for file = files'
        file.name
        final_matrix(counter,1:number_of_features) = pitchVectorExtract(audio_id,file.name);
        final_matrix(counter,(number_of_features+1)) = class_id;%TODO chane it back to a string
        counter = counter + 1
    end
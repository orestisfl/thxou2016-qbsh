function [y_targets] = converterFromLabelToTarget(y_labels,class_num)
    dataset_num = length(y_labels);
    y_targets = zeros(dataset_num,class_num);
    for i=1:dataset_num;
        y_targets(i,y_labels(i)+1)=1;
    end
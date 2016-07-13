%addpath(genpath('../libsvm-3.17/'))
% clear all;
% close all;


meta_data = importdata('../data/WoZAI_utterances_meta_data_4.csv',',');
sentence_vectors = importdata('../data/WoZAIUtterances_total.csv',',');
labels = meta_data(:,2) | meta_data(:,4);

mean_sentences = [];
mean_labels = [];

speaker_ids = unique(meta_data(:,1));

for ids = speaker_ids'
    mean_sentences = [mean_sentences; mean(sentence_vectors(meta_data(:,1) == ids, :))];
    mean_labels = [mean_labels; mean(labels(meta_data(:,1) == ids, :))];
end

% feature selection:
% mean_sentences = mean_sentences(:, ttest2(mean_sentences(mean_labels==1,:), mean_sentences(mean_labels==0,:)) == 1);

c = cvpartition(labels, 'kfold', 10);

minfn = @(z)kfoldLoss(fitcsvm(sentence_vectors(:,h == 1), labels, 'CVPartition',c,...
    'KernelFunction','rbf', 'BoxConstraint',exp(z(2)),...
    'KernelScale',exp(z(1))));

% minfn = @(z)kfoldLoss(fitcsvm(mean_sentences,mean_labels,  'CVPartition',c,...
%     'KernelFunction','rbf', 'BoxConstraint',exp(z(2)),...
%     'KernelScale',exp(z(1))));

% minfn = @(z)myLossFunction(sentence_vectors, labels, meta_data, z);


opts = optimset('TolX',5e-5,'TolFun',5e-5);

m = 10;
fval = zeros(m,1);
z = zeros(m,2);
for j = 1:m;
    [searchmin, fval(j)] = fminsearch(minfn,randn(2,1),opts);
    fval(j)
    z(j,:) = exp(searchmin)
end

z = z(fval == min(fval),:)


% minfn_mysig = @(z)kfoldLoss(fitcsvm(sentence_vectors,labels,'CVPartition',c,...
%     'KernelFunction','mysigmoid', 'Cost', [0,1;2,0], 'BoxConstraint',exp(z(2)),...
%     'KernelScale',exp(z(1))));
% 
% fval_mysig = zeros(m,1);
% z_mysig = zeros(m,2);
% for j = 1:m;
%     [searchmin_mysig, fval_mysig(j)] = fminsearch(minfn_mysig,randn(2,1),opts);
%     fval_mysig(j)
%     z_mysig(j,:) = exp(searchmin_mysig)
% end
% 
% z_mysig = z_mysig(fval_mysig == min(fval_mysig),:)


% Use 'Mode','individual' in kfoldLoss for individual error rates.


% SVMModel = fitcsvm(sentence_vectors, labels, 'KernelFunction', 'rbf', 'kFold', 10, 'BoxConstraint',z(2),...
%     'KernelScale',z(1));
% for i = 1:SVMModel.KFold
%     predicted_labels = predict(SVMModel.Trained{i}, sentence_vectors(SVMModel.Partition.test(i),:));
%     confusionmat(labels(SVMModel.Partition.test(i)), predicted_labels)
%     sum(diag(confusionmat(labels(SVMModel.Partition.test(i)), predicted_labels)))./sum(sum(confusionmat(labels(SVMModel.Partition.test(i)), predicted_labels)))
% end
%

speaker_ids = unique(meta_data(:,1));

conf_mats = {};
for id = speaker_ids(end:-1:1)'
    train_data = sentence_vectors(meta_data(:,1) ~= id,:);
    permutation = randperm(size(train_data,1));
    train_data = train_data(permutation, :);
    train_label = labels(meta_data(:,1) ~= id,:);
    train_label = train_label(permutation);
    SVMModel = fitcsvm(train_data, train_label,...
        'KernelFunction', 'rbf', 'BoxConstraint',z(1,2),...
        'KernelScale',z(1,1));
    %test_model = fitSVMPosterior(SVMModel,train_data(5001:10000,:), train_label(5001:10000,:));
    predicted_labels = predict(SVMModel, sentence_vectors(meta_data(:,1) == id,:));
    conf_mat = confusionmat([0;1;labels(meta_data(:,1) == id,:)], [0;1;predicted_labels]);
    fprintf('id: %d, target: %d, acc: %2.4f, positive: %2.4f\n', id, ...
        mean(labels(meta_data(:,1) == id,:)), (sum(diag(conf_mat))-2)./(sum(sum(conf_mat))-2), ...
        sum(predicted_labels)/length(predicted_labels));
    conf_mats{id,1}.conf_mat = conf_mat - [1,0;0,1];
    conf_mats{id,1}.id = id;
    conf_mats{id,1}.label = mean(labels(meta_data(:,1) == id,:));
    conf_mats{id,1}.predicted_labels = predicted_labels;
end


% [performance, parameters] = find_optimal_params_doc2vec(meta_data, sentence_vectors, 4, 2, 1, [0.01, 0.05, 0.1, 0.2])
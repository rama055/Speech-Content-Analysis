filename='avg_vec.csv';
A=csvread(filename);
sentence_vectors=A(:,5:end-1);

FOC=nan(size(sentence_vectors,1),1);
SOC=nan(size(sentence_vectors,1),1);

for i=1:size(sentence_vectors,1)-1
    if(i==size(sentence_vectors,1)-1 || A(i+2,4)==1)
      X=sentence_vectors(i:i+1,:);
      FOC(i)=pdist(X,'cosine');
    elseif(A(i+1,4)==1)
      %do nothing
    else
      X=sentence_vectors(i:i+1,:);
      FOC(i)=pdist(X,'cosine');
      X(2,:)=sentence_vectors(i+2,:);
      SOC(i)=pdist(X,'cosine');  
    end     
end

% for i = 1: size(FOC,1)
%    if(isnan(FOC(i)))
%        FOC(i)=1;
%    end
% end
% 
% for i = 1: size(SOC,1)
%    if(isnan(SOC(i)))
%        SOC(i)=1;
%    end
% end

sentence_vectors=[sentence_vectors FOC SOC];

%compute avg FOC and SOC for winners and losers
winner_indices=A(:,end)==1;
loser_indices=A(:,end)==0;

[h_f,p_f,ci_f,stats_f]=ttest2(sentence_vectors(winner_indices & A(:,3) == 0,size(sentence_vectors,2)-1),sentence_vectors(loser_indices & A(:,3) == 0,size(sentence_vectors,2)-1))  
[h_s,p_s,ci_s,stats_s]=ttest2(sentence_vectors(winner_indices & A(:,3) == 0,size(sentence_vectors,2)),sentence_vectors(loser_indices & A(:,3) == 0,size(sentence_vectors,2)))

%     
% FOC_avg_winners=sum(sentence_vectors(winner_indices,size(sentence_vectors,2)-1))/size(sentence_vectors,1);
% SOC_avg_winners=sum(sentence_vectors(winner_indices,size(sentence_vectors,2)))/size(sentence_vectors,1);
% FOC_avg_losers=sum(sentence_vectors(loser_indices,size(sentence_vectors,2)-1))/size(sentence_vectors,1);
% SOC_avg_losers=sum(sentence_vectors(loser_indices,size(sentence_vectors,2)))/size(sentence_vectors,1);


% labels=A(:,end);
% 
% % Optimize parameters for SVM
% 
% 
% c = cvpartition(labels, 'kfold', 10);
%  
% minfn = @(z)kfoldLoss(fitcsvm(sentence_vectors, labels, 'CVPartition',c,...
%     'KernelFunction','rbf', 'BoxConstraint',exp(z(2)),...
%     'KernelScale',exp(z(1))));
%   
% opts = optimset('TolX',5e-5,'TolFun',5e-5);
%  
% m = 10;
% fval = zeros(m,1);
% z = zeros(m,2);
% for j = 1:m;
%     [searchmin, fval(j)] = fminsearch(minfn,randn(2,1),opts);
%     %fval(j)
%     z(j,:) = exp(searchmin);
% end
%  
% z = z(fval == min(fval),:);
% 
% %z = [17.2506, 1.2129];
% %%LEAVE ONE DEBATE OUT Validation
% debate_ids = unique(A(:,1));
%  
% conf_mats = {};
% for id = debate_ids(end:-1:1)'
%     train_data = sentence_vectors(A(:,1) ~= id,:);
%     permutation = randperm(size(train_data,1));
%     train_data = train_data(permutation, :);
%     train_label = labels(A(:,1) ~= id,:);
%     train_label = train_label(permutation);
%     SVMModel = fitcsvm(train_data, train_label,...
%         'KernelFunction', 'rbf', 'BoxConstraint',exp(z(2)),...
%         'KernelScale',exp(z(1)));
%     predicted_labels = predict(SVMModel, sentence_vectors(A(:,1) == id,:));
%     conf_mat = confusionmat([0;1;labels(A(:,1) == id,:)], [0;1;predicted_labels]);
%     fprintf('id: %d, target: %d, acc: %2.4f, positive: %2.4f\n', id, ...
%         mean(labels(A(:,1) == id,:)), (sum(diag(conf_mat))-2)./(sum(sum(conf_mat))-2), ...
%         sum(predicted_labels)/length(predicted_labels));
%     conf_mats{id,1}.conf_mat = conf_mat - [1,0;0,1];
%     conf_mats{id,1}.id = id;
%     conf_mats{id,1}.label = mean(labels(A(:,1) == id,:));
%     conf_mats{id,1}.predicted_labels = predicted_labels;
% end
% 
% 

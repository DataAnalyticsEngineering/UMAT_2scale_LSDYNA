data = hdfread('WS_2a.hdf','Not specified');

%%
size(data)
cleaned_data = data;
cleaned_data(cleaned_data<18000)=0;
cleaned_data(cleaned_data>25000)=56633;
X = squeeze(cleaned_data(:,500,:));
imshow(X)

%%
m1=1;
m2=1012;
centers={1012};
radii={1012};
for i=m1:m2
    X = squeeze(cleaned_data(:,i,:));
    [centers{i},radii{i}] = imfindcircles(edge(X,'canny'),[6,65],'ObjectPolarity','bright');
%     imshow(BW)    
%     cla;
%     imshow(X)
%     viscircles(centers{i},radii{i},'EdgeColor','r');
%     pause(1)
end

save

%%
% 
% 
% % [center_img,sphere_img,cent,radi]=SphericalHough(cleaned_data,[6,65],0.2,6,0.5,0.1);
% r=[];
% for i=490:510
%     cc = (centers{i}(:,1)<=500+1) .* (centers{i}(:,1)>=500-1);
%     if sum(cc)
%         [a,b]=max(cc);
%         r(end+1) = radii{i}(b);
%     end
% 
%     
% end
% % 505.8267  440.5143
% plot(r)
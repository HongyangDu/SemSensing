clc;clear;
load scene01_10_28.13
load ../Recode_AmN.mat

Ammax = 1203.844;
x_ori = x_ori.*Ammax;
x_rec = x_rec.*Ammax;


Am_rx_ori = zeros(7,2048,length(x_ori(1,1,:)));
Am_rx_rec = zeros(7,2048,length(x_ori(1,1,:)));

for j = 1:length(x_ori(1,1,:))
    temp = reshape(x_ori(:,:,j),7,2048);
    Am_rx_ori(:,:,j) = temp;
    temp = reshape(x_rec(:,:,j),7,2048);
    Am_rx_rec(:,:,j) = temp;
end
% Am_rx_rec = smoothdata(Am_rx_rec,2,'sgolay',50);
%% For Recover
for i = 1:length(x_ori(1,1,:)) % 时刻
    Am_rx_rec(1,:,i) = Recode_AmN(:,i);
    for j = 1:5 % 天线
        rxtemp1 = Am_rx_rec(j,:,i)+Am_rx_rec(j+1,:,i);
        rxtemp2 = Am_rx_rec(j+1,:,i)+Am_rx_rec(j+2,:,i);
        Am_rx_rec(j+1,:,i) = rxtemp1;
    end
    Am_rx_rec(7,:,i) = Am_rx_rec(6,:,i)+Am_rx_rec(7,:,i);
end

for i = 1:length(x_ori(1,1,:)) % 时刻
    Am_rx_ori(1,:,i) = Recode_AmN(:,i);
    for j = 1:5 % 天线
        rxtemp1 = Am_rx_ori(j,:,i)+Am_rx_ori(j+1,:,i);
        rxtemp2 = Am_rx_ori(j+1,:,i)+Am_rx_ori(j+2,:,i);
        Am_rx_ori(j+1,:,i) = rxtemp1;
    end
    Am_rx_ori(7,:,i) = Am_rx_ori(6,:,i)+Am_rx_ori(7,:,i);
end

Am_rx_rec(Am_rx_rec<0) = 0;
%% Ori Plot
chi = 1;
sizef = 16;
figure
tempori = Am_rx_ori(:,:,chi);
s = surf(tempori,'FaceAlpha',0.8);
% axis([0 2048 1 7 0 1000])
s.EdgeColor = 'none';
Azimuth = 150;
Elevation = 20;
view([Azimuth,Elevation])
ylabel('Antenna');
xlabel('Subcarrier');
zlabel('Magnitude');
view(50,30)
set(gca,'FontSize',sizef,'Fontname','times new Roman');

%% Rec Plot
figure
temprec = Am_rx_rec(:,:,chi);
s = surf(temprec,'FaceAlpha',0.8);
% axis([0 2048 1 7 0 1000])
s.EdgeColor = 'none';
view([Azimuth,Elevation])
ylabel('Antenna');
xlabel('Subcarrier');
zlabel('Magnitude');
view(50,30)
set(gca,'FontSize',sizef,'Fontname','times new Roman');
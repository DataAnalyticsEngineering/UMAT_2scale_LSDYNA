clc
close all;

%----------copper----------
density_cu = @(x) 8.93300e-06 * x.^0;
poisson_ratio_cu = @(x) 3.40000e-01 * x.^0;
conductivity_cu = @(x) 4.20749e+05 * x.^0+-6.84915e+01 * x.^1;
heat_capacity_cu = @(x) 3.16246e+08 * x.^0+3.17858e+05 * x.^1+-3.49795e+02 * x.^2+1.66327e-01 * x.^3;
cte_cu = @(x) 1.28170e-05 * x.^0+8.23091e-09 * x.^1;
elastic_modulus_cu = @(x) max(1.0255e+04, 1.35742e+08 * x.^0+5.85757e+03 * x.^1+-8.16134e+01 * x.^2);
%----------tungsten----------
density_wsc = @(x) 1.93000e-05 * x.^0;
poisson_ratio_wsc = @(x) 2.80000e-01 * x.^0;
conductivity_wsc = @(x) 2.19308e+05 * x.^0+-1.87425e+02 * x.^1+1.05157e-01 * x.^2+-2.01180e-05 * x.^3;
heat_capacity_wsc = @(x) 1.23958e+08 * x.^0+3.44414e+04 * x.^1+-1.25514e+01 * x.^2+2.87070e-03 * x.^3;
cte_wsc = @(x) 5.07893e-06 * x.^0+5.67524e-10 * x.^1;
% elastic_modulus_wsc = @(x) 4.13295e+08 * x.^0+-7.83159e+03 * x.^1+-3.65909e+01 * x.^2+5.48782e-03 * x.^3;
elastic_modulus_wsc = @(x) max(3.5137e+08,4.13295e+08 * x.^0+-7.83159e+03 * x.^1+-3.65909e+01 * x.^2+5.48782e-03 * x.^3);


temp_range = 293:0.5:1500;
e_ratio = zeros(length(temp_range),1);
cond_ratio = zeros(length(temp_range),1);
heat_ratio = zeros(length(temp_range),1);
cte_ratio = zeros(length(temp_range),1);
idx=1;
for temp=temp_range
    e_ratio(idx) = elastic_modulus_wsc(temp)/elastic_modulus_cu(temp);
    cond_ratio(idx) = conductivity_wsc(temp)/conductivity_cu(temp);
    heat_ratio(idx) = heat_capacity_wsc(temp)/heat_capacity_cu(temp);
    cte_ratio(idx) = cte_wsc(temp)/cte_cu(temp);
    
    % for better visualization
    e_ratio(idx) = 1/e_ratio(idx);
    cond_ratio(idx) = 1/cond_ratio(idx);
    heat_ratio(idx) = 1/heat_ratio(idx);
    cte_ratio(idx) = 1/cte_ratio(idx);
    
    idx=idx+1;
end

figure

rng=1:50:length(temp_range);

plot(temp_range,e_ratio,'DisplayName','e\_ratio', 'LineWidth',3)
hold on
scatter(temp_range(rng),e_ratio(rng),'filled')

plot(temp_range,cond_ratio,'DisplayName','cond\_ratio', 'LineWidth',3)
hold on
scatter(temp_range(rng),cond_ratio(rng),'filled')

plot(temp_range,heat_ratio,'DisplayName','heat\_ratio','LineWidth',3)
hold on
scatter(temp_range(rng),heat_ratio(rng),'filled')

plot(temp_range,cte_ratio,'DisplayName','cte\_ratio', 'LineWidth',3)
hold on
scatter(temp_range(rng),cte_ratio(rng),'filled')
grid on
legend('Location','northwest')




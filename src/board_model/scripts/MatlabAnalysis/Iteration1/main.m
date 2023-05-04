T = 100;
X0 = [0 ; 0; 0 ]; % Initial State
v_ref = 2;
prevT = 0;
prevF = 0;
Calldynamics = @(t,X) dynamics(t, X, v_ref);
[t, y] = ode45(Calldynamics, [0,T], X0);


N = length(y)
jerk = []
jerk(1) = 0;
for i = 2 : N
    jerk(i) = (y(i, 3) - y(i - 1, 3))/(t(i) - t(i - 1));
end




subplot(2,2,1);

plot(t,y(:,1));
title('x vs time');

subplot(2,2,2);
plot(t,y(:,2));
title('vel vs time');

subplot(2,2,3);

plot(t,y(:,3));
%title('accelearation vs time');

subplot(2,2,4);

plot(t,jerk);
title('jerk vs time');







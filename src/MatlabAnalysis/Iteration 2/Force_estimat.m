    %Using the LQR values
    K = [0.7071 -106.4988   3.2090  -13.3208]
    m = matfile("Stateresponse.mat");
    m1 = matfile("time.mat");
    t = m1.t;
    x = m.y(:,1);
    theta = m.y(:,2);
    thetadot = m.y(:,4);
    xdot = m.y(:,3)

    %We shall not use Xdes since its values are 0
    F_array =[]
    for i = 1:size(t)
        F_array(i) = K*[x(i) theta(i) xdot(i) thetadot(i)]';

    end

    plot(t, F_array);
    title('t vs Force')
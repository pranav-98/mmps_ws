function [F, Fdot] = pd_control(v, accel, v_ref, t)

% Initializing Kp and Kd values 
%      kp = 30;
%      kd = 5;    
        kp = 4;
        kd = 0.8;


% Defining variables as persistent to store the previous values
    persistent j
    persistent tim
    persistent Farray
    persistent Fdotarray

    if isempty(j)
        j = 0; 
    end
    j = j + 1;
    tim(j) = t;


    Farray(j) = (kp*(v_ref - v) + kd*(accel));
  
    if t == 0
        Fdotarray(j) = 0;  
    else
        delT = tim(j) - tim(j - 1);
        if delT == 0
            Fdotarray(j) = Fdotarray(j - 1);
        else 
                Fdotarray(j) = (Farray(j) - Farray(j - 1))/delT;        
        end 
    end
    F = Farray(j);
    Fdot = Fdotarray(j);
    
end
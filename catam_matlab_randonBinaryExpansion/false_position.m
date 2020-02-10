function [p] = false_position(start,stop,epsilon,h,alpha)
%h=0.001;
%alpha=2;

%validate
if sign(phi(start))*sign(phi(stop))>0
    disp('failed');
    return
end

list_interval=[];
list_p=[];
list_phi=[];
%do-while loop
while 1
  p=(phi(stop)*start-phi(start)*stop)/(phi(stop)-phi(start));
  ph=phi(p);
  list_p=[list_p; stringfy(p)];
  list_interval=[list_interval;[stringfy(start) stringfy(stop)]];
  list_phi=[list_phi;stringfy(ph)];
  if abs(ph)<epsilon
      break;
  end
  
  if sign(p)==sign(start)
      start=p;
  else
      stop=p;
  end
  
end

dim=size(list_p);


tb=table((1:dim(1)).',list_interval,list_p,list_phi);
vars={'Number of steps n','interval','estimates of p','phi(p)'};
tb.Properties.VariableNames = vars;
 %plot table
fig= uifigure('Name','res');
uit = uitable(fig,'Data',tb);



function [out]=phi(p)
    t=rk4_2d(1,h,p,alpha).';
    out=t(end-1);
end
function [out]=stringfy(in)
    out=string(in);
    for i=1:length(in)
        out(i) = sprintf('%.8f',in(i));
    end
    
end
end

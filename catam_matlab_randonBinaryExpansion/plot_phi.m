step=1;
start=0;
stop=70;
X = start:step:stop;

f = arrayfun(@phi,X);

plot(X,f,'-x');
hold on;
plot([start,stop],[0,0],'-');
hold off;
xlabel('p') ;
ylabel('phi(p)') ;
xticks((0:5:70));

function [out]=phi(p)
    t=rk4_2d(1,0.001,p,10).';
    out=t(end-1);
end

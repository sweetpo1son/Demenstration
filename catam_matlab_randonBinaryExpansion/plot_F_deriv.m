%a script to estimate and plot the density function

n=14;
h=2.^n;
p=0.5;
c=51/128;
delt_left=2.^-9;
delt_right=2.^-9;

list_delt=(-delt_left:(1/h):delt_right);
list_deriv=zeros(1,length(list_delt));

counter=1;
Fc=F(c*h,p,n);
for k=(-delt_left):(1/h):(delt_right)
    list_deriv(counter)=(F((c+k)*h,p,n)-Fc)/k;
    counter=counter+1;
end

plot(list_delt,list_deriv,'DisplayName','c=, p=');
     ylabel('(F(c+\delta)-F(c))/\delta');
     xlabel('\delta') ;
     legend;

function [out]=F(x,p,n)
        binary=de2bi(x);
        str=flip(cat(2,binary,zeros(1,n-length(binary))));
        q=1-p;
        prod=1;
        out=0;
        for m=1:n
            x_i=str(m);
            out=out+q*x_i*prod;
            prod=prod*(p.^x_i)*(q.^(1-x_i));
        end      
    end

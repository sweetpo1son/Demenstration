%numerical solution

function [] = analytic(p,n)
    list_F=zeros(1,(2^n)+1);
    list_x=(0:2^(-n):1);
    for k=0:2^n
       list_F(k+1)=F(k,p);
    end
    list_F(end)=1;
     plot(list_x,list_F,'DisplayName','Question 2');
     hold on;
     xlabel('x');
     ylabel('F(x)') ;

    function [out]=F(x,p)
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
end

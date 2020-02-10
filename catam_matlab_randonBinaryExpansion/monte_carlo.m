%Monte Carlo Method to estimate distribution function
function [] = monte_carlo(p,n,N)
    %step=10^-6;
    step=2^-11;
    density=zeros(1,(1/step)+1);
    for m=1:N
        X_m=0;
        for k=1:n
            X_m=X_m+binornd(1,p)*(2.^(-k));
        end
        ind=ceil(X_m/step)+1;
        density(ind)=density(ind)+1;
        
        
    end
    
    cumulative=cumsum(density)/N;
    plot((0:step:1),cumulative,'DisplayName','Question 1');
    hold off;
    xlabel('x');
    ylabel('F(x)') ;
    legend('Location','northwest');
end

roots=find_roots([12 13;26 27;39 40;53 54;66 67]);

for k=1:5
    step_len=0.001;
    t=rk4_2d(1,step_len,roots(k),10);
    y_k=t(:,1).';
    list_x=(0:step_len:1);
    f=@(x) (1+x).^(-10);
    temp=arrayfun(f,list_x);
    const=0.001*trapz(temp.*y_k*roots(k));
    y_k_normal=y_k/const;
    switch k
        case 1
            figure(1);
            plot(list_x,y_k_normal,'DisplayName','p^{(1)}');
            hold on;
        case 2
            plot(list_x,y_k_normal,'--','DisplayName','p^{(2)}');
            hold on;
        case 3
            plot(list_x,y_k_normal,':k','DisplayName','p^{(3)}');
            hold off;
            legend;
            xlabel('x') ;
            ylabel('y^k(x)') ;
        case 4
            figure(2);
            plot(list_x,y_k_normal,'DisplayName','p^{(4)}');
            hold on;
        otherwise
            plot(list_x,y_k_normal,'--','DisplayName','p^{(5)}');
            hold off;
            legend;
            xlabel('x') ;
            ylabel('y^k(x)') ;            
    end
    

    
end
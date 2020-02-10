function [out]=stringfy(in)
    out=string(in);
    for i=1:length(in)
        out(i) = sprintf('%.8f',in(i));
    end
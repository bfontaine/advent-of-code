# Advent of code 2021

## Code-golf’d AWK solutions

```awk
# day 1, problem 1
{if($1>p)n++;p=$1}END{print n-1}
# day 1, problem 2
{c++;b[c%4]=$0;n+=(c>3&&$0>b[(c+1)%4])}END{print n}
# day 2, problem 1
/f/{h+=$2}/u/{d-=$2}/n/{d+=$2}END{print h*d}
# day 2, problem 2
/n/{a+=$2}/u/{a-=$2}/f/{h+=$2;d+=a*$2}END{print h*d}
# day 3, problem 1
{split($0,s,X);for(i=1;i<=length($0);)b[i]+=s[i++]*2-1}END{for(i in b){x=b[i]>0;g=g*2+x;e=e*2+!x}print g*e}
# day 3, problem 2
function r(N,D){i=1;for(s=length(N);s>1;){n=0;for(j=1;j<=s;){n+=substr(N[j++],i,1)*2-1};b=n?D==(n>0):D;S=0;for(j=1;j<=s;j++){if(substr(N[j],i,1)==b){N[S+1]=N[j];S++}};s=S;i++}d=0;split(N[1],B,X);for(j in B){d=d*2+B[j]}return d}{y[i+1]=x[i+1]=$0;i++}END{print r(x,1)*r(y,0)}
```
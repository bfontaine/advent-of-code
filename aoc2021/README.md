# Advent of code 2021

## Code-golf’d AWK solutions

```awk
# day 1, problem 1
{if($1>p)n++;p=$1}END{print n-1}
# day 1, problem 2
{b[++c%4]=$0;n+=(c>3&&$0>b[(c+1)%4])}END{print n}
# day 2, problem 1
/f/{h+=$2}/u/{d-=$2}/n/{d+=$2}END{print h*d}
# day 2, problem 2
/n/{a+=$2}/u/{a-=$2}/f/{h+=$2;d+=a*$2}END{print h*d}
# day 3, problem 1
{l=split($0,s,X);for(i=1;i<=l;)b[i]+=s[i++]*2-1}END{for(i in b){x=b[i]>0;g=g*2+x;e=e*2+!x}print g*e}
# day 3, problem 2
function r(N,D){i=1;for(s=J;s>1;){n=0;for(j=1;j<=s;){n+=substr(N[j++],i,1)*2-1};b=n?D==(n>0):D;S=0;for(j=1;j<=s;j++){if(substr(N[j],i,1)==b){N[S+1]=N[j];S++}};s=S;i++}d=0;split(N[1],B,X);for(j in B){d=d*2+B[j]}return d}{y[J+1]=x[++J]=$0}END{print r(x,1)*r(y,0)}
# day 5, problem 1
{split($0,A,",| ");x=A[1];y=A[2];a=A[4];b=A[5];X=x==a;Y=y==b;k=X||Y;while(k){n+=g[x" "y]++==1;x==a&&y==b?k=0:0;X?0:x+=(a<x?-1:1);Y?0:y+=(b<y?-1:1)}}END{print n}
# day 5, problem 2
{split($0,A,",| ");x=A[1];y=A[2];a=A[4];b=A[5];while(1){n+=g[x" "y]++==1;if(x==a&&y==b)next;x==a?0:x+=(a<x?-1:1);y==b?0:y+=(b<y?-1:1)}}END{print n}
# day 6, problem 1
{l=split($0,s,",");for(;d++<80;)for(i in s)s[i]?s[i]--:s[i]=(s[++l]=8)-2;print l}
# day 6, problem 2
{t=split($0,s,",");for(i in s){S[s[i]]++};for(d=0;d<256;d++){S[7]+=N=S[0];S[0]=0;for(i=1;i<9;i++){S[i-1]=S[i];S[i]=0};t+=S[8]=N}print t}
```

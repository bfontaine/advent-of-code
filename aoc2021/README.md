# Advent of code 2021

## Code-golf’d AWK solutions

```awk
# day 1, problem 1
p<(p=$1){n++}END{print n-1}
# day 1, problem 2
{n+=((b[++c%4]=$0)>b[(c+1)%4]&&c>3)}END{print n}
# day 2, problem 1
/f/{h+=$2}/u/{d-=$2}/n/{d+=$2}END{print h*d}
# day 2, problem 2
/n/{a+=$2}/u/{a-=$2}/f/{h+=$2;d+=a*$2}END{print h*d}
# day 3, problem 1
{l=split($0,s,X);for(i=1;i<=l;)b[i]+=s[i++]*2-1}END{for(i in b){x=b[i]>0;g=g*2+x;e=e*2+!x}print g*e}
# day 3, problem 2
function r(N,D){i=1;for(s=J;s>1;){n=0;for(j=1;j<=s;)n+=substr(N[j++],i,1)*2-1;b=n?D==(n>0):D;S=0;for(j=1;j<=s;j++)substr(N[j],i,1)==b?N[++S]=N[j]:0;s=S;i++}d=0;split(N[1],B,X);for(j in B)d=d*2+B[j];return d}{y[J+1]=x[++J]=$0}END{print r(x,1)*r(y,0)}
# day 5, problem 1
{split($0,A,",| ");x=A[1];y=A[2];a=A[4];b=A[5];X=x==a;Y=y==b;k=X||Y;while(k){n+=g[x" "y]++==1;x==a&&y==b?k=0:0;X?0:x+=(a>x)*2-1;Y?0:y+=(b>y)*2-1}}END{print n}
# day 5, problem 2
{split($0,A,",| ");x=A[1];y=A[2];a=A[4];b=A[5];while(1){n+=g[x" "y]++==1;if(x==a&&y==b)next;x==a?0:x+=(a<x?-1:1);y==b?0:y+=(b<y?-1:1)}}END{print n}
# day 6, problem 1
{l=split($0,s,",");for(;d++<80;)for(i in s)s[i]?s[i]--:s[i]=(s[++l]=8)-2;print l}
# day 6, problem 2
{t=split($0,s,",");for(i in s){S[s[i]]++}for(d=0;d<256;d++){S[7]+=N=S[0];for(i=0;i<9;i++){S[i-1]=S[i];S[i]=0}t+=S[8]=N}print t}
# day 7, problem 1
{l=split($0,c,",");asort(c);for(i in c)f+=sqrt((c[i]-(l%2?c[(l+1)/2]:(c[l/2]+c[l/2+1])/2))^2);print f}
# day 7, problem 2
{split($0,C,",");for(i in C)m=C[i]>m?C[i]:m;for(;x++<=m;){s=0;for(i in C)s+=(n=(n=C[i]-x)<0?-n:n)*(n+1);!b||s<b?b=s:0}print b/2}
# day 8, problem 1
{for(i=NF-3;i<=NF;i++)n+=(l=length($i))>1&&l<5||l==7}END{print n}
# day 9, problem 1
{l=split($0,R,X);for(i=1;i<=l;i++){G[i" "NR]=R[i]+1}}END{for(y=1;y<=FNR;y++)for(x=1;x<=l;x++){h=G[x" "y];o=1;for(z=y-1;z<y+2;z++)for(w=x-1;w<x+2;w++)(j=G[w" "z])&&(w!=x||z!=y)&&j<=h?o=0:0;S+=h*o}print S}
# day 9, problem 2
{l=split($0,R,"");for(i=1;i<=l;i++)if(R[i]>8)S[i]=0;else{T=S[i];if(L=S[i-1]){if(T&&T!=L){B[T]+=B[L]+1;B[L]=0;for(j=i;S[j];)S[j--]=T}else B[S[i]=L]++}else T?B[T]++:B[S[i]=++N]++}}END{asort(B);print B[l=length(B)]*B[l-1]*B[l-2]}
```

# Advent of code 2021

## Code-golf’d AWK solutions

Here are only the solutions that would fit in a tweet (≤280 characters).

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
{for(i=12;i<16;i++)n+=(l=length($i))>1&&l<5||l==7}END{print n}
# day 9, problem 1
{split($0,R,X);for(i in R){G[i" "NR]=R[i]+1}}END{for(y=1;y<=FNR;y++)for(x in R){h=G[x" "y];o=1;for(z=y-1;z<y+2;z++)for(w=x-1;w<x+2;w++)(j=G[w" "z])&&(w!=x||z!=y)&&j<=h?o=0:0;S+=h*o}print S}
# day 9, problem 2
{split($0,R,X);for(i in R)R[i]>8?S[i]=0:(1+(T=S[i])&&(L=S[i-1])&&++B[S[i]=L])?((T&&T!=L&&B[L]+=B[T])?B[T]=0:0):T?B[T]++:B[S[i]=++N]++}END{asort(B);print B[l=length(B)]*B[l-1]*B[l-2]}
# day 10, problem 1
{T=s=0;E["("]=")";E["{"]="}";E["["]="]";E["<"]=">";split($0,L,X);for(i in L)if(e=E[c=L[i]])S[++T]=e;else if(S[T--]!=c){C+=c==")"?3:c=="]"?57:c=="}"?1197:25137;next}}END{print C}
# day 10, problem 2
{T=s=0;E["("]=")";E["{"]="}";E["["]="]";E["<"]=">";split($0,L,X);for(i in L)if(e=E[c=L[i]])S[++T]=e;else if(S[T--]!=c)next;for(i=T;i;)s=s*5+index(")]}>",S[i--]);C[++N]=s}END{asort(C);print C[(N+1)/2]}
# day 11, problem 1
{W=split($0,r,X);for(i in r)G[i,NR]=r[i]}END{for(;s++<100;){for(c in G)G[c]++;split(X,F,X);T=1;while(T){;T=0;for(y=1;y<=NR;y++)for(x=1;x<=W;x++)if(!((x,y)in F)&&G[x,y]>9){F[x,y]=T=++H;for(Y=y-1;Y<y+2;Y++)for(X=x-1;X<x+2;)G[X++,Y]++}}for(c in F)G[c]=0}print H}
# day 12, problem 1
function f(n,v,N,s){if(n=="end")R=1;else{S[n]?v=v V n V:0;split(E[n],N,V);for(i in N)if(n!=(m=N[i])&&m&&!index(v,V m V)){f(m,v);s+=R}R=s}}{V="-";split($0,N,V);for(i in N){S[n]=tolower(n=N[i])==n;E[n]=E[n]V N[1]V N[2]V}}END{f("start");print R}
# day 13, problem 1
/,/{G[$0]}/=/{if(++F<2){split($3,A,"=");a=A[1]=="x";for(s in G){split(s,X,",");x=X[1];y=X[2];x>(v=A[2])&&a?x=2*v-x:!a&&y>v?y=2*v-y:0;G[s]=0;G[x","y]=1}for(s in G)N+=G[s];print N}}
# day 13, problem 2
/,/{G[$0]}/=/{split($3,A,"=");V=A[2];for(s in G){G[s]=0;split(s,C,",");x=C[1];y=C[2];A[1]=="x"?(x>(M=V)?x=2*V-x:0):y>(N=V)?y=2*V-y:0;G[x","y]=1}}END{for(z=0;z<=N;z++){for(x=0;x<=M;)printf G[x++","z]?"#":FS;print""}}
# day 14, problems 1 and 2: too long
# day 15, problem 1
{split($0,R,X);NR<2?R[1]=-1:0;for(i in R){f=S[i-1];S[i]=((t=S[i])&&t<f?t:f?f:t)+R[i]}}END{print S[i]+1}
# day 15, problem 2: too long
# day 22, problem 1
{W=2501;split($2,P,"[.,xyz=]+");for(x=P[2];x<=P[3]&&x**2<W;x++)for(y=P[4];y<=P[5]&&y**2<W;y++)for(z=P[6];z<=P[7]&&z**2<W;z++)if(C[x,y,z]||$1!="on")delete C[x,y,z]}END{print length(C)}
```

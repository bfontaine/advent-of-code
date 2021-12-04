# Code-golf’d:
# {split($0,s,"");for(i=1;i<=length($0);i++)b[i]+=s[i]*2-1}END{for(i in b){x=b[i]>0;g=g*2+x;e=e*2+!x;}print g*e}
{
  split($0, s, "")
  for (i=1; i <= length($0); i++) {
    # 1: +1, 0: -1
    bits[i]+= s[i] * 2 - 1;
  }
}
END {
  for (i in bits) {
    x = (bits[i] > 0)
    g = g * 2 + x
    e = e * 2 + !x
  }
  print g * e
}

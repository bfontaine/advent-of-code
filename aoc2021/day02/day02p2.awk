/down/ { a+=$2 }
/up/ { a-=$2 }
/forward/ { h+=$2;d+=a*$2 }
END { print h*d }

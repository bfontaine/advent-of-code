{
        cur++
        # circular buffer of size 4
        buf[cur % 4] = $0
        # A A A
        #   B B B
        # 1 2 3 4
        #
        # [cur-3]+[cur-2]+[cur-1] < [cur-2]+[cur-1]+[cur]
        # is equivalent to:
        # [cur-3] < [cur]
        # Since the buffer is circular with size 4, cur-3 = (cur-3+4)%4 = (cur+1)%4
        if (cur > 3 && $0 > buf[(cur+1)%4]) {
                count++
        }
}
END {
        print count
}

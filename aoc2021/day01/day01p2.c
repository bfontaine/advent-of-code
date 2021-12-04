#include <stdio.h>

#define SIZE 4
#define INDEX(i) ((i+SIZE)%SIZE)

int main(int argc, char **argv) {
        int count = 0;
        // circular buffer
        int buf[SIZE];
        int cur = 0;

        while (scanf("%d", &buf[INDEX(cur)]) > 0) {
                //printf("[%d]= %d\n", cur, buf[INDEX(cur)]);

                // 1 2 3 4
                // A A A
                //   B B B
                //
                // [1]+[2]+[3] > [2]+[3]+[4]
                // is equivalent to:
                // [1] > [4]
                if (cur > 2 && buf[INDEX(cur)] > buf[INDEX(cur-3)]) {
                        count++;
                }

                cur++;
        }

        printf("%d\n", count);

        return 0;
}

#include <stdio.h>
#include <unistd.h>

int main(int n) {
    printf("Hello, World!  number = %d\n",n);

    pid_t pid = fork();

    if (pid == 0){
        printf("From child ID is : %d \n",getpid());
    }
    else{
        printf("From parent ID is : %d  child ID is : %d\n",getpid(),pid);
    }

    return 0;
}

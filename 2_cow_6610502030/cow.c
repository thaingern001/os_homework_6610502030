#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

size_t get_rss_kb(pid_t pid){
    char p[64]; snprintf(p,sizeof(p),"/proc/%d/status",pid);
    FILE* f=fopen(p,"r"); if(!f) return 0;
    char line[256]; size_t rss=0;
    while(fgets(line,sizeof(line),f)){
        if(strncmp(line,"VmRSS:",6)==0){ sscanf(line+6,"%zu",&rss); break; }
    }
    fclose(f); return rss; // in kB
}

int main(int argc, char** argv){
    size_t meg = (argc>1)? strtoull(argv[1],NULL,10): 50; // MB
    size_t bytes = meg * 1024ull * 1024ull;
    size_t pagesz = sysconf(_SC_PAGESIZE);

    uint8_t* buf = malloc(bytes);
    if( !buf ){ 
        perror("malloc"); 
        return 1; 
    }

    for (size_t i=0; i<bytes; i+=pagesz){
         (void)buf[i]; 
    }

    pid_t pid = fork();
    if(pid<0){ 
        perror("fork"); 
        return 1; 
    }

    if(pid==0){
        // child: วัดก่อนเขียน
        printf("[child] init VmRSS(kB)=%zu\n", get_rss_kb(getpid()));

        // เขียนแตะหน้า (write-touch) ตามสัดส่วนที่กำหนด
        double frac = (argc>2)? atof(argv[2]): 1.0; // 0.0..1.0
        size_t to_touch = (size_t)(bytes*frac);
        for(size_t i=0;i<to_touch;i+=pagesz){ 
            buf[i]= (uint8_t)(i); 
        }

        printf("[child] after write %.0f%% VmRSS(kB)=%zu\n", frac*100.0, get_rss_kb(getpid()));
        // delaay
        struct timespec ts={0,200*1000*1000}; nanosleep(&ts,NULL);
        return 0;
    }else{
        // parent: วัดรอบ ๆ child
        printf("[parent] before wait VmRSS(kB)=%zu\n", get_rss_kb(getpid()));
        int st=0; waitpid(pid,&st,0);
        printf("[parent] after wait VmRSS(kB)=%zu\n", get_rss_kb(getpid()));
    }
    return 0;
}

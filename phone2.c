#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>


int main(int argc, char** argv){

    int N = 10000;

    unsigned char data[N];
    int ss = socket(PF_INET, SOCK_STREAM, 0);
    int s;

    int mode = -1;
    

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    char *e;
    long port = strtol(argv[1], &e, 10);
    if(*e == '.'){
        mode = 2;
        port = strtol(argv[2], &e, 10);
        if(*e != '\0'){
            fprintf(stderr, "%s:  irregular character found %s\n", argv[2], e);
            exit(1);
        }
    }else if(*e != '\0'){
        fprintf(stderr, "%s:  irregular character found %s\n", argv[2], e);
        exit(1);
    }else{
        mode = 1;
    }

    char mode_list[2][10] = {"sever", "client"};
    printf("%s mode\n", mode_list[mode-1]);


    if(mode == 1){
        //server

        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);
        if(bind(ss, (struct sockaddr *)&addr, sizeof(addr)) == -1){perror("bind"); exit(1);}
        if(listen(ss, 10) == -1){perror("listen"); exit(1);}

        struct sockaddr_in client_addr;
        socklen_t len = sizeof(struct sockaddr_in);
        s = accept(ss, (struct sockaddr*)&client_addr, &len);
        if(s == -1){perror("accept"); exit(1);}
        close(ss);

    }else if(mode == 2){
        //client
        if(inet_aton(argv[1], &addr.sin_addr) == 0){perror("ip is wrong"); exit(1);}
        addr.sin_port = htons(port);
        int ret = connect(ss, (struct sockaddr *)&addr, sizeof(addr));
        if(ret == -1){
            perror("connect");
            exit(1);
        }
        s = ss;

    }else{fprintf(stderr, "argv is wrong");exit(1);}
    



    FILE* fp1;
    FILE* fp2;
    char* cmdline1 = "rec -t raw -b 16 -c 1 -e s -r 48000 -";
    char* cmdline2 = "play -t raw -b 16 -c 1 -e s -r 48000 -";
    if((fp1=popen(cmdline1, "r")) == NULL){perror ("popen"); exit(1);}
    if((fp2=popen(cmdline2, "w")) == NULL){perror ("popen"); exit(1);}

    int n = 0;
    int fd = open("input1.raw", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    int fd2 = open("input2.raw", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    while((n = fread(data, sizeof(unsigned char), N, fp1)) > 0){
        //send
        n = send(s, data, n, 0);
        if (n == -1){perror("send"); exit(1);}
        write(fd, data, n);
        //recv
        n = recv(s, data, N, 0);
        if (n == -1){perror("recv"); exit(1);}
        if(fwrite(data, sizeof(unsigned char), n, fp2) < 0){perror("fwrite"); exit(1);}
        write(fd2, data, n);
    }
    pclose(fp1);
    pclose(fp2);
    close(s);
    // gcc phone2.c -o phone 
    //server: ./phone 50000 | play -t raw -b 16 -c 1 -e s -r 48000 -
    //client: rec -t raw -b 16 -c 1 -e s -r 48000 - | ./phone 127.0.0.1 50000 | play -t raw -b 16 -c 1 -e s -r 48000 -
    //俺: 192.168.100.12
    //IZUME: 192.168.100.35
}

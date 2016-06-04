#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <signal.h>

#define PORT "5555"

int main(){
    // 1. get addrinfo
    int sockfd; 
    struct addrinfo hint, *res, *p; 
    memset(&hint, sizeof(hint), 0); 

    hint.ai_family = AF_UNSPEC;
    hint.ai_flags = AI_PASSIVE; 
    hint.ai_socktype = SOCK_DGRAM; 

    if (getaddrinfo(NULL, PORT, &hint, &res) != 0) {
        printf("ERROR\n"); 
    }

    // 2. create socket 
    for (p = res; p != NULL; p = p->ai_next) {
       sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol); 
      if (sockfd == -1){
          continue; 
      }
      printf("Created socket");  
      break;
    }

    freeaddrinfo(res); 


    // 3. bind socket to a port and address
    // handle
}

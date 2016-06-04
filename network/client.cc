#include <sys/socket.h>
#include <sys/types.h>

int main() {
    int sockfd; 
    struct addrinfo hint; 
    memset(&hint, sizeof(hint), 0); 
    hint.ai_family = AI_UNSPEC; 
    hint.ai_addr = AI_PASSIVE; 
    hint.ai_socktype = SOCK_DGRAM; 
    // create socket 
    //
    // sendto
    return 0; 
}

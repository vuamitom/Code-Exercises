#include <string.h>
#include <event2/event.h>
#include <event2/listener.h>
#include <event2/bufferevent.h>
#include <event2/buffer.h>


static const int PORT = 9995;
static const char MESSAGE[] = "Hello, World!\n";

static void
conn_writecb(struct bufferevent *bev, void *user_data)
{
	struct evbuffer *output = bufferevent_get_output(bev);
	if (evbuffer_get_length(output) == 0) {
		printf("flushed answer\n");
		bufferevent_free(bev);
	}
}

static void
conn_eventcb(struct bufferevent *bev, short events, void *user_data)
{
	if (events & BEV_EVENT_EOF) {
		printf("Connection closed.\n");
	} else if (events & BEV_EVENT_ERROR) {
		printf("Got an error on the connection: %s\n",
		    strerror(errno));/*XXX win32*/
	}
	/* None of the other events can happen here, since we haven't enabled
	 * timeouts */
	bufferevent_free(bev);
}


static void
listener_cb(struct evconnlistener *listener, evutil_socket_t fd,
    struct sockaddr *sa, int socklen, void *user_data)
{
	struct event_base *base = (event_base *)user_data;
	struct bufferevent *bev;

	bev = bufferevent_socket_new(base, fd, BEV_OPT_CLOSE_ON_FREE);
	if (!bev) {
		fprintf(stderr, "Error constructing bufferevent!");
		event_base_loopbreak(base);
		return;
	}
	bufferevent_setcb(bev, NULL, conn_writecb, conn_eventcb, NULL);
	bufferevent_enable(bev, EV_WRITE);
	bufferevent_disable(bev, EV_READ);
	bufferevent_write(bev, MESSAGE, strlen(MESSAGE));
}


int main(int argc, char *argv[]) {

	struct event_base *base;
	struct evconnlistener *listener;
	struct sockaddr_in sin;

	base = event_base_new();
	if (!base) {
		fprintf(stderr, "Could not initialize libevent!\n");
		return 1;
	}

	memset(&sin, 0, sizeof(sin));
	sin.sin_family = AF_INET;
	sin.sin_port = htons(PORT);

	// create server socket manually
	// to make this code works with other frameworks which 
	// we don't open socket by ourselves.
	int reuseaddr_on = 1;
	int server_socket;
	server_socket = socket(AF_INET, SOCK_STREAM , 0);
	if (server_socket < 0) {
		fprintf(stderr, "Could not open socket!\n");
		return 1;
	}

	if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR | SO_KEEPALIVE, &reuseaddr_on, 
		sizeof(reuseaddr_on)) < 0) {
		fprintf(stderr, "setsockopt failed");
		goto err;
	}

	if (evutil_make_socket_nonblocking(server_socket) < 0) {
		fprintf(stderr, "set nonblocking failed");
		goto err;
	}

	if (bind(server_socket, (struct sockaddr *)&sin,
		sizeof(sin)) < 0) {
		fprintf(stderr, "bind failed\n");
		goto err;
	}
	
	// add libevent connection listener
	listener = evconnlistener_new(base, listener_cb, (void *)base,
	    LEV_OPT_REUSEABLE|LEV_OPT_CLOSE_ON_FREE, -1,
	    server_socket);

	if (!listener) {
		fprintf(stderr, "Could not create a listener!\n");
		goto err;
	}
	// signal_event = evsignal_new(base, SIGINT, signal_cb, (void *)base);
	// if (!signal_event || event_add(signal_event, NULL)<0) {
	// 	fprintf(stderr, "Could not create/add a signal event!\n");
	// 	return 1;
	// }

	event_base_dispatch(base);
	evconnlistener_free(listener);
	// event_free(signal_event);
	event_base_free(base);
	printf("done\n");
	return 0;
err:
	evutil_closesocket(server_socket);
	return 1;
}


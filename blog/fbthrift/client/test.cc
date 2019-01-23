#include <stdio.h>
#include <glog/logging.h>
#include <folly/init/Init.h>
#include <folly/portability/GFlags.h>
#include <thrift/lib/cpp2/server/ThriftServer.h>
#include <folly/futures/Future.h>
#include <folly/synchronization/Baton.h>
#include <thrift/lib/cpp/async/TAsyncSocket.h>
#include <thrift/lib/cpp2/async/HeaderClientChannel.h>
#include <thrift/lib/cpp2/async/RocketClientChannel.h>
#include <thrift/lib/cpp2/async/RSocketClientChannel.h>
#include "../ExampleHandler.h"


using apache::thrift::ThriftServer;
using apache::thrift::ThriftServerAsyncProcessorFactory;
using apache::thrift::RequestCallback;
using apache::thrift::ClientReceiveState;
using apache::thrift::HeaderClientChannel;
using apache::thrift::RocketClientChannel;
using apache::thrift::RSocketClientChannel;
using apache::thrift::async::TAsyncSocket;
using tamvm::cpp2::ExampleHandler;
using tamvm::cpp2::ExampleServiceAsyncClient;

constexpr std::int32_t thrift_port = 12999;

TAsyncSocket::UniquePtr getSocket(
    folly::EventBase* evb,
    folly::SocketAddress const& addr,
    std::list<std::string> advertizedProtocols = {}) {
  TAsyncSocket::UniquePtr sock(new TAsyncSocket(evb, addr));
  sock->setZeroCopy(true);
  return sock;
}

static std::unique_ptr<ExampleServiceAsyncClient> newHeaderClient(
    folly::EventBase* evb,
    folly::SocketAddress const& addr) {
  auto sock = getSocket(evb, addr);
  auto chan = HeaderClientChannel::newChannel(std::move(sock));
  chan->setProtocolId(apache::thrift::protocol::T_BINARY_PROTOCOL);
  return std::make_unique<ExampleServiceAsyncClient>(std::move(chan));
}

// static std::unique_ptr<ExampleServiceAsyncClient> newRocketClient(
//     folly::EventBase* evb,
//     folly::SocketAddress const& addr) {
//   // auto sock = getSocket(evb, addr, {"rs2"});
// TAsyncSocket::UniquePtr sock(new TAsyncSocket(evb, addr));
//   auto channel = RocketClientChannel::newChannel(sock);
//   channel->setProtocolId(apache::thrift::protocol::T_COMPACT_PROTOCOL);
//   return std::make_unique<ExampleServiceAsyncClient>(std::move(channel));
// }

std::unique_ptr<ThriftServer> newServer(folly::SocketAddress const&addr) {
  auto handler = std::make_shared<ExampleHandler>();
  auto proc_factory =
      std::make_shared<ThriftServerAsyncProcessorFactory<ExampleHandler>>(
          handler);
  auto server = std::make_unique<ThriftServer>();
  server->setAddress(addr);
  server->setProcessorFactory(proc_factory);
  return server;
}

class TestAsyncCallback : public apache::thrift::RequestCallback {
	void requestSent() override {
 		LOG(INFO) << "client: requestSent";
 	}

	void replyReceived(ClientReceiveState&& state) override {
		LOG(INFO) << "client: replyReceived";
	}

	void requestError(ClientReceiveState&& state) override {
		LOG(ERROR) << "client: requestError";		
	}
};

class AsyncCallback : public apache::thrift::RequestCallback {
 public:
 	AsyncCallback(ClientReceiveState* result, folly::Baton<>* baton)
 		: result_(result), baton_(baton) {}
 	void requestSent() override {
 		LOG(INFO) << "client: requestSent";
 	}

	void replyReceived(ClientReceiveState&& state) override {
		LOG(INFO) << "client: replyReceived";
		*result_ = std::move(state);
		baton_->post();
	}

	void requestError(ClientReceiveState&& state) override {
		LOG(ERROR) << "client: requestError";		
		*result_ = std::move(state);
		LOG(ERROR) << "exception: " << result_->exception();
		baton_->post();
	}
  private:
  	folly::Baton<>* baton_;
  	ClientReceiveState* result_;
};

void test(ClientReceiveState* result, folly::Baton<>* baton) {

	folly::EventBase eb;
	folly::SocketAddress addr("::1", thrift_port);
	auto client = newHeaderClient(&eb, addr);
	LOG(INFO) << "client sending...";
	auto r = client->sync_get_number(1113);
	LOG(INFO) << "result " << r;
	auto fut = client->future_get_number(1114);
	std::move(fut).thenValue([](int32_t val) {
		LOG(INFO) << "callback: " << val;
	});
	auto cb = std::make_unique<AsyncCallback>(result, baton);
	client->get_number(std::move(cb), 1116);
}

int main(int argc, char *argv[]) {
	LOG(INFO) << "Starting test ...";
	FLAGS_logtostderr = 1;
	
	folly::init(&argc, &argv);
	
	folly::EventBase eb;
	folly::SocketAddress addr("::1", thrift_port);
	auto client = newHeaderClient(&eb, addr);
	// LOG(INFO) << "client sending...";
	// auto r = client->sync_get_number(13);
	// LOG(INFO) << "result " << r;

	ClientReceiveState result;
	folly::Baton<> baton;
	
	// auto client = newHeaderClient(&eb, addr);
	// LOG(INFO) << "client sending...";
	// r = client->sync_get_number(1113);
	// LOG(INFO) << "result " << r;
	auto fut = client->future_get_number(4112);
	int32_t count = 2;
	std::move(fut).thenValue([&eb, &count](int32_t val) {
		LOG(INFO) << "callback: " << val;
		eb.terminateLoopSoon();
	});
	// fut = client->future_get_number(4114);	
	// std::move(fut).thenValue([&eb, &count](int32_t val) {
	// 	LOG(INFO) << "callback: " << val;
	// 	eb.terminateLoopSoon();
	// });
	// auto cb = std::make_unique<AsyncCallback>(&result, &baton);
	// client->get_number(std::move(cb), 1116);
	eb.loopForever();

	// std::thread client_thread([]() {
	//     // LOG(INFO) << "ChatRoom Server running on port: " << FLAGS_chatroom_port;
	// 	folly::EventBase eb;
	// 	folly::SocketAddress addr("::1", thrift_port);
	// 	auto client = newHeaderClient(&eb, addr);
	// 	// LOG(INFO) << "client sending...";
	// 	// auto r = client->sync_get_number(1213);
	// 	// LOG(INFO) << "result " << r;

		
		
	// 	// auto client = newHeaderClient(&eb, addr);
	// 	// LOG(INFO) << "client sending...";
	// 	// r = client->sync_get_number(1113);
	// 	// LOG(INFO) << "result " << r;
	// 	auto fut = client->future_get_number(3114);
	// 	auto futN = std::move(fut).thenValue([&eb](int32_t val) {
	// 		LOG(INFO) << "callback: " << val;
	// 		eb.terminateLoopSoon();
	// 		LOG(INFO) << "done terminateLoopSoon";
	// 	});    
	// 	// ClientReceiveState result;
	// 	// folly::Baton<> baton;
	// 	// auto cb = std::make_unique<AsyncCallback>(&result, &baton);
	// 	// client->get_number(std::move(cb), 1116);
	// 	eb.loopForever();
	// });
	// client_thread.detach();
	// baton.wait();
	// eb.loopForever();
	// auto fut = client->future_get_number(16);
	// std::move(fut).thenValue([](int32_t val) {
	// 	LOG(INFO) << "callback: " << val;
	// });
	// std::thread client_thread([this]() {
	// 	    // LOG(INFO) << "ChatRoom Server running on port: " << FLAGS_chatroom_port;
	// 	    server_running = true;
	// 	    server_->serve();
	// 	    server_running = false;
	// 	  });
	// baton.wait();
	// auto cb = std::make_unique<TestAsyncCallback>();
	// client->get_number(std::move(cb), 16);

	// std::this_thread::sleep_for(std::chrono::milliseconds(10000));
	// client->recv_get_number(result);
	// LOG(INFO) << "wait response ";
	// baton.wait();
	

	// std::this_thread::sleep_for(std::chrono::milliseconds(1500));

	return 0;
}

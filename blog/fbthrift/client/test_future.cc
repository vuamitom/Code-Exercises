#include <stdio.h>
#include <glog/logging.h>
#include <folly/init/Init.h>
#include <folly/portability/GFlags.h>
#include <thrift/lib/cpp2/server/ThriftServer.h>
#include <folly/futures/Future.h>
#include <folly/Unit.h>
#include <folly/synchronization/Baton.h>
#include <thrift/lib/cpp/async/TAsyncSocket.h>
#include <thrift/lib/cpp2/async/HeaderClientChannel.h>
#include <thrift/lib/cpp2/async/RocketClientChannel.h>
#include <thrift/lib/cpp2/async/RSocketClientChannel.h>
#include <vector>
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

std::unique_ptr<ThriftServer> newServer(int32_t port) {
  auto handler = std::make_shared<ExampleHandler>();
  auto proc_factory =
      std::make_shared<ThriftServerAsyncProcessorFactory<ExampleHandler>>(
          handler);
  auto server = std::make_unique<ThriftServer>();
  // server->setAddress(addr);
  server->setPort(port);
  server->setProcessorFactory(proc_factory);
  return server;
}

// class AsyncCallback : public apache::thrift::RequestCallback {
//  public:
//  	AsyncCallback(ClientReceiveState* result, folly::Baton<>* baton)
//  		: result_(result), baton_(baton) {}
//  	void requestSent() override {
//  		LOG(INFO) << "client: requestSent";
//  	}

// 	void replyReceived(ClientReceiveState&& state) override {
// 		LOG(INFO) << "client: replyReceived";
// 		*result_ = std::move(state);
// 		baton_->post();
// 	}

// 	void requestError(ClientReceiveState&& state) override {
// 		LOG(ERROR) << "client: requestError";		
// 		*result_ = std::move(state);
// 		LOG(ERROR) << "exception: " << result_->exception();
// 		baton_->post();
// 	}
//   private:
//   	folly::Baton<>* baton_;
//   	ClientReceiveState* result_;
// };
void onReply(int32_t number) {
	LOG(INFO) << "client: get response " << number;
}

void onError(std::exception const& e) {
	LOG(ERROR) << "client: error: " << e.what();
}

int main(int argc, char *argv[]) {
	LOG(INFO) << "Starting test ...";
	FLAGS_logtostderr = 1;	
	folly::init(&argc, &argv);

	// creating client
	folly::EventBase eb;
	folly::SocketAddress addr("127.0.0.1", thrift_port);
	auto client = newHeaderClient(&eb, addr);
	std::vector<folly::Future<folly::Unit>> futs;
	for (int32_t i = 10; i < 14; i++) {
		LOG(INFO) << "client: send number " << i;
		auto f = client->future_get_number(i);
		futs.push_back(std::move(f).thenValue(onReply).thenError<std::exception>(onError));
	}
	collectAll(futs.begin(), futs.end()).thenValue([&eb](std::vector<folly::Try<folly::Unit>>&& v){
		LOG(INFO) << "client: received all responses";
		eb.terminateLoopSoon();
	});
	eb.loopForever();
		
	return 0;
}
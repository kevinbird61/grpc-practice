# About google protobuf

這邊主要探討關於 protobuf 的格式與其對應的意義

我們就以下列這個程式碼來做探討：
```pb
syntax = "proto2";

package tutorial;

message Person {
  required string name = 1;
  required int32 id = 2;
  optional string email = 3;

  enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  message PhoneNumber {
    required string number = 1;
    optional PhoneType type = 2 [default = HOME];
  }

  repeated PhoneNumber phones = 4;
}

message AddressBook {
  repeated Person people = 1;
}
```

## Package

* Protobuf 以 `package` 作為開始，透過 package 指定名稱的方式來**防止`命名衝突`的問題**

* 而在 python 的 grpc 版本當中， package 則由 directory structure 來做決定; 所以在當 python 版本運行時，由 proto 定義的 package 則會失去作用

## Message

先來看看使用 `message` 作為定義關鍵字的使用：

### Field Type

* Protobuf 也定義許多 type 的關鍵字：
    * `bool`
    * `int32`
    * `float`
    * `double` 
    * `string`

* 除了使用原生的定義關鍵字外，也可以用其他定義好的 message type 作為 field type 於其他 message type 的物件內使用
    * 舉例來說，像是上方 example code 中 `Person` message 當中包含的 `PhoneNumber` messages; 並且在 message `AddressBook` 當中使用 `Person` 作為 field type 使用！

* `enum`:
    * 讓使用者能夠從中多個選項一個作選擇
    * 詳細可以看 example code 的 `PhoneType`，於 `Person` 當中做 enum 定義出 `PhoneType` 後， 在後面的 `PhoneNumber` 內做使用！

### =1, =2 ...

* 在上面範例 code 當中可以看到每個 attribute 都被賦予一個等號數值，這裡並不是單純的附值！ 而是於 protobuf 中特殊的使用!

* 這些數字標記用來給予一個獨一無二的 "tag" 給這個 field， 作為後續 binary encoding 使用
    * 而 range 在 `1~15` 中的 tag，則會比其他大於 15 的數值所使用的 bytes 上會小 1 個 byte 
    * 可以視其為一個 optimization -> 當這個欄位會被 **重複使用(e.g. `repeated`)**, 或是**經常被使用** 的話， 則可以利用這個 tag 的特性，藉由賦予其較小數值的 tag，來減少其使用的 bytes 數量

### Annotation

* 每個 field 在除了定義其 `field type` 之外，也會定義他的 *annotation*:
    * `required`
        * 代表這個欄位的數值必須一定要被提供，否則該 message 則會被認為是 *uninitialized*
        * 對一個 uninitialized 的 message 做 serializing 會發生 `exception`; 而對其做 parsing 的動作則會發生 `fail`; 除此之外基本上行為與 `optional` 相同
    * `optional`
        * 可以選擇性做賦值的動作; 若一個 optional 的欄位沒有被賦值，則系統會使用其預設值
    * `repeated`
        * 這個欄位的數值可以重複多次，當然也包括 0 次（e.g. 空的）
        * 可以想像他是一個 *dynamic sized 的 array*

## Service

在來看到 `service` 的使用

當你想要透過 RPC (Remote Procedure Call) 來使用你所定義的 `message` 時，則可以透過 `service` 這個定義字來建立一個 RPC 服務介面於 `.proto` 當中

剩餘的部份則透過 protobuf compiler 來產生 interface 相依的程式碼（你所選擇的程式）及 stub

舉例，我們定義一個 RPC Service，接收 `SearchRequest` 後，並將結果 - `SearchResponse` 做回傳（return）:
```
service SearchService {
  rpc Search (SearchRequest) returns (SearchResponse);
}
```

則透過 protobuf 編譯後，則會幫忙產生 `SearchService` 的抽象介面以及對應的 `stub` 的實作
而這個 `stub` 則會把所有 call forward 到一個 `RpcChannel` 當中，其為一個抽象介面，必須透過使用者自己的 RPC 系統程式來做定義，可見（以 C++ 為範例）：

Client 端的部份：

```c++
using google::protobuf;

protobuf::RpcChannel* channel;
protobuf::RpcController* controller;
SearchService* service;
SearchRequest request;
SearchResponse response;

void DoSearch() {
  // You provide classes MyRpcChannel and MyRpcController, which implement
  // the abstract interfaces protobuf::RpcChannel and protobuf::RpcController.
  channel = new MyRpcChannel("somehost.example.com:1234");
  controller = new MyRpcController;

  // The protocol compiler generates the SearchService class based on the
  // definition given above.
  service = new SearchService::Stub(channel);

  // Set up the request.
  request.set_query("protocol buffers");

  // Execute the RPC.
  service->Search(controller, request, response, protobuf::NewCallback(&Done));
}

void Done() {
  delete service;
  delete channel;
  delete controller;
}
```

而 server 端可以這麼做：

```c++
using google::protobuf;

class ExampleSearchService : public SearchService {
 public:
  void Search(protobuf::RpcController* controller,
              const SearchRequest* request,
              SearchResponse* response,
              protobuf::Closure* done) {
    if (request->query() == "google") {
      response->add_result()->set_url("http://www.google.com");
    } else if (request->query() == "protocol buffers") {
      response->add_result()->set_url("http://protobuf.googlecode.com");
    }
    done->Run();
  }
};

int main() {
  // You provide class MyRpcServer.  It does not have to implement any
  // particular interface; this is just an example.
  MyRpcServer server;

  protobuf::Service* service = new ExampleSearchService;
  server.ExportOnPort(1234, service);
  server.Run();

  delete service;
  return 0;
}
```

## 小結

大致上可以從上面看出 grpc 以及 pb 之間的關係！

grpc 透過 pb 的特性，實作這些關鍵字作為其生成相依的來源，並為使用者實作 RPC 的介面，以及處理底層網路傳輸方面的程式碼; 讓使用者只需要著重在如何使用即可！


# Reference

* [Protocol buffer(Python)](https://developers.google.com/protocol-buffers/docs/pythontutorial)

* [Language Guide (Protocol buffer)](https://developers.google.com/protocol-buffers/docs/proto#packages)

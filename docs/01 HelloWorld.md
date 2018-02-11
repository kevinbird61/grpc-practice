# 01-HelloWorld 教學

## 開始

### 安裝 gRPC
- 在使用這篇教學前，需要安裝 gRPC 於你的系統上
依照以下的指示來做操作：[安裝說明](https://github.com/grpc/grpc/tree/master/src/cpp)

### 說明
- 本章教學主要使用來自 grpc 官方教學中的 helloworld 教學
- 說明原始碼位置於專案 `grpc-practice/01-HelloWorld` 底下
- 而本章主要著重在：
    - **如何編譯 protocol buffer**
    - **如何使用 pb 編譯後產生的檔案**（也是就是 grpc 的主要功能）

### 使用
```bash
# 產生 grpc 所有程式碼
$ make

# 清理所有 grpc 編譯產生 object 檔案
$ make clean

# 產生 document(透過轉換 markdown 成 static web)
$ make doc_page

# 清除 document 檔案
$ make clean_doc
```

## gRPC client/server

### 編譯 protocol buffer code
- 透過由 `protoc` 這個 protocol buffer compiler，並且利用他來編譯產生 `.pb.cc`、`.pb.h`、`.grpc.pb.cc`、`.grpc.pb.h` 的相依性檔案
- 分別透過兩次編譯，來產生：
    - 針對 ***service*** 定義所產生的: `*.grpc.pb.*`
    - 針對 ***message*** 定義所產生的: `*.pb.*`

```bash
# 第一次編譯
$ protoc -I path_to_your_protos --grpc_out=. --plugin=protoc-gen-grpc=path_to_your_cpp_plugin yourfile.proto

# 第二次編譯
$ protoc -I path_to_your_protos --cpp_out=. yourfile.proto 
```
- 第一次編譯時，會產生對應的 `*.grpc.pb.*`，同時也是當初在 yourfile.proto 裡頭定義的 service class
    - 這支檔案內會需要 `*.pb.*` 的定義，因此需要第二次編譯
    - `path_to_your_protos`: 這邊填入你 proto files 放置的位置
    - `--grpc_out=<path>`: 這邊指定輸出的檔案位置
    - `--plugin=...`: 這邊是指定轉換的格式，在這邊使用到的是 cpp，可以在 terminal 輸入 `which grpc_cpp_plugin` 來找到 cpp plugin 在你的開發環境的位置
    - 最後就是要轉換的那支 `.proto` 

- 第二次編譯，會產生 `*.pb.*`，同時也是當初 yourfile.proto 裡頭定義的 message 的部份
    - 這支檔案則是主要提供這些方便功能的主要程式碼 

- 到此為止，我們便成功的使用原有 protocol buffer 檔案轉換成為 c++ 可以使用的程式碼

### 實作 gRPC 的 client

Client 的部份可以看到，在 header files 的部份需要 include 來源 `.proto` 所產生的相依檔案 - `helloworld.grpc.pb.h`, 以及 C++ 的 grpc core library - `grpc++/grpc++.h`

再來就可以引入 `.proto` 內的 message, services 做使用！這邊可以看到程式所定義的 namespace 有 service 的 Greeter, 以及 message 的 HelloRequest 以及 HelloReply

有了這些 class, 使用者便可以利用這些來做一個封裝 - `GreeterClient` 的 class 產生！ 如此一來我們便可以利用這些 grpc 幫我們產生好的東西來做 RPC 傳輸的動作（在這個 scenario 當中，是 client 與 server 間相互傳遞一個問候語）

詳細對應的操作可以看原始碼 `01-HelloWorld` 中的 `grpc_client.cpp`.

### 實作 gRPC 的 server 

Server 的部份在 include 的部份也和 client 相同

而在 server 的部份，則是單純做一個 listening 的動作，透過 grpc 提供的 `ServerBuilder` 來建立 service (一樣繼承 `.proto` 所實作的 service - `Greeter` 來做新的實作)， 並把這個 service 加入到 server 的 class 當中（由 grpc 提供），完成後即可等待使用者的呼叫

這邊可以看到，在 client 與 server 中 message class 對於 access 自己的 attribute 的 method 則是以 `set_` 加上 attribute name 做命名


## 小結

grpc 的使用，主要還是透過其本身提供的 library 做實作，所以在使用前需要詳細閱讀其規格與定義！

不過可以從這個例子看到，在實作一個 RPC 服務來說， grpc 已經為我們做了大部份底層的功夫，剩餘的部份只需要我們去寫我們要的規格（protocol）以及 client, server 的主架構即可使用！


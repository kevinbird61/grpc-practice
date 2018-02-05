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

### 實作 gRPC 的 server 
(待補上)

### 實作 gRPC 的 client
(待補上)
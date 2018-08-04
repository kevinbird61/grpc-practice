# 02-Streaming 教學

### 說明

* 本章主要著重在:
    * **如何使用 grpc 當中的 stream**
    * **並使用 python 來展示**

### 執行程式

* 安裝相關開發環境
    * 手動安裝 python 
    * 透過 `pip` 來安裝相依性: `pip install grpcio-tools` (大約 5 min)

* 編譯產生 `*_pb2_grpc` 以及 `*_pb2`
```bash
$ python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/route_guide.proto
```

* 開啟 server 與 client 
    * 先 `python server.py`
    * 再來 `python client.py`，檢視溝通結果
    > 在本範例當中， client 的部分拿掉官方上頭 location 檢查是否相等的部分，直接在接收後便馬上做回傳
    * 得到的結果 (針對 `bidirectional` 顯示):
    ```
    > python client.py
    ... 
    -------------- RouteChat --------------
    Sending First message at
    Sending Second message at lng: 1

    Sending Third message at lat: 1

    Sending Fourth message at
    Received message First message at
    Sending Fifth message at lat: 1

    Received message Second message at lng: 1

    Received message Third message at lat: 1

    Received message Fourth message at
    Received message Fifth message at lat: 1
    ```
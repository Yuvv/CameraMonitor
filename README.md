# CameraMonitor
Camera data monitor

## 数据格式设计

采集周期：0.5秒/数据包

数据格式设计

| **2字节：数据包序列号** | **1字节：厂房和镁炉编号** |           | **49字节：PLC过程数据** | **数据采集时间（日期：年月日时分秒）** | **2字节：校验码** |
| :------------: | :-------------: | :-------: | :--------------: | :-------------------: | :---------: |
|      序列号       |     厂房编号：2位     | 电熔镁炉编号：6位 |       见表1        |                       |     可省略     |

 

**各字节说明如下：**

1.      厂房编号：1-5 

2.      电熔镁炉编号：1-10

3.      PLC过程数据：49字节

表1：PLC过程数据

| A相电流   | 4字节    |
| ------ | ------ |
| B相电流   | 4字节    |
| C相电流   | 4字节    |
| 电流设定值  | 4字节    |
| A相电压   | 4字节    |
| B相电压   | 4字节    |
| C相电压   | 4字节    |
| 手动电极速度 | 4字节    |
| 炉体转动速度 | 4字节    |
| A动作    | 4字节    |
| B动作    | 4字节    |
| C动作    | 4字节    |
| 手/自动状态 | 1位，见表2 |
| 加料指示   | 1位，见表2 |
| 排气指示   | 1位，见表2 |

表2：指示位

| **位****0** | **位****1** | **位****2** | **位****3** | **位****4** | **位****5** | **位****6** | **位****7** |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| 手/自动状态     | 加料指示       | 排气指示       | 预留         | 预留         | 预留         | 预留         | 预留         |

4.      数据采集时间：年-月-日-时-分-秒


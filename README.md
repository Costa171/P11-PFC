# Use and application of cryptographic algorithms in cloud computing.

### Final Project for Bachelor's Degree in Electronic, Telecommunications, and Computer Engineering

### Student: Pedro Costa (Nº49944)
### Supervisor: Prof. Valderi Leithardt
---

## Overview
<p align="justify">
This project addresses the critical concern of ensuring data security and efficiency in interconnected devices, particularly within IoT environments. The objective is to design and implement a model utilizing cryptographic algorithms to enhance data security in applications and sceneraios that use 5G networks.
</p>

## Motivation
<p align="justify">
With the increasing prevalence of cloud computing, edge computing, and big data in everyday life and business operations, ensuring the security of data processed by IoT devices against potential intruders has become paramount. The fields of medicine, smart grids, home automation, precision agriculture, and urban mobility represent just a few of the many scenarios where cloud computing is present. However, with the benefits of connectivity come significant risks, particularly regarding data security, which is the focus of this project.
</p>

## Objectives

1. Select and analyze different cryptographic algorithms to identify those with the best performance in terms of encryption and decryption time, while also considering packet size.
2. Implement these algorithms in a structured model to assess the time taken to encrypt and decrypt varied sizes of packets.
3. Analyze the performance of the model regarding the quantity of packets being transmitted.
4. Utilize cloud computing to enhance processing efficiency and resource utilization, while caring for memory usage and CPU architeture.


## Model created
<p align="justify">
For this project was  designed and implemented a structure model that uses cryptographic algorithms used in applications and scenarios that use 5G networks for data protection. This structure model has four levels (Guest,Basic,Advanced,Admin) that use encapsulation to create a better data security. It is important to clarify that, in the structure model, as the levels change, the algorithms used will also increase, maintaining a basic algorithm and adding a more robust algorithm as the levels grow. For example, in the Guest level, only one algorithm is used for encrypting data. However, at the Advanced level, two additional algorithms are introduced for data encryption so in total three algorithms will be used. With this approach, for instance, if someone intercepted the data, they would need to identify the pattern of algorithms used to access the unencrypted data. This is the reason behind the usage of the encapsulation process, rather than the only one or the same algorithm across all levels. Additionally,we explored cloud computing to enhance the scalability and performance of our cryptographic solution.
</p>   
<p align="justify">
Using the Python programming language in conjunction with flask, which is a framework that allows you to develop web applications, an interactive interface was built which presents the user the time required for encryption and decryption of data, the algorithms that were used, the access level, the packet size and quantity, and finally the client and server process time.
</p>  


<p align="center">
  <img src="https://github.com/user-attachments/assets/7a98fcdc-f928-4282-9bfa-7a8cfe388333" alt="Interface created" width="700">
</p>


<p align="justify">
As shown in the figure, the user interacts with the structure model application that is hosted in the cloud, and this application send a request to the server for encrypted data that will be decrypted in the cloud. Lastly it is generated a results page showing the all the information related to the test made.
</p>   

<p align="center">
  <img src="https://github.com/user-attachments/assets/66a3b865-72aa-4548-bfce-80869d8a15b6" alt="Cloud model">
</p>


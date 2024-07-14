# Secure Data Transmission with Flask and Crypto
<p align="justify">
This project demonstrates a secure data transmission application using Flask and various cryptographic algorithms. The application allows clients to send data to a server, which encrypts it based on the selected encryption level, and sends it back to the client for decryption. The server and client communicate over HTTP using JSON for data exchange.
</p>

## Features
1. Encryption Levels: Supports different encryption levels (Guest, Basic, Advanced, Admin) with increasing complexity.
2. Encryption Algorithms: Utilizes AES-256, AES-CTR, and XChaCha20 algorithms for encryption and decryption.
3. Data Integrity: Includes HMAC-SHA-256 for data integrity verification.
4. Memory Management: Uses Python's gc module for memory management to ensure efficient resource utilization.
5. Performance Testing: Measures encryption/decryption times and overall processing times for performance evaluation.

## Components
### Server (server.py)
The server side is implemented in Flask and performs the following tasks:
<p align="justify">
Receives data from clients via HTTP POST requests.
Generates random keys and nonce for encryption.
Encrypts data based on the selected encryption level.
Calculates encryption times and server processing times.
Sends back encrypted data along with encryption keys.
</p>

### Client (client.py)
The client side is implemented in Flask and involves:
<p align="justify">
Accepting user input for encryption level, data size, unit, and packet quantity.
Sending data to the server for encryption and receiving encrypted data and keys.
Decrypting data using the received keys.
Measuring client-side processing times and displaying results.
</p>
### Cryptographic Functions (functions.py)
Contains implementations of various cryptographic algorithms used in the project:
1. AES-256 (CBC mode), AES-CTR encryption/decryption.
2. HMAC-SHA-256 for integrity checks.
3. XChaCha20 encryption/decryption.

## Usage
1. Select an encryption level (Guest, Basic, Advanced, Admin).
2. Enter data size, unit (KB/MB), and packet quantity.
3. Submit the form to see the encryption/decryption times and overall processing times.

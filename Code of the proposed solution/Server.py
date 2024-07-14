from flask import Flask, request, jsonify
import time
import functions as ed
from Crypto.Random import get_random_bytes
import base64
import secrets
from tinyec import registry

#Server - Base64 encoding is essential for transmitting binary data over text-based protocols like HTTP, SMTP, or FTP.
app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def test_speed():
    test_type = request.form['test_type']
    custom_size = int(request.form['custom_size'])
    value_unit = request.form['value_unit']
    packet_quantity= int(request.form['packet_quantity'])

    ServerTimeProcess_start=time.time()

    key_aes_256 = get_random_bytes(32) # 256-bit key
    key_aes_ctr = get_random_bytes(16)  #  128-bit key
    hmac_key = get_random_bytes(32) # 256-bit key
    key_xchacha20 = get_random_bytes(32) #256-bit key
    nonce_xchacha20 = get_random_bytes(24) #24 bytes nonce
    
    # Generate random data
    if value_unit == 'MB':
        data =  b'A' * (custom_size*packet_quantity)  * 1024 * 1024  # Data in MB
    elif value_unit == 'KB':
        data =  b'A' * (custom_size*packet_quantity)  * 1024

    
    # Encryption process
    start_time = time.time()
    if test_type == 'Guest':
        encrypted_data = ed.aes_256_encrypt(data, key_aes_256)
    elif test_type == 'Basic':
        encrypted_data_aes_256 = ed.aes_256_encrypt(data, key_aes_256)
        encrypted_data = ed.aes_ctr_encrypt(encrypted_data_aes_256,key_aes_ctr)
    elif test_type == 'Advanced':
        encrypted_data_aes_256 = ed.aes_256_encrypt(data, key_aes_256)
        encrypted_data_aes_ctr = ed.aes_ctr_encrypt(encrypted_data_aes_256,key_aes_ctr)
        encrypted_data = ed.hmac_encrypt(encrypted_data_aes_ctr, hmac_key)
    elif test_type == 'Admin':
        encrypted_data_aes_256 = ed.aes_256_encrypt(data, key_aes_256)
        encrypted_data_aes_ctr = ed.aes_ctr_encrypt(encrypted_data_aes_256,key_aes_ctr)
        encrypted_data_hmac = ed.hmac_encrypt(encrypted_data_aes_ctr, hmac_key)
        encrypted_data = ed.xchacha20_encrypt(encrypted_data_hmac,key_xchacha20,nonce_xchacha20)
        
    end_time = time.time()

    encryption_time = end_time - start_time

    encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')

    if test_type == 'Guest':
        key_aes256_base64 = base64.b64encode(key_aes_256).decode('utf-8')
    elif test_type == 'Basic':
        key_aes256_base64 = base64.b64encode(key_aes_256).decode('utf-8')
        key_aesCtr_base64 = base64.b64encode(key_aes_ctr).decode('utf-8')
    elif test_type == 'Advanced':
        key_aes256_base64 = base64.b64encode(key_aes_256).decode('utf-8')
        key_aesCtr_base64 = base64.b64encode(key_aes_ctr).decode('utf-8')
        key_hmacSha256_base64 = base64.b64encode(hmac_key).decode('utf-8')
    elif test_type == 'Admin':
        key_aes256_base64 = base64.b64encode(key_aes_256).decode('utf-8')
        key_aesCtr_base64 = base64.b64encode(key_aes_ctr).decode('utf-8')
        key_hmacSha256_base64 = base64.b64encode(hmac_key).decode('utf-8')
        key_xchacha20_base64 = base64.b64encode(key_xchacha20).decode('utf-8')
        nonce_xchacha20_base64 = base64.b64encode(nonce_xchacha20).decode('utf-8')

    ServerTimeProcess_end=time.time()

    ServerTimeProcess = ServerTimeProcess_start - ServerTimeProcess_end
    if test_type == 'Guest':
        response_data = {
            'encrypted_data': encrypted_data_base64,
            'key': key_aes256_base64,
            'encryption_time': encryption_time,
            'serverTimeProcess': ServerTimeProcess
        }
    elif test_type == 'Basic':
        response_data = {
            'encrypted_data': encrypted_data_base64,
            'key_aes256': key_aes256_base64,
            'key_aesCtr': key_aesCtr_base64,
            'encryption_time': encryption_time,
            'serverTimeProcess': ServerTimeProcess
        }
    elif test_type == 'Advanced':
         response_data = {
            'encrypted_data': encrypted_data_base64,
            'key_aes256': key_aes256_base64,
            'key_aesCtr': key_aesCtr_base64,
            'key_hmacSha256': key_hmacSha256_base64,
            'encryption_time': encryption_time,
            'serverTimeProcess': ServerTimeProcess
        }
    elif test_type == 'Admin':
        response_data = {
            'encrypted_data': encrypted_data_base64,
            'key_aes256': key_aes256_base64,
            'key_aesCtr': key_aesCtr_base64,
            'key_hmacSha256': key_hmacSha256_base64,
            'key_xchacha20': key_xchacha20_base64,
            'nonce': nonce_xchacha20_base64,
            'encryption_time': encryption_time,
            'serverTimeProcess': ServerTimeProcess
        }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,threaded=True)


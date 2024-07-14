from flask import Flask, request, jsonify
import time
import functions as ed
from Crypto.Random import get_random_bytes
import base64
import gc

# Server - Base64 encoding is essential for transmitting binary data over text-based protocols like HTTP, SMTP, or FTP.
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test_speed():
    test_type = request.form['test_type']
    custom_size = int(request.form['custom_size'])
    value_unit = request.form['value_unit']
    packet_quantity = int(request.form['packet_quantity'])

    ServerTimeProcess_start = time.time()

    key_aes_256 = get_random_bytes(32)  # 256-bit key
    key_aes_ctr = get_random_bytes(16)  # 128-bit key
    hmac_key = get_random_bytes(32)  # 256-bit key
    key_xchacha20 = get_random_bytes(32)  # 256-bit key
    nonce_xchacha20 = get_random_bytes(24)  # 24 bytes nonce

    # Generate random data
    if value_unit == 'MB':
        data = b'A' * (custom_size * packet_quantity) * 1024 * 1024  # Data in MB
    elif value_unit == 'KB':
        data = b'A' * (custom_size * packet_quantity) * 1024  # Data in KB

    # Encryption process
    start_time = time.time()
    if test_type == 'Guest':
        encrypted_data = ed.aes_256_encrypt(data, key_aes_256)
    elif test_type == 'Basic':
        encrypted_data = ed.aes_ctr_encrypt(ed.aes_256_encrypt(data, key_aes_256), key_aes_ctr)
    elif test_type == 'Advanced':
        encrypted_data = ed.hmac_encrypt(
            ed.aes_ctr_encrypt(ed.aes_256_encrypt(data, key_aes_256), key_aes_ctr), hmac_key
        )
    elif test_type == 'Admin':
        encrypted_data = ed.xchacha20_encrypt(
            ed.hmac_encrypt(
                ed.aes_ctr_encrypt(ed.aes_256_encrypt(data, key_aes_256), key_aes_ctr), hmac_key
            ), key_xchacha20, nonce_xchacha20
        )
    end_time = time.time()

    del data
    gc.collect()

    encryption_time = end_time - start_time

    encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')

      # Free up memory
    del encrypted_data
    gc.collect()

    key_map = {
        'Guest': {'key': base64.b64encode(key_aes_256).decode('utf-8')},
        'Basic': {
            'key_aes256': base64.b64encode(key_aes_256).decode('utf-8'),
            'key_aesCtr': base64.b64encode(key_aes_ctr).decode('utf-8')
        },
        'Advanced': {
            'key_aes256': base64.b64encode(key_aes_256).decode('utf-8'),
            'key_aesCtr': base64.b64encode(key_aes_ctr).decode('utf-8'),
            'key_hmacSha256': base64.b64encode(hmac_key).decode('utf-8')
        },
        'Admin': {
            'key_aes256': base64.b64encode(key_aes_256).decode('utf-8'),
            'key_aesCtr': base64.b64encode(key_aes_ctr).decode('utf-8'),
            'key_hmacSha256': base64.b64encode(hmac_key).decode('utf-8'),
            'key_xchacha20': base64.b64encode(key_xchacha20).decode('utf-8'),
            'nonce': base64.b64encode(nonce_xchacha20).decode('utf-8')
        }
    }

    del key_aes_256, key_aes_ctr, hmac_key, key_xchacha20, nonce_xchacha20
    gc.collect()

    response_data = {
        'encrypted_data': encrypted_data_base64,
        'encryption_time': encryption_time,
        'serverTimeProcess': time.time() - ServerTimeProcess_start
    }

    # Merge keys into response data
    response_data.update(key_map[test_type])

    del encrypted_data_base64
    gc.collect()

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

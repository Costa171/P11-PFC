from flask import Flask, render_template, request
import functions as ed
import requests
import time
import base64
import gc

# Client
app = Flask(__name__)

# Function to send data to the server and receive response
def send_data(test_type, custom_size, value_unit, packet_quantity):
    url = 'http://home.mrcosta.net:8080'
    payload = {
        'test_type': test_type,
        'custom_size': custom_size,
        'value_unit': value_unit,
        'packet_quantity': packet_quantity
    }
    response = requests.post(url, data=payload)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_speed', methods=['GET', 'POST'])
def test_speed():
    test_type = request.form['test_type']
    custom_size = int(request.form['custom_size'])
    value_unit = request.form['unit']
    packet_quantity = int(request.form['packet_quantity'])

    response_data = send_data(test_type, custom_size, value_unit, packet_quantity)
    clientTimeProcess_start = time.time()
    encrypted_data = base64.b64decode(response_data['encrypted_data'])

    key_map = {
        'Guest': ['key'],
        'Basic': ['key_aes256', 'key_aesCtr'],
        'Advanced': ['key_aes256', 'key_aesCtr', 'key_hmacSha256'],
        'Admin': ['key_aes256', 'key_aesCtr', 'key_hmacSha256', 'key_xchacha20', 'nonce']
    }

    keys = {key: base64.b64decode(response_data[key]) for key in key_map[test_type]}

    decryption_start_time = time.time()

    if test_type == 'Guest':
        decrypted_data = ed.aes_256_decrypt(encrypted_data, keys['key'])
    elif test_type == 'Basic':
        decrypted_data = ed.aes_256_decrypt(
            ed.aes_ctr_decrypt(encrypted_data, keys['key_aesCtr']),
            keys['key_aes256']
        )
    elif test_type == 'Advanced':
        decrypted_data = ed.aes_256_decrypt(
            ed.aes_ctr_decrypt(
                ed.hmac_decrypt(encrypted_data, keys['key_hmacSha256']),
                keys['key_aesCtr']
            ),
            keys['key_aes256']
        )
    elif test_type == 'Admin':
        decrypted_data = ed.aes_256_decrypt(
            ed.aes_ctr_decrypt(
                ed.hmac_decrypt(
                    ed.xchacha20_decrypt(encrypted_data, keys['key_xchacha20'], keys['nonce']),
                    keys['key_hmacSha256']
                ),
                keys['key_aesCtr']
            ),
            keys['key_aes256']
        )

    decryption_end_time = time.time()
    clientTimeProcess_end = time.time()

    clientTimeProcess = clientTimeProcess_end - clientTimeProcess_start
    decryption_time = decryption_end_time - decryption_start_time
    TotalProcessTime = clientTimeProcess + response_data['serverTimeProcess']

    # Free the decrypted_data variable
    del decrypted_data
    gc.collect()

    return render_template(
        'results.html',
        encrypt_time=response_data['encryption_time'],
        server_time=response_data['serverTimeProcess'],
        client_time=clientTimeProcess,
        total_time=TotalProcessTime,
        decrypt_time=decryption_time,
        custom_size=custom_size,
        level_used=test_type,
        value_unit=value_unit,
        packet_quantity=packet_quantity
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)


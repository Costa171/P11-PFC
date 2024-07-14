from flask import Flask, render_template,request
import functions as ed
import requests
import time
import base64

#Client
app= Flask(__name__)
#home.mrcosta.net
# Function to send data to the server and receive response
def send_data(test_type, custom_size,value_unit,packet_quantity):
    url = 'http://home.mrcosta.net:8080'
    payload = {'test_type': test_type, 'custom_size': custom_size, 'value_unit':value_unit, 'packet_quantity':packet_quantity}
    response = requests.post(url, data=payload)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_speed', methods=['GET','POST'])
def test_speed():
    test_type = request.form['test_type']
    custom_size = int(request.form['custom_size'])
    value_unit = request.form['unit']
    packet_quantity= int(request.form['packet_quantity'])
    
    response_data = send_data(test_type, custom_size,value_unit,packet_quantity)
    clientTimeProcess_start = time.time()
    encrypted_data_base64 = response_data['encrypted_data']
    encrypted_data =  base64.b64decode(encrypted_data_base64)
    
    if test_type == 'Guest':
        key_base64 = response_data['key']
        key_aes256=base64.b64decode(key_base64)
    elif test_type == 'Basic':
        key_aes256_base64=response_data['key_aes256']
        key_aes256 = base64.b64decode(key_aes256_base64)
        key_aesctr_base64=response_data['key_aesCtr']
        key_aesctr = base64.b64decode(key_aesctr_base64)
    elif test_type == 'Advanced':
        key_aes256_base64=response_data['key_aes256']
        key_aes256 = base64.b64decode(key_aes256_base64)
        key_aesctr_base64=response_data['key_aesCtr']
        key_aesctr = base64.b64decode(key_aesctr_base64)
        key_hmacSha256_base64 = response_data['key_hmacSha256']
        key_hmacSha256 = base64.b64decode(key_hmacSha256_base64)
    elif test_type == 'Admin':
        key_aes256_base64=response_data['key_aes256']
        key_aes256 = base64.b64decode(key_aes256_base64)
        key_aesctr_base64=response_data['key_aesCtr']
        key_aesctr = base64.b64decode(key_aesctr_base64)
        key_hmacSha256_base64 = response_data['key_hmacSha256']
        key_hmacSha256 = base64.b64decode(key_hmacSha256_base64)
        key_xchacha20_base64 = response_data['key_xchacha20']
        key_xchacha20 = base64.b64decode(key_xchacha20_base64)
        nonce_xchacha20_base64 = response_data['nonce']
        nonce_xchacha20= base64.b64decode(nonce_xchacha20_base64)
    
    decryption_start_time = time.time()
    if test_type == 'Guest':
        decrypted_data = ed.aes_256_decrypt(encrypted_data, key_aes256)
    elif test_type == 'Basic':
        decrypted_data_aes_ctr = ed.aes_ctr_decrypt(encrypted_data, key_aesctr)
        decrypted_data = ed.aes_256_decrypt(decrypted_data_aes_ctr, key_aes256)
    elif test_type == 'Advanced':
        decrypted_data_hmac = ed.hmac_decrypt(encrypted_data, key_hmacSha256)
        decrypted_data_aes_ctr = ed.aes_ctr_decrypt(decrypted_data_hmac, key_aesctr)
        decrypted_data = ed.aes_256_decrypt(decrypted_data_aes_ctr, key_aes256)
    elif test_type == 'Admin':
        decrypted_data_ECC = ed.xchacha20_decrypt(encrypted_data, key_xchacha20,nonce_xchacha20)
        decrypted_data_hmac = ed.hmac_decrypt(decrypted_data_ECC, key_hmacSha256)
        decrypted_data_aes_ctr = ed.aes_ctr_decrypt(decrypted_data_hmac, key_aesctr)
        decrypted_data = ed.aes_256_decrypt(decrypted_data_aes_ctr, key_aes256)
    decryption_end_time = time.time()
    clientTimeProcess_end = time.time()

    clientTimeProcess = clientTimeProcess_end - clientTimeProcess_start
    decryption_time = decryption_end_time - decryption_start_time
    TotalProcessTime=clientTimeProcess+response_data['serverTimeProcess']

    return render_template('results.html', encrypt_time=response_data['encryption_time'],server_time=response_data['serverTimeProcess'],client_time=clientTimeProcess,total_time=TotalProcessTime, decrypt_time=decryption_time,custom_size=custom_size,level_used=test_type,value_unit=value_unit,packet_quantity=packet_quantity)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080,threaded=True)

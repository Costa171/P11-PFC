from Crypto.Cipher import AES
import hashlib
import sys
import binascii
from Crypto.Random import get_random_bytes

plaintext='hello how are you?'
password='qwerty123'


if (len(sys.argv)>1):
  plaintext=(sys.argv[1])
if (len(sys.argv)>2):
  password=(sys.argv[2])

def encrypt(plaintext,key):
  cipher = AES.new(key, AES.MODE_GCM)
  ciphertext,authTag=cipher.encrypt_and_digest(plaintext)
  return(ciphertext,authTag,cipher.nonce)

def decrypt(ciphertext,key):
  (ciphertext,  authTag, nonce) = ciphertext
  cipher = AES.new(key,  AES.MODE_GCM, nonce)
  return(cipher.decrypt_and_verify(ciphertext, authTag))

key = get_random_bytes(32)

print("GCM Mode: Stream cipher and authenticated")
print("\nMessage:\t",plaintext)
print("Key:\t\t",password)


ciphertext = encrypt(plaintext.encode(),key)

print("Cipher:\t\t",binascii.hexlify(ciphertext[0]))
print("Auth Msg:\t",binascii.hexlify(ciphertext[1]))
print("Nonce:\t\t",binascii.hexlify(ciphertext[2]))


res= decrypt(ciphertext,key)


print ("\n\nDecrypted:\t",res.decode())
import base58
import base64
import hashlib
import struct
from ecdsa import SigningKey, SECP256k1

####################################################################################################
## Encoding
####################################################################################################

def encode58(src):
    return base58.b58encode(src).decode()

def decode58(src):
    return base58.b58decode(src)

def encode64(src):
    return base64.b64encode(src).decode()

def decode64(src):
    return base64.b64decode(src)

####################################################################################################
## Hashing
####################################################################################################

def sha256(data): 
    return hashlib.sha256(data).digest()

def sha512(data):
    return hashlib.sha512(data).digest()

def sha160(data):
    return sha512(data)[:20]

def hash(data):
    return encode58(sha256(data))

def derive_hash(address, nonce, txActionNumber):
    addressB = decode58(address)
    nonceB = nonce.to_bytes(8, byteorder='big')
    txActionNumberB = txActionNumber.to_bytes(2, byteorder='big')
    return hash(addressB + nonceB + txActionNumberB)

def blockchain_address(publicKey):
    prefix = bytes(bytearray.fromhex('065A'))
    publicKeyHashWithPrefix = prefix + sha160(sha256(publicKey))
    checksum = sha256(sha256(publicKeyHashWithPrefix))[:4]
    return encode58(publicKeyHashWithPrefix + checksum)

####################################################################################################
## Signing
####################################################################################################

def decompress(pk):
     return bytes(chr(4), 'ascii') + pk.to_string()
     
def generate_wallet(): 
    sk = SigningKey.generate(curve=SECP256k1)
    pk = sk.get_verifying_key()
    privateKey = encode58(sk.to_string())
    publicKey = bytes(chr(4), 'ascii') + pk.to_string()
    address = blockchain_address(decompress(pk))
    return (privateKey, address)    
    
def address_from_private_key(privateKey):      
    privateKeyB = decode58(privateKey)
    sk = SigningKey.from_string(privateKeyB, curve=SECP256k1)
    pk = sk.get_verifying_key()
    return blockchain_address(decompress(pk))

def wallet_from_private_key(privateKey):
    address = address_from_private_key(privateKey)
    return (privateKey, address)

####################################################################################################
## Testing
####################################################################################################

def test_encode_decode_base64():
    originalData = 'Chainium'
    expected = 'Q2hhaW5pdW0='
    actual = encode64(originalData.encode())
    decoded = decode64(actual).decode()
    print('Expected = ', expected, ' | Actual = ', actual)
    print('Original = ', originalData, ' | Decoded = ', decoded)

def test_encode_decode_base58():
    originalData = 'Chainium'
    expected = 'CGwVR5Wyya4'
    actual = encode58(originalData.encode())
    decoded = decode58(actual).decode()
    print('Expected = ', expected, ' | Actual = ', actual)
    print('Original = ', originalData, ' | Decoded = ', decoded)

def test_hash(): 
    originalData = 'Chainium'
    expected = 'Dp6vNLdUbRTc1Y3i9uSBritNqvqe4es9MjjGrVi1nQMu'
    actual = hash(originalData.encode())
    print('Expected = ', expected, ' | Actual = ', actual)

def test_derive_hash():
    address = 'CHPJ6aVwpGBRf1dv6Ey1TuhJzt1VtCP5LYB'
    nonce = 32
    txActionNumber = 2
    expected = '5kHcMrwXUptjmbdR8XBW2yY3FkSFwnMdrVr22Yg39pTR'
    actual = derive_hash(address, nonce, txActionNumber)
    print('Expected = ', expected, ' | Actual = ', actual)

def test_generate_wallet():
    privateKey, address = generate_wallet()
    expected = address   
    actual = address_from_private_key(privateKey)
    print('Expected = ', expected, ' | Actual = ', actual)    
    
def test_address_from_private_key():
    privateKey = '3rzY3EENhYrWXzUqNnMEbGUr3iEzzSZrjMwJ1CgQpJpq'
    expected = 'CHGmdQdHfLPcMHtzyDzxAkTAQiRvKJrkYv8'
    actual = address_from_private_key(privateKey)
    print('Expected = ', expected, ' | Actual = ', actual)    
        
test_encode_decode_base64()
test_encode_decode_base58()
test_hash()
test_derive_hash()
test_generate_wallet()
test_address_from_private_key()

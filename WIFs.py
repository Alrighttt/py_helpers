#!/usr/bin/env python3
import hashlib
import binascii
import base58
import platform


import bitcoin
from bitcoin.wallet import P2PKHBitcoinAddress
from bitcoin.core import x
from bitcoin.core import CoreMainParams
from slickrpc import Proxy

if platform.system() != 'Windows':
    import readline

class CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}

bitcoin.params = CoinParams

pubkey_check = P2PKHBitcoinAddress.from_pubkey(x('02443ecb4b78fdbbc372c278d092bf03d535ddb1eb2310b56a56a58052c8a3109d'))
print(pubkey_check)

"""
def hash160(hexstr):
    preshabin = binascii.unhexlify(hexstr)
    my160 = hashlib.sha256(preshabin).hexdigest()
    return(hashlib.new('ripemd160', binascii.unhexlify(my160)).hexdigest())

def addr_from_ripemd(prefix, ripemd):
    net_byte = prefix + ripemd
    bina = binascii.unhexlify(net_byte)
    sha256a = hashlib.sha256(bina).hexdigest()
    binb = binascii.unhexlify(sha256a)
    sha256b = hashlib.sha256(binb).hexdigest()
    hmmmm = binascii.unhexlify(net_byte + sha256b[:8])
    final = base58.b58encode(hmmmm)
    return(final.decode())

def WIFdecode(WIF):
    b58decode = base58.b58decode(WIF)
    full_privkey = binascii.hexlify(b58decode)
    raw_privkey = full_privkey[2:-8]
    return(raw_privkey.decode("utf-8"))

def WIF_uncompressed(byte, raw_privkey):
    extended_key = byte+raw_privkey
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key[:66])).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # add checksum to end of extended key
    final_key = extended_key[:66]+second_sha256[:8]
    # Wallet Import Format = base 58 encoded final_key
    WIF = base58.b58encode(binascii.unhexlify(final_key))
    return(WIF.decode("utf-8"))

def WIF_compressed(byte, raw_privkey):
    extended_key = byte+raw_privkey+'01'
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key[:68])).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # add checksum to end of extended key
    final_key = extended_key[:68]+second_sha256[:8]
    # Wallet Import Format = base 58 encoded final_key
    WIF = base58.b58encode(binascii.unhexlify(final_key))
    return(WIF.decode("utf-8"))

WIF = ""
raw_privkey = WIFdecode(WIF) #modo0 2021testnet


print('KMD: ', WIF_compressed('bc', raw_privkey))
print('LTC: ', WIF_compressed('b0', raw_privkey))

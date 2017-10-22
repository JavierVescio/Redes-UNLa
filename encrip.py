from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64



def encrypt_val(clear_text,MASTER_KEY):
    enc_secret = AES.new(MASTER_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

    return cipher_text
def encrypt_md5(text):
    m = MD5.new()
    m.update(text) 
    return m.digest()

def decrypt_val(cipher_text,MASTER_KEY):
    dec_secret = AES.new(MASTER_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.rstrip("\0")
    return clear_val

def main():
    MASTER_KEY="mi_key_for_game_"
    encriptaion = encrypt_val("hola",MASTER_KEY)
    print "Dato= hola"
    print "encriptado= "+encriptaion
    desencriptacion = decrypt_val(encriptaion,MASTER_KEY)
    print "Desencriptado= "+desencriptacion
    print "En MD5= "+encrypt_md5("hola")
    

if __name__ == '__main__':
    main()

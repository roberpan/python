# -*- coding: utf-8 -*-
import rsa
import base64

plain='test'
verifycode='test'

#生成公私钥对
(public_key,private_key)=rsa.newkeys(2048)

#将公私钥存储为pem标准格式文件,公钥存在public.pem中，私钥存在private.pem中
pub=public_key.save_pkcs1()
print(pub)
pubfile=open('public.pem','w+')
pubfile.write(pub)
pubfile.close()

pri=private_key.save_pkcs1()
print(pri)
prifile=open('private.pem','w+')
prifile.write(pri)
prifile.close()

message=plain
with open('public.pem') as publicfile:
    p=publicfile.read()
    publickey=rsa.PublicKey.load_pkcs1(p)

with open('private.pem') as privatefile:
    p=privatefile.read()
    privatekey=rsa.PrivateKey.load_pkcs1(p)

def CypherWriter(base64code):
    f=open('Cyphertext.txt','w')
    f.write(base64code)
    f.close()

#数据加密流程，使用公钥进行加密，私钥解密
crypto=rsa.encrypt(message,publickey)
crypto64=base64.b64encode(crypto)
CypherWriter(crypto64)
print('The cyphertext is :')
print(crypto64)

crypto=base64.b64decode(crypto64)
message=rsa.decrypt(crypto,privatekey)
print('The code is: ')
print(message)

#进行认证，使用私钥加密，公钥解密
signature=rsa.sign(message,privatekey,'SHA-1')
rsa.verify(verifycode,signature,publickey)

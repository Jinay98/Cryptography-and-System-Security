from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import DES
import ast

def check(key, table):
    flag = 0
    index = -1
    for i in table:

        if i['entry'] == key:
            flag = 1
            index = i['index']
            break
    return flag, index
def encode(msg):
    #print(msg)
    table = []
    index=0
    c=-1
    counter=0
    for x in range(0,len(msg)):
        c += 1
        if c==len(msg):
            break
        else:
            key = ""
            #print("C value is = ",c)
            #print("char is ",msg[c])
            flag=1
            ind=0
            flag1=0
            while((flag!=0) and (c<=len(msg)-1)):
                key+=msg[c]
                #print("The key is ",key)
                flag,index=check(key,table)
                if(flag==1):
                    flag1=1
                    ind=index
                    c+=1
            #print("The flag value is =",flag)
            #print("The flag1 value is =",flag1)
            counter += 1
            if(flag1==0):
                info = {
                "encode": [0, key[-1]],
                "index": counter,
                "entry": key
                }
                table.append(info)
            else:
                info={
                    "encode":[ind,key[-1]],
                    "index":counter,
                    "entry":key
                }
                table.append(info)
            #print("Added in the table ",info)
    #print(table)
    enc=""
    for i in table:
        enc+=str(i['encode'][0])+i['encode'][1]
    print "After performing LZ78 zip value is = ",enc
    return table,enc


def returnvalue(table,index):
    val=""
    for i in table:
        if index==i['index']:
            val=i['entry']
    return val

def decode(table):
    msg=""
    dectable=[]
    counter=0
    for i in table:
        val=i['encode'][0]
        counter+=1
        if val==0:
            info={
              "output":i['encode'],
                "index":counter,
                "entry":i['encode'][1]
            }
            dectable.append(info)
        else:
            newentry=returnvalue(dectable,i['encode'][0])
            info = {
                "output": i['encode'],
                "index": counter,
                "entry": newentry+i['encode'][1]
            }
            dectable.append(info)
    #print(dectable)
    for i in dectable:
        msg+=i['entry']
    print("Decoded msg is ",msg)
    return msg


msg=str(input("enter the message"))
hash=SHA256.new(msg.encode('utf-8')).hexdigest()
print "The hash value of the message is",hash
print (type(hash))
random_generator=Random.new().read
key=RSA.generate(1024,random_generator)
pk=key.publickey()
print"The private key is ",pk
enc=pk.encrypt(hash.encode('utf-8'),32)
print "Encrypted Hash Value is ",enc
print type(enc[0])

decrypted = key.decrypt(ast.literal_eval(str(enc)))
print 'decrypted', decrypted

encstring=enc[0]
#encstring=encstring[2:len(encstring)-1]
print "encstring is = ",encstring
msg_ehash=msg+encstring
print "The message after appending the encrypted hash value is ",msg_ehash
table,zip_msg_ehash=encode(msg_ehash)
counter=0
while len(zip_msg_ehash)%8!=0:
    zip_msg_ehash+="0"
    counter+=1

des=DES.new('01234567',DES.MODE_ECB)
cipher_zip=des.encrypt(zip_msg_ehash)
print "After applying DES encryption we get",cipher_zip
# cipher_zip=(str(cipher_zip))[2:]
# print("The Zipped message after DES encryption is ",cipher_zip)
key1=RSA.generate(1024,random_generator)
puk=key1.publickey()
print"The public key of receiver is ",puk
enc_key=puk.encrypt('01234567'.encode('utf-8'),32)
print "Encrypted Key Value is ",enc_key[0]
# enc_key=str(puk.encrypt('01234567'.encode('utf-8'),32)[0])[2:]
# print ("Encrypted Key Value is ",enc_key)

print"Message sent to receiver is = ",cipher_zip+enc_key[0]
print("At the receiver side")
decrypted_session_key=key1.decrypt(ast.literal_eval(str(enc_key)))
print "Decrypted session key is",decrypted_session_key
plain_text=des.decrypt(cipher_zip)
#print "After DES Decryption we get = ",plain_text
plain_text=plain_text[0:len(plain_text)-counter]
print "After DES Decryption we get = ",plain_text
zipinv=decode(table)
print "After performing Zip inverse function",zipinv
zipinv=zipinv[len(msg):]
print "After performing Zip inverse function",zipinv
d=key.decrypt(zipinv)
print "Decryption generates ",d
ans=SHA256.new(zipinv).hexdigest()
# print "ans is ",ans
if d==hash:
    print "The two hash values match hence we achieve authentication and confidentiality"
#decmsg=decode(table)


'''
Output:
jinay@jinay:~/Desktop$ python PGP.py 
enter the message"jinay"
The hash value of the message is 1c03cdc9f0a00c5762960272e50cbd81b97ca3c15aa3604e358b5f2178c968b3
<type 'str'>
The private key is  <_RSAobj @0x7ff89ab57a70 n(1024),e>
Encrypted Hash Value is  ("\xa2J\xd2\x95\x823\xb9\xe7<\xf8\xc5!\xd9\xa0C\x00tRh\x1f\x00\x00\xf2s\x0cQ\x99e7\xed\x8e'\x8aP\x1c\xc5\xed|\xcc\xc097\xdb\xf7\x08(l\x0fM\xb6{;\xfa\\\x10A7=Q\xc9\x13\x8b\x8bh\x9d\x91D\xa4\x18\x8a\x0f($Knhy3:B\x84A\xd4\xc6\x8ez\x88\xca\xbe\xa3\xc5~\x01z\xcd\x8a\xb8\x84\xec\xe1\x93\x8a\x01.\t\x14k\x04\xe1\x05[\x9fi\x86.b\x84f\xd4~\x1a@@\x07\x1e\x9d8,",)
<type 'str'>
decrypted 1c03cdc9f0a00c5762960272e50cbd81b97ca3c15aa3604e358b5f2178c968b3
encstring is =  �Jҕ�3��<��!٠CtRh�s
                                   Q�e7��'�P��|��97�(lM�{;�\A7=Q���h��D��($Knhy3:B�A�Ǝz�ʾ��~z͊���ᓊ.	k�[�i�.b�f�~@@�8,
The message after appending the encrypted hash value is  jinay�Jҕ�3��<��!٠CtRh�s
 Q�e7��'�P��|��97�(lM�{;�\A7=Q���h��D��($Knhy3:B�A�Ǝz�ʾ��~z͊���ᓊ.	k�[�i�.b�f�~@@�8,
After performing LZ78 zip value is =  0j0i0n0a0y0�0J0�0�0�030�0�0<0�0�0!0�0�0C00t0R0h0210�0s0
              0Q0�0e070�0�0'0�0P016�0|0�0�0933�0�0(0l00M0�0{0;0�0\00A33=30�00�62h0�0�0D0�03748$0K3h530:0B0�58�0�35z0�0�0�0�16~00z0�37�76�0�0�370.0	00k0900[0�2�93b76f0�0~00@10706480,
After applying DES encryption we get ��,1��C|c��Q|yP7�e�����J�������k��Ǿ��3����Q�zʎ+(��Yp��k`7���IA�LK5�[,����^"7"L[�!��_���6xsu�0�ډm���g��od[���lM�Рi���te�Í���R�oVoK��	!�]�����9������d�h�d����`S�EH=���
�5��*{4�
�qvn��m�
The public key of receiver is  <_RSAobj @0x7ff89a4e8488 n(1024),e>
Encrypted Key Value is  �NDi	�m���v����~[oIy����B�Sg��'�ޘW�	�]�O�6��#���;N?�֯��Qw�Q��+�Ҟ��|ݙ��N��z��(�vъH�a��A��f}9�?�`�N�����4�1ydC
Message sent to receiver is =  ��,1��C|c��Q|yP7�e�����J�������k��Ǿ��3����Q�zʎ+(��Yp��k`7���IA�LK5�[,����^"7"L[�!��_���6xsu�0�ډm���g��od[��/���Р��lM,���te�Í���R�oVoK��	!�]�����9������d�h�d����`S�EH=���
�5��*{4�
�qvn��m݋NDi	�m���v����~[oIy����B�Sg��'�ޘW�	�]�O�6��#���;N?�֯��Qw�Q��+�Ҟ��|ݙ��N��z��(�vъH�a��A��f}9�?�`�N�����4�1ydC
At the receiver side
Decrypted session key is 01234567
After DES Decryption we get =  0j0i0n0a0y0�0J0�0�0�030�0�0<0�0�0!0�0�0C00t0R0h0210�0s0
       0Q0�0e070�0�0'0�0P016�0|0�0�0933�0�0(0l00M0�0{0;0�0\00A33=30�00�62h0�0�0D0�03748$0K3h530:0B0�58�0�35z0�0�0�0�16~00z0�37�76�0�0�370.0	00k0900[0�2�93b76f0�0~00@10706480,
('Decoded msg is ', "jinay\xa2J\xd2\x95\x823\xb9\xe7<\xf8\xc5!\xd9\xa0C\x00tRh\x1f\x00\x00\xf2s\x0cQ\x99e7\xed\x8e'\x8aP\x1c\xc5\xed|\xcc\xc097\xdb\xf7\x08(l\x0fM\xb6{;\xfa\\\x10A7=Q\xc9\x13\x8b\x8bh\x9d\x91D\xa4\x18\x8a\x0f($Knhy3:B\x84A\xd4\xc6\x8ez\x88\xca\xbe\xa3\xc5~\x01z\xcd\x8a\xb8\x84\xec\xe1\x93\x8a\x01.\t\x14k\x04\xe1\x05[\x9fi\x86.b\x84f\xd4~\x1a@@\x07\x1e\x9d8,")
After performing Zip inverse function jinay�Jҕ�3��<��!٠CtRh�s
                                                              Q�e7��'�P��|��97�(lM�{;�\A7=Q���h��D��($Knhy3:B�A�Ǝz�ʾ��~z͊���ᓊ.	k�[�i�.b�f�~@@�8,
After performing Zip inverse function �Jҕ�3��<��!٠CtRh�s
                                                         Q�e7��'�P��|��97�(lM�{;�\A7=Q���h��D��($Knhy3:B�A�Ǝz�ʾ��~z͊���ᓊ.	k�[�i�.b�f�~@@�8,
Decryption generates  1c03cdc9f0a00c5762960272e50cbd81b97ca3c15aa3604e358b5f2178c968b3
The two hash values match hence we achieve authentication and confidentiality
'''
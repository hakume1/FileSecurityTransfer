# coding:utf8

from Crypto.Cipher import AES

# 终端输出中文不乱码
def printCN(str1):
    print(str1.decode("utf8"))

def raw_inputCN(str1):
    return raw_input(str1.decode("utf8").encode("gbk"))


def file_encrypt():
    file_name=raw_inputCN("请输入要加密的文件名:\n")
    printCN("生成AES秘钥文件中......\n")

    file=open(file_name,'rb')       # 打开要加密文件
    file_msg=file.read()
    file_aes_key=open('AES_key','rb')   # 打开AES秘钥文件
    aes_key=file_aes_key.read()

    from Crypto.Cipher import AES
    from Crypto import Random
    # iv用来记录AES随机生成的一个16字节初始向量
    iv = Random.new().read(AES.block_size)   # 使用Crypto中Random模块,读取16字节数据作为iv的值，AES分块大小固定为16字节
    printCN("开始对原文件进行AES加密......")
    file_encrypted_msg,fill_number=aes_encrypt(file_msg,aes_key,iv)  # 调用AES加密函数  fill_number填充的位数
    file_encrypted=open('file_encrypted','wb')    # 生成存储加密后文件
    file_encrypted.write(file_encrypted_msg)
    file_encrypted.close()
    printCN("原文件AES加密完成！")
    file_fill_number=open('fill_number','wb')     # 生成存储填充位数文件
    file_fill_number.write(str(fill_number))
    file_fill_number.close()

    printCN("开始对原文件进行MD5摘要......")
    md5_msg=md5_encrypt(file_msg)
    printCN("MD5摘要完成！")
    file.close()                           # 已不用原文件，关闭

    printCN("生成你的RSA私钥文件中......\n")
    printCN("开始对MD5摘要签名")
    signature_msg=rsa_private_encrypt(md5_msg,'Alice_private_key')  # MD5摘要RSA加密
    printCN("MD5摘要签名完成！")
    printCN("对签名进行AES加密")         # 因为MD5值是32位的，所以AES16位一块的加密不需要填充数据
    signature_encrypted_msg,number=aes_encrypt(signature_msg,aes_key,iv)   # number仅用来接收一个值，没有其他作用
    file_signature_encrypted=open('file_signature_encrypted','wb')    # 生成存储加密后的签名文件
    file_signature_encrypted.write(signature_encrypted_msg)
    file_signature_encrypted.close()
    printCN("签名AES加密完成！")

    printCN("接收接收者RSA公钥文件中......\n")
    printCN("开始对AES秘钥进行RSA加密")
    aes_key_encrypted=rsa_public_encrypt(aes_key,'Bob_public_key')
    file_aes_key_encrypted=open('AES_key_encrypted','wb')
    file_aes_key_encrypted.write(aes_key_encrypted)
    file_aes_key_encrypted.close()
    printCN("AES秘钥RSA加密完成！")
    printCN("开始对iv进行RSA加密")
    iv_encrypted=rsa_public_encrypt(iv,'Bob_public_key')
    file_iv_encrypted=open('file_iv_encrypted','wb')
    file_iv_encrypted.write(iv_encrypted)
    file_iv_encrypted.close()
    printCN("对iv的RSA加密完成！")
    file_aes_key.close()

    printCN("加密过程结束！\n")
    printCN("发送给接收者的文件：")
    printCN("1.已加密文件：file_encrypted")
    printCN("2.加密后的AES秘钥文件：AES_key_encrypted")
    printCN("3.AES加密后的初始化向量文件：file_iv_encrypted")
    printCN("4.加密后的签名文件：file_signature_encrypted")
    printCN("5.填充位数文件：fill_number")
    return

def file_decrypt():

    file_aes_key_encrypted_name='AES_key_encrypted'
    iv_encrypted_name='file_iv_encrypted'
    file_rsa_private_key_name='Bob_private_key'
    file_aes_key_encrypted=open(file_aes_key_encrypted_name,'rb')
    aes_key_encrypted=file_aes_key_encrypted.read()
    file_iv_encrypted=open(iv_encrypted_name,'rb')
    iv_encrypted=file_iv_encrypted.read()

    printCN("开始解密AES秘钥......")
    aes_key=rsa_private_decrypt(aes_key_encrypted, file_rsa_private_key_name)
    printCN("AES秘钥解密完成！")
    printCN("开始解密AES初始化向量......")
    iv=rsa_private_decrypt(iv_encrypted,file_rsa_private_key_name)
    printCN("AES初始化向量解密完成！")
    file_encrypted_name='file_encrypted'
    file_encrypted=open(file_encrypted_name,'rb')
    file_encrypted_msg=file_encrypted.read()

    file_fill_number_name='fill_number'
    file_fill_number=open(file_fill_number_name,'rb')
    fill_number=file_fill_number.read()
    printCN("开始对加密文件进行AES解密")
    file_msg=aes_decrypt(file_encrypted_msg,aes_key,iv)
    file_msg=file_msg[0:len(file_msg)-int(fill_number)]     # 去掉AES加密时填充的位
    printCN("加密文件AES解密完成！")
    file_fill_number.close()
    file_decrypted=open('file_decrypted','wb')
    file_decrypted.write(file_msg)
    md5_file_msg=md5_encrypt(file_msg)
    file_decrypted.close()
    file_encrypted.close()

    printCN("已接收加密的签名文件！")
    file_signature_encrypted_name='file_signature_encrypted'
    file_signature_encrypted=open(file_signature_encrypted_name,'rb')
    signature_encrypted=file_signature_encrypted.read()
    printCN("加密签名文件AES解密")
    file_signature=aes_decrypt(signature_encrypted,aes_key,iv)
    printCN("加密签名文件AES解密完成！")
    file_signature_encrypted.close()
    file_aes_key_encrypted.close()
    file_iv_encrypted.close()

    sender_public_key_name='Alice_public_key'
    printCN("开始签名文件RSA解密")
    md5_decrypted=rsa_public_decrypt(file_signature,sender_public_key_name)
    printCN("签名文件RSA解密完成，得到原文件MD5值！")

    if md5_file_msg==md5_decrypted:   # MD5值校验
        printCN("MD5值校验成功！")
    else:
        printCN("MD5值校验失败，请重新传输或检查错误原因")

    printCN("解密程序运行完毕，请提取解密文件！")
    raw_inputCN("回车结束程序\n")

    return

# AES加密
def aes_encrypt(aes_file, key,iv):  # aes_file 文件，key 16-bytes 对称秘钥
    cipher = AES.new(key, AES.MODE_OFB,iv)   # 生成了加密时需要的实际密码,这里采用OFB模式
    # if fs is a multiple of 16
    x = len(aes_file) % 16
    printCN("要加密文件的长度是： %d"%len(aes_file))
    printCN("需要填充的数据长度 : %d"%((16- x)%16))
    if x != 0:
        aes_file_pad = aes_file + '0'*(16 - x) # It should be 16-x
    else:
        aes_file_pad=aes_file
    msg = cipher.encrypt(aes_file_pad)
    return msg,(16- x)%16

# AES解密
def aes_decrypt(aes_file, key,iv):
    cipher = AES.new(key, AES.MODE_OFB,iv)   # 生成了解密时需要的实际密码,这里采用OFB模式
    msg=cipher.decrypt(aes_file)
    return msg

# 计算MD5值
def md5_encrypt(md5_file):
    from Crypto.Hash import MD5
    msg = MD5.new()
    msg.update(md5_file)
    return msg.hexdigest()

# RSA私钥加密
def rsa_private_encrypt(msg,file_rsa_private_key_name):
    from M2Crypto import RSA
    rsa_private_key=RSA.load_key(file_rsa_private_key_name)
    msg_encrypted=rsa_private_key.private_encrypt(msg,RSA.pkcs1_padding)
    return msg_encrypted

# RSA公钥加密
def rsa_public_encrypt(msg,file_rsa_public_name):
    from M2Crypto import RSA
    rsa_public_key=RSA.load_pub_key(file_rsa_public_name)
    msg_encrypted=rsa_public_key.public_encrypt(msg,RSA.pkcs1_padding)
    return msg_encrypted

#  RSA私钥解密
def rsa_private_decrypt(msg,file_rsa_private_key_name):
    from M2Crypto import RSA    # 用M2Crypto下的RSA模块
    rsa_private_key=RSA.load_key(file_rsa_private_key_name)
    msg_decrypted=rsa_private_key.private_decrypt(msg,RSA.pkcs1_padding)
    return msg_decrypted

#  RSA公钥解密
def rsa_public_decrypt(msg,file_rsa_public_name):
    from M2Crypto import RSA    # 用M2Crypto下的RSA模块
    rsa_public_key=RSA.load_pub_key(file_rsa_public_name)
    msg_decrypted=rsa_public_key.public_decrypt(msg,RSA.pkcs1_padding)
    return msg_decrypted

from utils import PrpCrypt, Utils
from datetime import datetime

class GenerateLicense():
    def __init__(self, mac_addr, license_time):
        self.mac_addr = mac_addr
        self.license_time = license_time
        self.file_path = 'LICENSE'
        self.record_path = './records.txt'
        self.current_time = datetime.now().isoformat('T')

    def save_lic(self):
        psw = Utils().hash_msg('jerry' + str(self.mac_addr))  # 将mac地址加个字符串进行编译，增加破解难度，字符串自由定义

        license = {}
        license['mac'] = self.mac_addr
        license['license_time'] = self.license_time
        license['psw'] = psw
        print('license:', license)
        
        pc = PrpCrypt('keyskeyskeyskeys')  # 初始化密钥,可以为16位，32位，以及更长，一般为16位，加密解密都需要这个
        encrypted_license = pc.encrypt(str(license))  # 加密 <class 'bytes'>
        # decrypted_license = pc.decrypt(encrypted_license)  # 解密

        mac_str = self.mac_addr.replace(':', '')
        current_time = self.current_time.replace(':', '')
        file_path = self.file_path + '/license_'+ mac_str + '_' + current_time + '.lic'
        encrypted_license = str(encrypted_license, encoding = "utf-8")   #  bytes to str

        Utils().write_license(file_path, str(encrypted_license))

        record_msg = mac_str + " --->from " + self.current_time + " to " + license['license_time'] 
        Utils().write_license_record(self.record_path, record_msg)

if __name__ == "__main__":
    mac_addr = 'f0:2f:74:f3:9e:9e'
    license_time = '2022-09-11T10:03:15.447229'

    license = GenerateLicense(mac_addr, license_time)
    license.save_lic()
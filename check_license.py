# encoding: utf-8
import ast
from datetime import datetime
from utils import PrpCrypt, Utils

class CheckLicense():
    def __init__(self, lic_path):
        self.lic_path = lic_path

    def lic_decrypt(self, lic_path):
        encrpted_content = Utils().get_license_lic(lic_path)
        pc = PrpCrypt('keyskeyskeyskeys')
        d = pc.decrypt(encrpted_content)
        lic = ast.literal_eval(d)
        print(lic)
        return lic

    def check_psw(self):
        """
        check encoded password in user's license.
        :param psw: str, encoded password.
        :return: boolean, check result.
        """
        lic = self.lic_decrypt(self.lic_path)
        psw = lic['psw']

        mac_addr = Utils().get_mac_address()
        hashed_msg = Utils().hash_msg('jerry' + str(mac_addr))

        if psw == hashed_msg:
            return True
        else:
            return False
    def check_date(self, current_time):
        """
        check datetime in user's license.
        :param lic_date: str, license datetime.
        :return: boolean, if the active days smaller than current_time, return Flase.
        """
        lic = self.lic_decrypt(self.lic_path)
        lic_date = lic['license_time']

        current_time = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%S.%f")    # switch the str datetime to array.
        lic_date_array = datetime.strptime(lic_date, "%Y-%m-%dT%H:%M:%S.%f")    # the array type is datetime.datetime.
        remain_days = lic_date_array - current_time
        remain_days = remain_days.days
        return remain_days

if __name__ == '__main__':
    current_time = datetime.now().isoformat('T') # https://www.cnblogs.com/yyds/p/6369211.html    '2022-09-10T10:03:15.447229'
    # current_time = '2022-09-10T10:03:15.447229'
    # print(current_time)
    lic_path = 'LICENSE/license_f02f74f39e9e_2022-08-11T152437.166253.lic'
    checklicense = CheckLicense(lic_path)
    check_date_result = checklicense.check_date(current_time)
    print(check_date_result)

    check_psw_result = checklicense.check_psw()
    print(check_psw_result)

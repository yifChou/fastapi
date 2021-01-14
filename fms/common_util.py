import time,random
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")
def now_T():
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%S")
def ymd():
    return time.strftime("%Y%m%d")
def y_m_d():
    return time.strftime("%Y-%m-%d")
def y_m_d000():
    return time.strftime("%Y-%m-%d 00:00:00")
def time_str():
    return time.strftime("%Y%m%d%H%M%S")
def ymd_ms():
    return time.strftime("%Y%m%d%M%S")
def rand100_999():
    return str(random.randint(100, 999))
def rand1_9():
    return str(random.randint(1, 9))
def date_now():
    return time.strftime("%m%d")
def md5_32_upper(str):
    import hashlib
    # 待加密信息
    # 创建md5对象
    m = hashlib.md5()
    # Tips
    # 此处必须encode
    # 若写法为m.update(str) 报错为：Unicode-objects must be encoded before hashing
    # 因为python3里默认的str是unicode
    # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
    b = str.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest().upper()
    print('MD5加密前为 ：' + str)
    print('MD5加密后为 ：' + str_md5)
    return str_md5
def new_txt():
    file_name = "lading_number"+y_m_d()+".txt"
    with open(file_name, "a") as txt:
        txt.close()
    return file_name

def lading_generate():
    '''随机生成4位不重复的数值'''
    try:
        file_name = "lading_number" + y_m_d() + ".txt"
        with open(file_name, "a") as txt:
            txt.close()
        with open(file_name,"r+") as f:
            data = f.readlines()
            # for i in data:
            #     print(i)
            lading_number = random.randint(1000,9999)
            #print("txt",str(data))
            #print(str(ladings))
            if str(lading_number) not in str(data):
                f.writelines(str(lading_number)+"\n")
                return lading_number
            else:
                return lading_generate()
    except Exception as e:
        print(e,"生成单号重复多次")
        return random.randint(10000, 99999)
if __name__=="__main__":
    #file_name = new_txt()
    for i in range(10):
        print(lading_generate())

import shelve
import random
import time
def store_people(db,pid,input_yd_code,input_bag_code,input_yd_number,input_bag_numer):
    if if_exit_people(db,input_yd_number, input_bag_numer):
        tms_bag = {}
        tms_bag['yd_code'] = input_yd_code
        tms_bag['bag_code'] = input_bag_code
        tms_bag['yd_number'] = input_yd_number
        tms_bag['bag_numer'] = input_bag_numer
        db[pid] = tms_bag
        print("Store information: pid is %s, information is %s" % (pid, tms_bag))
        return 1
    else:
        return 0
def if_exit_people(db,input_yd_code,input_bag_code):
    flag = 1
    for key, value in db.items():
        print("打印所有item",key, value)
        if int(db[key]["yd_code"]) < input_yd_code < int(db[key]["yd_code"])+db[key]["yd_number"]:
            print("有重复运单起始号",input_yd_code)
            flag = 0
            break
        if int(db[key]["bag_code"]) < input_yd_code < int(db[key]["bag_code"])+db[key]["bag_numer"]:
            print("有重复袋子起始号",input_bag_code)
            flag = 0
            break
    if flag:
        return flag
    else:
        return flag

def update_people(db,pid,input_yd_code,input_bag_code):
    if pid in db.keys():
        if if_exit_people(db,input_yd_code,input_bag_code):
            value = db[pid]
            value['yd_code'] = input_yd_code
            value['bag_code'] = input_bag_code
            print("Pid %s's %s update information is %s" % (pid,"yd_code", input_yd_code))
            print("Pid %s's %s update information is %s" % (pid, "bag_code", input_bag_code))
        else:
            print("有重复，无法更新")
    else:
        print("Not found this number, can't update")
def lookup_people(db,pid):
    if pid in db.keys():
        value = db[pid]['yd_code']
        value2 = db[pid]['bag_code']
        print("Pid %s's %s is %s" % (pid, 'yd_code', value))
        print("Pid %s's %s is %s" % (pid, 'bag_code', value2))
    else:
        print('Not found this number')
def save_bag_record(input_yd_number,input_bag_numer):
    database = shelve.open('database202008.db', writeback=True)
    pid =new_pid(database, "tms_1")
    #yd_code = 4916402008173000
    #bag_code = 2081720
    start_yd = int(str(random.randint(1000, 9999)) + time.strftime("%Y%m%d", time.localtime()) + str(random.randint(1, 9)) + "000")
    start_bag = int(str(random.randint(10, 99)) + time.strftime("%Y%m%d", time.localtime())[2:] + str(random.randint(1, 9)) + "0")
    try:
        flag = store_people(database, pid, start_yd, start_bag,input_yd_number=input_yd_number,input_bag_numer=input_bag_numer)
        #update_people(database, pid+str(i), yd_code+i, bag_code+i)
        #lookup_people(database, pid+str(i))
        return flag,start_yd,start_bag
    finally:
        database.close()
def generate_ramdom(db):
    pass
def read_all(db_name):
    database = shelve.open(db_name+".db", writeback=True)
    print("打印所有item")
    for key, value in database.items():
        print("item",key, value)
def new_pid(db,pid):
    key_list = []
    flag = 1
    for key in db.keys():
        key_list.append(key)
    if len(key_list) == 0:
        return "tms_0"
    else:
        last_pid = key_list[-1]
        for key in db.keys():
            if key == pid:
                print("PID重复",key)
                flag = 0
                break
        if flag:
            newpid = pid
        else:
            pid1,pid2 = last_pid.split("_")
            newpid = pid1+ "_" + str(int(pid2)+1)
        return newpid
def store_batch(db,pid,input_batch_code,input_batch_number):
    if if_exit_batch(db,input_batch_code):
        tms_bag = {}
        tms_bag['batch_code'] = input_batch_code
        tms_bag['batch_number'] = input_batch_number
        db[pid] = tms_bag
        print("Store information: pid is %s, information is %s" % (pid, tms_bag))
        return 1
    else:
        return 0
def if_exit_batch(db,input_batch_code):
    flag = 1
    for key, value in db.items():
        print("打印所有item",key, value)
        if int(db[key]["batch_code"]) < input_batch_code < int(db[key]["batch_code"])+db[key]["batch_number"]:
            print("有重复批次起始号",input_batch_code)
            flag = 0
            break
    if flag:
        return flag
    else:
        return flag
def save_dts_batch_record(input_batch_number):
    database = shelve.open('dts_batch_number_202008.db', writeback=True)
    pid =new_pid(database, "dtsbatch_1")
    #input_batch_code = 20200821
    #input_batch_number = 10
    start_batch = int(str(random.randint(10, 99)) + time.strftime("%Y%m%d", time.localtime())[2:] + str(random.randint(10, 99)))
    try:
        flag = store_batch(database, pid,start_batch,input_batch_number )
        #update_people(database, pid+str(i), yd_code+i, bag_code+i)
        #lookup_people(database, pid+str(i))
        return flag,start_batch,input_batch_number
    finally:
        database.close()
if __name__ == "__main__":
    #save_bag_record(input_yd_number=10,input_bag_numer=20)
    a = save_dts_batch_record(10)
    read_all("dts_batch_number_202008")
    print(a)
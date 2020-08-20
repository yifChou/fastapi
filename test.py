import time
import random
start_yd = str(random.randint(100330,9999))+time.strftime("%Y%m%d", time.localtime())+str(random.randint(1,9))+"000"
start_bag =str(random.randint(10,99)) + time.strftime("%Y%m%d", time.localtime())[2:] +str(random.randint(1,9))+"0"
print(start_yd,start_bag)
#print(int(time.strftime("%Y%m%d", time.localtime())))
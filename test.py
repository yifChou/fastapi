import time
import random
# start_yd = str(random.randint(100330,9999))+time.strftime("%Y%m%d", time.localtime())+str(random.randint(1,9))+"000"
# start_bag =str(random.randint(10,99)) + time.strftime("%Y%m%d", time.localtime())[2:] +str(random.randint(1,9))+"0"
# print(start_yd,start_bag)
#print(int(time.strftime("%Y%m%d", time.localtime())))
import random
def random_list(start,end,number):
    a=[]
    for i in range(number):
        a.append(random.randint(start,end))
    print(a)
    return a
def maopao(a):
    for i in range(len(a)):
        for j in range(i,len(a)):
            if a[i]<=a[j]:
                a[i],a[j]=a[j],a[i]
    print(a)
def xiangtong(a):
    chongfu_dict = {}
    dict_key = set(a)
    for i in dict_key:
        sum = 0
        for j in a:
            if i == j:
                sum+=1
                # a.pop(j)
                # print(a)
                # length = length-1
        print(sum)
        chongfu_dict[i]=sum
    print(chongfu_dict)
    return chongfu_dict
def xiangtong2(a):
    chongfu_dict = {}
    dict_key = set(a)
    for i in dict_key:
        sum = a.count(i)
        print(sum)
        chongfu_dict[i]=sum
    print(chongfu_dict)
    return chongfu_dict

if __name__=="__main__":
    #maopao(random_list(10,99,10))
    # dict_result = xiangtong2(random_list(10,12,10))
    # print(sorted(dict_result.items(), key=lambda kv: kv[1]))
    # a = [15, 13, 14, 10, 14, 10, 10, 15, 13, 10]
    # b = [4, 2, 2, 2]
    # aa = dict(zip(a, b))
    # print(aa)
    a = random_list(10,20,5)
    b = a[::-1]
    c = sorted(a ,reverse=True)
    print(a,c)
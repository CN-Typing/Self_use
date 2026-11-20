import random
import time
list1 = ['3','4','5','up']
a = 0
weights=[0.916,0.072,0.006,0.006]
weights2=[0,0,0.5,0.5]
n=int(input('你想抽多少抽：'))
result=random.choices(list1,weights=weights)
print(result,end='')
for i in range(n):
    if '5' in result:
        weights=[0.916,0.072,0,0.012]
    if 'up' in result:
        print('\n恭喜出货\n一共%d抽' % a)
        weights = [0.916, 0.072, 0.006, 0.006]
        a=0
    a=a+1
    if a==179:
        result='[up]'
        print(result)
        print('\n恭喜保底\n一共180抽数')
    if a==90:
        result=random.choices(list1,weights=weights2)
        print(result)
        continue

    result=random.choices(list1,weights=weights)
    print(result,end='')
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
    print(msg)
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
            print("C value is = ",c)
            print("char is ",msg[c])
            flag=1
            ind=0
            flag1=0
            while((flag!=0) and (c<=len(msg)-1)):
                key+=msg[c]
                print("The key is ",key)
                flag,index=check(key,table)
                if(flag==1):
                    flag1=1
                    ind=index
                    c+=1
            print("The flag value is =",flag)
            print("The flag1 value is =",flag1)
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
            print("Added in the table ",info)
    print(table)
    enc=""
    for i in table:
        enc+=str(i['encode'][0])+i['encode'][1]
    print("Encoding is =",enc)
    return table
table=encode("abcdabcabcdaabcabce")

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
    print(dectable)
    for i in dectable:
        msg+=i['entry']
    print(msg)
decode(table)
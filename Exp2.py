from math import gcd
import random
def primRoots(p):
    roots = []
    required_set = set(num for num in range (1, p) if gcd(num, p) == 1)

    for g in range(1, p):
        actual_set = set(pow(g, powers) % p for powers in range (1, p))
        if required_set == actual_set:
            roots.append(g)
    return roots

p=int(input("Enter the prime no."))
print("List of primitive roots are",primRoots(p))
index=random.randint(0,len(primRoots(p))-1)
print("Random primitive root that is selected is :",primRoots(p)[index])
g=primRoots(p)[index]
privatekeys=[]
n=int(input("Enter the number of users"))
for i in range(n) :
    privatekeys.append(int(input('input the '+str(i+1)+' private key and it should be less than the prime number selected')))
print("The private keys are",privatekeys)
index1, index2 = map(int,input('Enter the number of the 2 users whose secret key has to be found').split())
print("Value of private key of person "+str(index1)+" is : ",privatekeys[index1-1])
print("Value of private key of person "+str(index2)+" is : ",privatekeys[index2-1])
R1=(g**privatekeys[index1-1])%p
R2=(g**privatekeys[index2-1])%p
print("Public key of person "+str(index1)+" is ",R1)
print("Public key of person "+str(index2)+" is ",R2)
S1=(R2**privatekeys[index1-1])%p
S2=(R1**privatekeys[index2-1])%p
print("Secret key value found out by person "+str(index1)+" when he calculates it using public key of person "+str(index2)+"("+str(R2)+") is :",S1)
print("Secret key value found out by person "+str(index2)+" when he calculates it using public key of person "+str(index1)+"("+str(R1)+") is :",S2)

'''Output:
Enter the prime no.19
List of primitive roots are [2, 3, 10, 13, 14, 15]
Random primitive root that is selected is : 13
Enter the number of users 7
input the 1 private key and it should be less than the prime number selected 5
input the 2 private key and it should be less than the prime number selected 4
input the 3 private key and it should be less than the prime number selected 3
input the 4 private key and it should be less than the prime number selected 2
input the 5 private key and it should be less than the prime number selected 7
input the 6 private key and it should be less than the prime number selected 8
input the 7 private key and it should be less than the prime number selected 9
The private keys are [5, 4, 3, 2, 7, 8, 9]
Enter the number of the 2 users whose secret key has to be found 2 4
Value of private key of person 2 is :  4
Value of private key of person 4 is :  2
Public key of person 2 is  4
Public key of person 4 is  17
Secret key value found out by person 2 when he calculates it using public key of person 4(17) is : 16
Secret key value found out by person 4 when he calculates it using public key of person 2(4) is : 16
'''
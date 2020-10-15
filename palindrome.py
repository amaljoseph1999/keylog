a=int(input("enter a no"))
b=a
s=0
while a!=0:
    r=a%10
    s=(s*10)+r
    a=int(a/10)
if b==s:
    print("palindrome")
else:
    print("not")

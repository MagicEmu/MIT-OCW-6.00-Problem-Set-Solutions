import math

count = 1
curr = 2
prime = True
i = 2
n = 10
sum = 0
while count <= n:
    while i<curr:
        if curr%i == 0:
            prime = False
            break
        i += 1
    if prime == True:
        curr += 1
        count += 1
        sum += math.log10(curr)
    else:
        prime = True
        curr += 1
    i = 2
print(n)
print(sum)
print(str(n)+":"+str(sum))


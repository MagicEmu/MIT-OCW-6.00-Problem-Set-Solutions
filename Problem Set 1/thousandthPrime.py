count = 1
curr = 2
prime = True
i = 2
while count <= 1000:
    while i<curr:
        if curr%i == 0:
            prime = False
            break
        i += 1
    if prime == True:
        print(str(count)+'th prime number:')
        print(curr)
        curr += 1
        count += 1
    else:
        prime = True
        curr += 1
    i = 2
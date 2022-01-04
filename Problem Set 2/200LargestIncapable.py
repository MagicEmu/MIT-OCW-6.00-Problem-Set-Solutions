want = 200
curr1 = 0
curr2 = 0
curr3 = 0
capable = False
while True:
    max1 = int(want / 20)
    max2 = int(want / 9)
    max3 = int(want / 6)
    capable = False
    curr1 = 0
    while curr1 <= max1:
        curr2 = 0
        while curr2 <= max2:
            curr3 = 0
            while curr3 <= max3:
                cur = curr1*20+curr2*9+curr3*6
                if cur == want:
                    capable = True
                    break
                curr3 += 1
            if capable == True:
                break
            curr2 += 1
        if capable == True:
            break
        curr1 += 1
    if capable == False:
        print(want)
        break
    want -= 1
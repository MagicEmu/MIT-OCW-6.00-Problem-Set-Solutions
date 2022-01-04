want = int(input("How many McNuggets would you like? "))
max1 = want//20
max2 = want//9
max3 = want//6
curr1 = 0
curr2 = 0
curr3 = 0
while curr1 <= max1:
    curr2 = 0
    while curr2 <= max2:
        curr3 = 0
        while curr3 <= max3:
            cur = curr1*20+curr2*9+curr3*6
            if cur == want:
                print(str(curr1) + " 20s " + str(curr2) + " 9s " + str(curr3) + " 6s")
            curr3 += 1
        curr2 += 1
    curr1 += 1
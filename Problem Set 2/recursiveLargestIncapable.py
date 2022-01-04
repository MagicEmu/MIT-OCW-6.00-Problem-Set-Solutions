def findIncapables(choice, curr1, curr2, curr3, max1, max2, max3):
    if curr1 > max1:
        return True
    if curr2 > max2:
        return findIncapables(choice, curr1+1, 0, 0, max1, max2, max3)
    if curr3 > max3:
        return findIncapables(choice, curr1, curr2+1, 0, max1, max2, max3)
    cur = curr1 * 20 + curr2 * 9 + curr3 * 6
    if cur == choice:
        return False
    return findIncapables(choice, curr1, curr2, curr3+1, max1, max2, max3)

want = int(input("How many examples of choices that we cannot perform would you like? "))
incapables = []
i = 1
while len(incapables) < want:
    if findIncapables(i, 0, 0, 0, want//20, want//9, want//6):
        incapables += [i]
    i += 1
print(incapables)

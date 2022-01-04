
def findCombinationsLock(want, curr20, curr9, curr6, max20, max9, max6):
    if curr20 > max20:
        return
    if curr9 > max9:
        return findCombinationsLock(want, curr20 + 1, 0, 0, max20, max9, max6)
    if curr6 > max6:
        return findCombinationsLock(want, curr20, curr9 + 1, 0, max20, max9, max6)
    cur = curr20 * 20 + curr9 * 9 + curr6 * 6
    if cur == want:
        return str(curr20) + " 20s " + str(curr9) + " 9s " + str(curr6) + " 6s"
    return findCombinationsLock(want, curr20, curr9, curr6 + 1, max20, max9, max6)


def findCombinationsList(want, choices, curr):
    mult = 0
    for i in range(len(curr)):
        mult += choices[i]*curr[i]
    if mult == want:
        return curr
    for i in range(len(curr)):
        if curr[i] > want//choices[i]:
            curr[i] = 0
            curr[i-1] += 1
    curr[-1] += 1
    return findCombinationsList(want, choices, curr)

def findCombinationsCount(want, choices, curr, count):
    if curr[0] == want//choices[0]:
        if choices[0]*curr[0] == want:
            return count+1
        else:
            return count
    mult = 0
    for i in range(len(curr)):
        mult += choices[i]*curr[i]
    if mult == want:
        count += 1
    changed = False
    for i in range(len(curr)):
        if curr[i] > want // choices[i]:
            curr[i] = 0
            curr[i - 1] += 1
            changed = True
    if changed == False:
        curr[-1] += 1
    return findCombinationsCount(want, choices, curr, count)


want = int(input("How much would you like? "))
count = findCombinationsCount(want, [5, 2, 1], [0, 0, 0], 0)
print(count)
def nestEggFixed(salary, save, growthRate, years):
    F = []
    F.append(salary * save * 0.01)
    for i in range(1, years):
        F.append(F[i-1] * (1 + 0.01 * growthRate) + salary * save * 0.01)
    return F


def testNestEggFixed():
    print(nestEggFixed(15000, 5, 5, 5))
    print(nestEggFixed(120000, 5, 10, 30))
    print(nestEggFixed(100000, 3, 1, 20))


def nestEggVariable(salary, save, growthRates):
    F = []
    F.append(salary * save * 0.01)
    for i in range(1, len(growthRates)):
        F.append(F[i-1] * (1 + 0.01 * growthRates[i]) + salary * save * 0.01)
    return F


def testNestEggVariable():
    print(nestEggVariable(15000, 5, [5, 4, 5, 3]))
    print(nestEggVariable(120000, 1, [1, 2, 3, 3, 4]))
    print(nestEggVariable(100000, 3, [3, 2, 2, 4, 1, 5]))


def postRetirement(savings, growthRates, expenses):
    F = []
    F.append(savings * (1 + 0.01 * growthRates[0]) - expenses)
    for i in range(1, len(growthRates)):
        F.append(F[i-1] * (1 + 0.01 * growthRates[i]) - expenses)
    return F


def testPostRetirement():
    print(postRetirement(2000000, [5, 4, 5, 3], 50000))
    print(postRetirement(10000000, [1, 2, 3, 3, 4], 1000000))
    print(postRetirement(6000000, [3, 2, 2, 4, 1, 5], 30000))


def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates, epsilon):
    F = nestEggVariable(salary, save, preRetireGrowthRates)
    savings = F[-1]
    high = F[-1]
    low = 0
    while low < high:
        middle = (high-low)/2+low
        F = postRetirement(savings, postRetireGrowthRates, middle)
        if abs(F[-1]) < epsilon:
            return middle
        elif F[-1] < 0:
            high = middle
        else:
            low = middle


def testFindMaxExpenses():
    print(findMaxExpenses(15000, 5, [5, 4, 5, 3], [5, 4, 5, 3], 0.01))
    print(findMaxExpenses(1200000, 1, [1, 2, 3, 3, 4], [1, 2, 3, 3, 4], 0.01))
    print(findMaxExpenses(1000000, 3, [3, 2, 2, 4, 1, 5], [3, 2, 2, 4, 1, 5], 0.01))


testFindMaxExpenses()
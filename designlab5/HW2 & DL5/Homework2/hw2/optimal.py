import lib601.optimize as optimize
def f1(x):
    return x*x - x

def f2(x):
    return x**5-7*x**3+6*x**2+2

def Finder(f, min, max, numsteps):
    print (optimize.optOverLine(f , min, max, numsteps))

Finder(f1 , -5, 5, 1000)
Finder(f2 , 1, 2, 100)

# >>> (-0.25, 0.499999999999938)
# >>> (-0.8815419423999984, 1.6600000000000006)
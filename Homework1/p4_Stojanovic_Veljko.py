import math
import matplotlib.pyplot as plt
import numpy as np

fun_str = input("Enter function with variable x: ")
ns = int(input("Enter the number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))

domain = (xmin, xmax)

def plot_function(fun_str, domain, ns):
    xmin = domain[0]
    xmax = domain[1]

    xs = list(np.linspace(xmin, xmax, ns))
    ys = []

    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print("{:>10} {:>10}".format("x", "y"))
    print("-" * 10)

    for i in range(len(xs)):
        print("{:>10.5f} {:>10.5f}".format(xs[i], ys[i]))
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.grid(True)
    plt.show()

plot_function(fun_str, domain, ns)
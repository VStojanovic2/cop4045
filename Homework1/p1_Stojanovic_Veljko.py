import math
import matplotlib.pyplot as plt
import numpy as np

while True:
         a = float(input("Enter the a: "))
         b = float(input("Enter the b: "))
         c = float(input("Enter the c: "))

         d = b**2 - 4*a*c

         if d < 0: 
            print("The equation has no real solutions.")
            x_opt = -b / (2*a)
            x_min = x_opt - 2
            x_max = x_opt + 2

         elif d == 0: 
            root1 = (-b + math.sqrt(d)) / (2*a)
            print("The equation has one real solution: ", root1)

            x_min = root1 - 2
            x_max = root1 + 2
         else:
            root1 = (-b + math.sqrt(d)) / (2*a)
            root2 = (-b - math.sqrt(d)) / (2*a)
            print("The equation has two real solutions: ", root1, " and ", root2)
            x_min = min(root1, root2) - 2
            x_max = max(root1, root2) + 2

         x = np.linspace(x_min, x_max, 150)
         y = a*x**2 + b*x + c
         plt.plot(x, y)
         plt.xlabel("x")
         plt.ylabel("y")
         plt.title("Quadratic Function")
         plt.grid(True)
         plt.show()

import math

def find_Pythagorean(n): 
    triples = []

    for a in range(1, n):
        for b in range(a, n):
            for c in range(1, n):
                if a**2 + b**2 == c**2:
                    triples.append((a, b, c))

    return triples

n = int(input("Enter the perimeter: "))
result = find_Pythagorean(n)
if result:
    print("The Pythagorean triple is:", result)
else:
    print("No Pythagorean triple found.")

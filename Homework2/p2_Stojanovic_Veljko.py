triples = [
    (a, b, c, d)
    for a in range(1,11)
    for b in range(1, 11)
    for c in range(1, 11)
    for d in range(1,11)
    if a !=b
    and a != c
    and a != d
    and b!= c
    and b != d
    and c!=d
    and a**2 + b**2 == c**2 + d**2
]

print("\nPart a:")
print(triples)

# Part b
words = ["One", "SEVEN", "three", "two", "Ten"]

short_words = [
    (word.lower(), len(word))
    for word in words
    if len(word) < 5
]

print("\nPart b:")
print(short_words)

# Part c
names = [
    "Christopher Ashton Kutcher",
    "Elizabeth Stamatina Fey"
]

formatted_names = [
    name.split()[0]
    + " "
    + name.split()[1][0]
    + ". "
    + name.split()[2]
    for name in names
]

print("\nPart c:")
print(formatted_names)


# Part d
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

anagrams = [
    (word1, word2)
    for word1 in lst1
    for word2 in lst2
    if sorted(word1.lower()) == sorted(word2.lower())
]

print("\nPart d:")
print(anagrams)


# Part e
s = ["one", "two", "three"]

lengths = {
    word: len(word)
    for word in s
}

print("\nPart e:")
print(lengths)


# Part f
text = "Hello world"

vowels = {
    i: text[i]
    for i in range(len(text))
    if text[i].lower() in "aeiou"
}

print("\nPart f:")
print(vowels)

print("Veljko Stojanovic")
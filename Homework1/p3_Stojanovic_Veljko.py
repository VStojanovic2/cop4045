s = input("Enter a string: ")
n = int(input("Enter the substring length: "))

def find_dup_str(s, n):
    for i in range(len(s) - n + 1):
        substring = s[i:i+n]
        for j in range(i + n, len(s) - n + 1):
            if substring == s[j:j+n]:
                return substring
    return ""

print(find_dup_str(s, n))

def find_max_dup(s):
    max_length = 0
    max_substring = ""
    for length in range(1, len(s) // 2 + 1):
        substring = find_dup_str(s, length)
        if substring and length > max_length:
            max_length = length
            max_substring = substring
    return max_substring

s = input("Enter a string: ")
print(find_max_dup(s))
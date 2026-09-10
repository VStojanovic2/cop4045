def caesar_cipher(text, shift):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ciphered_text = ""

    for character in text:
        if character in lowercase:
            index = lowercase.index(character)
            new_index = (index + shift) % 26
            ciphered_text += lowercase[new_index]

        elif character in uppercase:
            index = uppercase.index(character)
            new_index = (index + shift) % 26
            ciphered_text += uppercase[new_index]

        else:
            ciphered_text += character

    return ciphered_text


def caesar_decipher(ciphertext, shift):
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = {}

    for letter in alphabet:
        frequencies[letter] = 0

    for character in text:
        character = character.lower()

        if character in alphabet:
            frequencies[character] += 1

    return frequencies


def main():
    while True:
        print("\nCaesar Cipher Menu")
        print("1. Encrypt a message")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            message = input("Enter a message: ")
            shift = int(input("Enter the shift value: "))

            ciphered_text = caesar_cipher(message, shift)
            print("\nCiphered text:", ciphered_text)

            frequencies = letter_frequency(ciphered_text)

            print("\nLetter frequencies:")
            for letter in frequencies:
                print("{}: {}".format(letter, frequencies[letter]))

            deciphered_text = caesar_decipher(ciphered_text, shift)
            print("\nDeciphered text:", deciphered_text)

        elif choice == "2":
            print("Program finished.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
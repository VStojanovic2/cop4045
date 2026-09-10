import unittest

from p5_Stojanovic_Veljko import (
    caesar_cipher,
    caesar_decipher,
    letter_frequency
)


class TestCaesarCipher(unittest.TestCase):

    def test_caesar_cipher_lowercase(self):
        self.assertEqual(caesar_cipher("hello", 3), "khoor")

    def test_caesar_cipher_uppercase(self):
        self.assertEqual(caesar_cipher("HELLO", 3), "KHOOR")

    def test_caesar_cipher_mixed_case(self):
        self.assertEqual(caesar_cipher("Hello World", 3), "Khoor Zruog")

    def test_caesar_decipher(self):
        self.assertEqual(caesar_decipher("Khoor Zruog", 3), "Hello World")

    def test_spaces_and_punctuation(self):
        self.assertEqual(
            caesar_cipher("Hello, World!", 3),
            "Khoor, Zruog!"
        )

    def test_letter_frequency(self):
        expected = {
            "a": 2,
            "b": 1,
            "c": 0,
            "d": 0,
            "e": 0,
            "f": 0,
            "g": 0,
            "h": 0,
            "i": 0,
            "j": 0,
            "k": 0,
            "l": 0,
            "m": 0,
            "n": 0,
            "o": 0,
            "p": 0,
            "q": 0,
            "r": 0,
            "s": 0,
            "t": 0,
            "u": 0,
            "v": 0,
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0
        }

        self.assertEqual(letter_frequency("Aab! 123"), expected)


if __name__ == "__main__":
    unittest.main()
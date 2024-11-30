def caesar_cipher(text, shift):
    result = ""

    # Traverse the text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters in plain text
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)

        # Encrypt lowercase characters in plain text
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)

        # Handle non-alphabet characters without changing them
        else:
            result += char

    return result
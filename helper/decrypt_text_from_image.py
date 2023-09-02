def bin_to_ascii(binary):
    ascii = int(f"{binary}", 2)
    byte_number = ascii.bit_length() + 7 // 8
    binary_array = ascii.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text

# example
print(bin_to_ascii(11000010110001001100011))


def decrypt(image):
    """Sample function"""
    pass


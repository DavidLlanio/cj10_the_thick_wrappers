from PIL import Image

def bin_to_ascii(binary):
    ascii = int(f"{binary}", 2)
    byte_number = ascii.bit_length() + 7 // 8
    binary_array = ascii.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text

# example
print(bin_to_ascii(11000010110001001100011)) # "abc"


def decrypt(image):
    img = Image.open(image)
    pixels = img.load() 
    print(pixels)
    width, height = img.size
    def pixel_to_hex(x, y):
        if img.mode == 'RGBA':
            r, g, b, a = pixels[x, y]
            return r, g
        else:
            r, g, b = pixels[x, y]
            return r, g
    return pixel_to_hex
    

print(decrypt("/Users/maxencegilloteaux/Desktop/secret_image1_unscrambledcopy.png")(200, 50))
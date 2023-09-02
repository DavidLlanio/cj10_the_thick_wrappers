from PIL import Image

def bin_to_ascii(binary):
    ascii = int(f"{(binary)}", 2)
    byte_number = ascii.bit_length() + 7 // 8
    binary_array = ascii.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text

# example
print(bin_to_ascii(11000010110001001100011)) # "abc"
print(bin_to_ascii("0101010001101111011100100110111101101110011101000110111100100000010000110110000101101110011000010110010001100001")) # Toronto Canada

def decrypt(image):
    img = Image.open(image)
    pixels = img.load() 
    print(pixels)
    width, height = img.size
    pixel_list = []

    def pixel_to_bin(x, y):
        if img.mode == 'RGBA':
            r, g, b, a = pixels[x, y]
            r, g, b = int(str(bin(r))[2:]), int(str(bin(g))[2:]), int(str(bin(b))[2:])
            return r, g, b
        
        else:
            r, g, b = pixels[x, y]
            r, g, b = int(str(bin(r))[2:]), int(str(bin(g))[2:]), int(str(bin(b))[2:])
            return r, g, b
    
    def decrypt_each_pixel():
        for y in range(height):
            for x in range(width):
                rgb_val = pixel_to_bin(x, y)
                pixel_list.append(rgb_val)

    decrypt_each_pixel()

    return pixel_list
    

# print(decrypt("/Users/maxencegilloteaux/Desktop/secret_image1_unscrambledcopy.png"))
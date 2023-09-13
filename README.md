# In Plain Pixel
Created by "The Thick Wrappers" (github: DavidLlanio, maxence-glt, standard-affect, Jaavv, Robin5605) for the Python Discord 2023 CodeJam

## In Brief
In Plain Pixel is a Steganogrpahy application built completely with Python. Through this application, you are able to encrypt a valid input method (see below) into an image of your choice, or decrypt an image created through this application by simply inputting your decrypted image.

The following input types are supported for encryption:
- Typed Text
- Text File (*.txt)
- Image File (*.jpg, *.jpeg, *.png)

## What is Steganography?
Imagine you want to pass a note to your friend in a crowded library, but don't want to draw attention to the contents of the note or the note itself. Maybe you hide the message you want to pass in something inconspicuous like in the margins of a book or between the lines of sentences. In essence, you're hiding your message in plain sight.

[Steganography](https://en.wikipedia.org/wiki/Steganography) is similar to this concept, but with digital media, like pictures!

With steganography, you can hide something like a text message in a picture. You can even hide a picture in another picture!

### How does it work?

Computers only understand ones and zeros. Let's say a pixel in an RGB digital image has the integer values of [255, 255, 255], representing white.

255 in binary is 11111111
So the entire pixel is: [11111111, 11111111, 11111111]

With steganography, you can hide something in the [least significant bits](https://www.analog.com/en/design-center/glossary/lsb.html#:~:text=Least%2Dsignificant%20bit.,is%20the%20furthest%2Dright%20bit.) of this pixel. For example, let's hide the letter "H" in this pixel.

The [ASCII](https://www.asciitable.com/) code of the letter "H" is: 72 (decimal) or 1001000 (binary)

We can split up the binary of the ASCII for "H" into 3 parts:
- 1
- 001
- 000

Then clear and set the least significant bits of the pixel RGB values:
- R: 11111111 -> 11111000
- G: 11111111 -> 11111001
- B: 11111111 -> 11111111 (Last bit stays the same)

With these changes, the letter "H" is now hidden in the image with little impact to the image itself.

### How are we using Steganography?
The previous example features our method of hiding text in an image. We split the character's binary into 3 parts and hide the most significant bit in the lease significant bit of the blue channel, the 3 middle bits in the 3 least significant bits of the green channel, and the 3 least significant bits in the 3 least significant bits of the red channel.

We do this process for every character in the word, sentence, or paragraph.

For image inputs, we place the 4 most significant bits of the RGB channels of every pixel of the image you want to hide into the 4 least significant bits of the RGB channels of every pixel of the image you want to use as the cover.

When you decrypt an image inside of another image, you will get a lower quality version of the original image you wanted to hide because we cannot reproduce the least significant bits of the original image.

## How to Set up
- Download and unzip the repository, or clone it
- Use the change directory command into the repository at the level of main.py
```
cd cj10_the_thick_wrappers
```
- Install the dependencies:
```
python3 -m pip install -r dev-requirements.txt
```
## How to Start and Use GUI
After setup, run the main.py file to start the GUI:
```
python3 main.py
```

Sample use of GUI:

Encrypting text into an image

![In Plain Pixel](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExenhtZHU1cGp2MmExZnk4NmZqcHV0ZHhmNHQ2ZWFsNWozdmFzbGJ4OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O7yq741e0EFZ4lLxpW/giphy.gif)

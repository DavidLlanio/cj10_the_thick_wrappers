import io
import os
import re
from dataclasses import dataclass

from nicegui import app, events, ui
from PIL import Image

from helper.decrypt_text_from_image import binary_decoder
from helper.encrypt_text import encrypt_text
from helper.Steganographizer import Steganographizer


@dataclass
class Filepaths:
    """Class that has file paths of user image, cover image, and output files"""

    user_image_fe = ""
    cover_image_fe = ""

    def get_user_image_fp(self):
        """Get file path for user iamge"""
        return os.path.join("static", f"user_image.{self.user_image_fe}")

    def get_cover_image_fp(self):
        """Get file path for cover image"""
        return os.path.join("static", f"cover_image.{self.cover_image_fe}")

    def get_encrypted_image_output_path(self):
        """Get file path for encrypted output image"""
        return os.path.join("static", f"output.{self.cover_image_fe}")

    def get_decrypted_output_file_path(self, text=False):
        """Get file path for decrypted output, either an image or text file"""
        if text:
            return os.path.join("static", "output.txt")
        else:
            return os.path.join("static", f"output.{self.cover_image_fe}")


def placeholder_function(*args, **kwargs):  # noqa: D103
    return [None, None]


# GUI callback functions
def show_output():
    """Creates dialog with output"""
    text_output_fp = file_paths.get_decrypted_output_file_path(text=True)
    image_output_fp = file_paths.get_decrypted_output_file_path()
    # If there is output use that as the content of the markdown
    if os.path.exists(image_output_fp):
        with ui.dialog() as dialog, ui.card():
            ui.label("Image Output")
            ui.markdown(f"![output]({image_output_fp})")
            with ui.row():
                ui.button("Download", on_click=lambda: ui.download(image_output_fp))
                ui.button("Close", on_click=dialog.close)
        dialog.open()
    elif os.path.exists(text_output_fp):
        with open(text_output_fp, "r") as o:
            text = o.read()
        with ui.dialog() as dialog, ui.card():
            ui.label("Text Output")
            ui.markdown(f"{text}")
            with ui.row():
                ui.button("Close", on_click=dialog.close)
        dialog.open()
    else:
        ui.notify("Something went wrong, please try again.")


def handle_image_upload(img: events.UploadEventArguments, cover=False):
    """Handle user image to encrypt.

    This function will take the image that was uploaded by the user
    and put it in the static file folder of the repository as
    user_image.(file extension of original image)
    or
    cover_image.(file extension of original image)

    param img: object that has uploaded file
    """
    # Get the binary of the tempfile object
    content = img.content.read()
    # Create a pillow image object using the binary
    with Image.open(io.BytesIO(content)) as image:
        image.load()
        rgb_image = image.convert("RGB")
    # Get the extension using regex and check that it is valid
    acceptable_extensions = ["jpg", "png", "jpeg"]
    file_extension = re.search(r"\.([a-zA-Z0-9]+)$", img.name).group(1)
    if file_extension not in acceptable_extensions:
        ui.notify("Not an acceptable file type!")
        return
    # Save the image locally if the file extension is valid
    if cover:
        file_paths.cover_image_fe = "png"
        fp = file_paths.get_cover_image_fp()
    else:
        file_paths.user_image_fe = "png"
        fp = file_paths.get_user_image_fp()
    rgb_image.save(fp, format="PNG")


def encrypt_event(e: events.ClickEventArguments, value: str, text_input: str = None):
    """Function that checks if conditions for encryption are met and calls encrypt fucntion

    This function will check whether text or image is being encrypted into the cover_iamge.
    If it is an image it will first check if the user_image is smaller or equal
    in size to cover_image. If user_image is too large it will resize it to be the same
    size as the cover_image. Then, the appropriate function will be called to encrypt
    either the text or image into the cover_image. The output image will be saved in static
    folder as output_image.(cover image file extension)

    param e: GUI objects for click event.
    param value: String with type of message will be encrypted. Will be "Text" or "Image".
    param text_input: Message to be encrypted into image
    """
    # File paths for all images
    user_image_fp = file_paths.get_user_image_fp()
    cover_image_fp = file_paths.get_cover_image_fp()
    encrypt_output_image_fp = file_paths.get_encrypted_image_output_path()
    text_output_fp = file_paths.get_decrypted_output_file_path(text=True)
    image_output_fp = file_paths.get_decrypted_output_file_path()
    # Open the cover image
    with Image.open(cover_image_fp) as cimg:
        cimg.load()
    # Check if user image is larger than cover image, resize if it is
    if value == "Image":
        # Open user image
        with Image.open(user_image_fp) as uimg:
            uimg.load()
        # Check sizes
        if uimg.size[0] > cimg.size[0] and uimg.size[1] > cimg.size[1]:
            uimg = uimg.resize(cimg.size)
        # Call function to encrypt user image into cover image
        output_image = Steganographizer(cimg, uimg)
        output_image.encrypt_image()
        # Remove output file if it exists
        if os.path.exists(image_output_fp):
            os.remove(image_output_fp)
        elif os.path.exists(text_output_fp):
            os.remove(text_output_fp)
        # Save the output image
        output_image.save_image(encrypt_output_image_fp)
    elif value == "Text":
        # Check if there is text Input
        if text_input:
            # Call function to encrypt text into cover image
            output_image = encrypt_text(text_input, cimg)
            # Check return value in case text is too long
            if output_image is None:
                ui.notify("Text message is too long for image!")
                return
            # Remove output file if it exists
            if os.path.exists(image_output_fp):
                os.remove(image_output_fp)
            elif os.path.exists(text_output_fp):
                os.remove(text_output_fp)
            # Save the output image
            output_image.save(encrypt_output_image_fp)
        else:
            ui.notify("Please input a text message to encrypt!")
            return
    show_output()


def decrypt_event():
    """Function that does procedures for decryption

    Loads up the cover_image gotten from the user
    and calls the decrypt functions. If the text funciton detects text
    a text file with the decrypted message will be saved as a text file.
    Otherwise, the decrypted image will be saved.
    """
    # File path of cover image
    cover_image_fp = file_paths.get_cover_image_fp()
    text_output_fp = file_paths.get_decrypted_output_file_path(text=True)
    image_output_fp = file_paths.get_decrypted_output_file_path()
    # Open the cover image
    with Image.open(cover_image_fp) as cimg:
        cimg.load()
    # Call the function to decrypt text from image
    decrypt_text, end_code_found = binary_decoder(cimg)
    # Save output as text file
    if end_code_found:
        # Remove output file if it exists
        if os.path.exists(image_output_fp):
            os.remove(image_output_fp)
        # Create new output file
        with open(text_output_fp, "w") as f:
            f.write(decrypt_text)
    else:
        # Remove output file if it exists
        if os.path.exists(text_output_fp):
            os.remove(text_output_fp)
        # Call the function to decrypt an image from an image
        decrypt_image = placeholder_function(cimg)
        # Save output as an image
        decrypt_image.save(image_output_fp)
    show_output()


# GUI Contents

# Create Filepaths object to keep track of file paths
file_paths = Filepaths()

# Add static files folder
app.add_static_files("/static", "static")

# Title of the project
ui.label("The Thick Wrappers Steganography Project")

# Prompt user to choose whether to encrypt or decrypt
ui.label("Select Encrpyt/Decrypt:")
dropdown_encrypt_or_decrypt = ui.select(["Encrypt", "Decrypt"], value="Encrypt")

# Card with user input needed for encrypt with encrypt button
with ui.card().bind_visibility_from(dropdown_encrypt_or_decrypt, "value", value="Encrypt"):
    # Prompt the user to select the message type
    with ui.row():
        ui.label("Choose message type:")
        dropdown_text_or_image = ui.select(["Text", "Image"], value="Text")
    # User input needed if text message type is chosen
    with ui.column().bind_visibility_from(dropdown_text_or_image, "value", value="Text"):
        # Prompt the user for the text they want to encrypt into cover image
        with ui.row():
            with ui.column():
                ui.label("Enter Text:")
            with ui.column():
                text_to_encrypt = ui.textarea(label="Message", placeholder="Hello World")
        # Prompt the user for the image they want to encrypt a message into
        with ui.row():
            with ui.column():
                ui.label("Enter Cover Image:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=lambda e: handle_image_upload(e, cover=True))
        with ui.row():
            encrypt_text_button = ui.button("Encrypt", on_click=lambda e:
                                            encrypt_event(e, dropdown_text_or_image.value, text_to_encrypt.value))
    # User input needed if image message type is chosen
    with ui.column().bind_visibility_from(dropdown_text_or_image, "value", value="Image"):
        # Prompt the user for the image they want to encrypt into cover image
        with ui.row():
            with ui.column():
                ui.label("Enter Image to Encrypt:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=handle_image_upload)
        # Prompt the user for the image they want to encrypt a message into
        with ui.row():
            with ui.column():
                ui.label("Enter Cover Image:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=lambda e: handle_image_upload(e, cover=True))
        with ui.row():
            encrypt_image_button = ui.button("Encrypt", on_click=lambda e:
                                             encrypt_event(e, dropdown_text_or_image.value))

# Card with user input needed for decrypt with decrypt button
with ui.card().bind_visibility_from(dropdown_encrypt_or_decrypt, "value", value="Decrypt"):
    with ui.column():
        # Prompt the user for the image they want to decrypt
        with ui.row():
            with ui.column():
                ui.label("Enter Image to Decrypt:")
            with ui.column():
                ui.upload(auto_upload=True, on_upload=lambda e: handle_image_upload(e, cover=True))
        with ui.row():
            ui.button("Decrypt", on_click=decrypt_event)

# Initialize and run the GUI
ui.run()

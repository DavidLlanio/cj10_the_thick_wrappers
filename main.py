import os
import re

from nicegui import events, ui


# GUI helper functions
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
    # Get the extension using regex and check that it is valid
    acceptable_extensions = ["jpg", "png", "jpeg"]
    file_extension = re.search(r"\.([a-zA-Z0-9]+)$", img.name).group(1)
    if file_extension not in acceptable_extensions:
        ui.notify("Not an acceptable file type!")
        return
    # Save the image locally if the file extension is valid
    if cover:
        file_path = os.path.join("static", f"cover_image.{file_extension}")
    else:
        file_path = os.path.join("static", f"user_image.{file_extension}")
    with open(file_path, "wb") as f:
        f.write(content)


def encrypt_event():
    """Function that checks if conditions for encryption are met and calls encrypt fucntion

    This function will check whether text or image is being encrypted into the cover_iamge.
    If it is an image it will first check if the user_image is smaller or equal
    in size to cover_image. If user_image is too large it will resize it to be the same
    size as the cover_image. Then, the appropriate function will be called to encrypt
    either the text or image into the cover_image. The output image will be saved in static
    folder as output_image.(cover image file extension)
    """
    # TODO: Check whether it is text or image encryption
    # TODO: Check if user_image is larger than cover image, resize if it is
    # TODO: Call appropriate function to encrypt either text or image
    # TODO: Save the image in static as output_image


def decrypt_event():
    """Function that does procedures for decryption

    Loads up the cover_image gotten from the user
    and calls the decrypt functions. This will output
    the decrypt function outputs into files for display
    in GUI.
    """
    # TODO: Call the function to decrypt text from image
    # TODO: Call the function to decrypt an image from image
    # TODO: Output resulst to output.txt and output.(file extension of cover image)


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
            ui.button("Encrypt", on_click=lambda: ui.notify("Encrypted!"))
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
            ui.button("Encrypt", on_click=lambda: ui.notify("Encrypted!"))

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
            ui.button("Decrypt", on_click=lambda: ui.notify("Decrypted!"))

# Output area
output = ui.image("https://picsum.photos/id/377/640/360")

# Buttons to download or clear output
with ui.row():
    download_button = ui.button("Download", on_click=lambda: ui.notify("Downloaded!"))
    clear_button = ui.button("Clear")

# Initialize and run the GUI
ui.run()

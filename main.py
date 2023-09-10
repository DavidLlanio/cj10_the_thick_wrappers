import io
import os
from dataclasses import dataclass

from nicegui import app, events, ui
from PIL import Image, UnidentifiedImageError

from helper.constant import ResizeMode
from helper.decrypt import decrypt_image_from_image, decrypt_text_from_image
from helper.encrypt import encrypt_image_to_image, encrypt_text_to_image
from helper.utility import exif_embed_ipp, image_resize

InvalidFileError = (OSError, UnidentifiedImageError)


@dataclass
class Filepaths:
    """Class that has file paths of user image, cover image, and output files"""

    user_text_fe = "txt"
    user_image_fe = ""
    cover_image_fe = ""

    def get_user_text_fp(self):
        """Get file path for user upload text"""
        return os.path.join("static", f"user_text.{self.user_text_fe}")

    def get_user_image_fp(self):
        """Get file path for user image"""
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


@dataclass
class TailwindStyling:
    """Class that contains all the curated styling chosen for GUI components"""

    # Layout styling
    header_row = "flex items-center justify-center relative px-4"
    center_card = "absolute top-1/2 left-1/2 transform -translate-x-1/2 \
    -translate-y-1/2 p-8 rounded-lg shadow-md max-w-md"
    button_row = "flex"

    # Text styling
    title_text = "text-2xl font-bold"
    prompt_text_h = "text-base py-5"
    prompt_text_v = "text-base"

    # Input element styling
    button_center = "mx-auto"
    dark_mode_switch = "absolute right-4"


# GUI callback functions
def show_output():
    """Creates dialog with output"""
    text_output_fp = file_paths.get_decrypted_output_file_path(text=True)
    image_output_fp = file_paths.get_decrypted_output_file_path()
    # If there is output use that as the content of the markdown
    if os.path.exists(image_output_fp):
        with ui.dialog() as dialog, ui.card():
            ui.label("Image Output").tailwind(styles.prompt_text_v)
            ui.markdown(f"![output]({image_output_fp})")
            with ui.row():
                ui.button("Download", on_click=lambda: ui.download(image_output_fp))
                ui.button("Close", on_click=dialog.close)
        dialog.open()
    elif os.path.exists(text_output_fp):
        with open(text_output_fp, "r") as o:
            text = o.read()
        with ui.dialog() as dialog, ui.card():
            ui.label("Text Output").tailwind(styles.prompt_text_v)
            ui.markdown(f"{text}")
            with ui.row():
                ui.button("Close", on_click=dialog.close)
        dialog.open()
    else:
        ui.notify("Something went wrong, please try again.")


def handle_text_file_upload(file: events.UploadEventArguments) -> str | None:
    """Read a text file selected as an encryption message"""
    # Try to parse file as text, aborting if this fails
    with file.content as f:
        bytes = f.read()
    try:
        text = bytes.decode("utf-8")
    except UnicodeDecodeError:
        ui.notify("File could not be read correctly")
        text_upload.reset()
        return
    # Write to storage file
    with open(file_paths.get_user_text_fp(), "w") as f:
        f.write(text)


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
    try:
        with Image.open(io.BytesIO(content)) as image:
            image.load()
            rgb_image = image.convert("RGB")
    except UnidentifiedImageError:
        ui.notify("Could not load image!")
        if cover:
            if dropdown_text_or_image.value == "Text":
                cover_image_upload_text.reset()
            else:
                cover_image_upload_image.reset()
        else:
            secret_image_upload.reset()
        return
    # Get the extension and check that it is present and valid
    acceptable_extensions = ["jpg", "png", "jpeg"]
    file_extension = os.path.splitext(img.name)[1]
    if not file_extension or file_extension[1:] not in acceptable_extensions:
        ui.notify("Not an acceptable file type!")
        return
    file_extension = file_extension[1:]
    # Save the image locally if the file extension is valid
    if cover:
        file_paths.cover_image_fe = "png"
        fp = file_paths.get_cover_image_fp()
    else:
        file_paths.user_image_fe = "png"
        fp = file_paths.get_user_image_fp()
    rgb_image.save(fp, format="PNG")


def encrypt_event(
    e: events.ClickEventArguments,
    value: str,
    upload: str,
    text_input: str | None = None,
):
    """Function that checks if conditions for encryption are met and calls encrypt fucntion

    This function will check whether text or image is being encrypted into the cover_image.
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
    try:
        with Image.open(cover_image_fp) as cimg:
            cimg.load()
    except InvalidFileError:
        ui.notify("Cover image file cannot be read!")
        cover_image_upload_image.reset()
        return
        # Check if user image is larger than cover image, resize if it is
    if value == "Image":
        # Open user image
        try:
            with Image.open(user_image_fp) as uimg:
                uimg.load()
        except InvalidFileError:
            ui.notify("Encryption image file cannot be read!")
            secret_image_upload.reset()
            return
        # Check sizes
        if uimg.size[0] > cimg.size[0] or uimg.size[1] > cimg.size[1]:
            with ui.dialog() as dialog, ui.card():
                ui.label(
                    "The image you want to encrypt is larger than the cover \
                         image in one or both dimensions. It will be resized."
                )
                with ui.row():
                    ui.button("Continue", on_click=dialog.close)
            dialog.open()
        # Call function to encrypt user image into cover image
        resized_uimg = image_resize(uimg, cimg.size, ResizeMode.SHRINK_TO_SCALE)
        user_image_exif_data = resized_uimg.getexif()
        new_exif_data = exif_embed_ipp(user_image_exif_data, resized_uimg.size)
        output_image = encrypt_image_to_image(cimg, resized_uimg)
        # Remove output file if it exists
        if os.path.exists(image_output_fp):
            os.remove(image_output_fp)
        elif os.path.exists(text_output_fp):
            os.remove(text_output_fp)
        # Save the output image
        output_image.save(encrypt_output_image_fp, exif=new_exif_data)
    elif value == "Text":
        # Check if there is text input, possibly from user-provided file
        if upload == "Read Text from File":
            try:
                with open(file_paths.get_user_text_fp()) as f:
                    text_input = f.read()
            except FileNotFoundError:
                ui.notify("Text input file not found!")
                text_upload.reset()
                return
            except OSError:
                ui.notify("Error reading text input!")
                text_upload.reset()
                return

        # Call function to encrypt text into cover image
        output_image = encrypt_text_to_image(text_input, cimg)
        # Check return value in case text is too long
        if output_image is None:
            ui.notify("Text message is too long for image!")
            text_upload.reset()
            return
        # Only remove input if encryption succeeded
        text_fp = file_paths.get_user_text_fp()
        if os.path.exists(text_fp):
            os.remove(text_fp)
            text_upload.reset()
        # Remove output file if it exists
        if os.path.exists(image_output_fp):
            os.remove(image_output_fp)
        elif os.path.exists(text_output_fp):
            os.remove(text_output_fp)
        # Save the output image
        output_image.save(encrypt_output_image_fp)
    show_output()


def decrypt_event():
    """Function that does procedures for decryption

    Loads up the cover_image gotten from the user
    and calls the decrypt functions. If the text function detects text
    a text file with the decrypted message will be saved as a text file.
    Otherwise, the decrypted image will be saved.
    """
    # File path of cover image
    cover_image_fp = file_paths.get_cover_image_fp()
    text_output_fp = file_paths.get_decrypted_output_file_path(text=True)
    image_output_fp = file_paths.get_decrypted_output_file_path()
    # Open the cover image
    try:
        with Image.open(cover_image_fp) as cimg:
            cimg.load()
    except InvalidFileError:
        ui.notify("Cover image file can't be read!")
        return
    # Call the function to decrypt text from image
    decrypt_text, end_code_found = decrypt_text_from_image(cimg)
    # Save output as text file
    if end_code_found:
        # Remove output file if it exists
        if os.path.exists(image_output_fp):
            os.remove(image_output_fp)
        # Create new output file
        with open(text_output_fp, "w") as f:
            f.write(decrypt_text)
        cover_image_upload_text.reset()
    else:
        # Remove output file if it exists
        if os.path.exists(text_output_fp):
            os.remove(text_output_fp)
        # Call the function to decrypt an image from an image
        # Save output as an image
        decrypt_image_from_image(cimg).save(image_output_fp)
        cover_image_upload_image.reset()
    # Flush upload prompts
    secret_image_upload.reset()
    decrypt_image_upload.reset()
    show_output()


# GUI Contents

# Create Filepaths object to keep track of file paths
file_paths = Filepaths()
# Create TailwindStyling object for components styles
styles = TailwindStyling()

# Add static files folder
app.add_static_files("/static", "static")
# Add dark mode config
dark_mode = ui.dark_mode()

# Title of the project
with ui.header(elevated=False) as h:
    h.tailwind(styles.header_row)
    ui.label("In Plain Pixel").tailwind(styles.title_text)
    dark_mode_button = ui.checkbox("Dark Mode").bind_value_to(dark_mode, "value")
    dark_mode_button.tailwind(styles.dark_mode_switch)

# Prompt user to choose whether to encrypt or decrypt
with ui.row():
    ui.label("Select Encrpyt/Decrypt:").tailwind(styles.prompt_text_h)
    dropdown_encrypt_or_decrypt = ui.select(["Encrypt", "Decrypt"], value="Encrypt")

# Card with user input needed for encrypt with encrypt button
with ui.card().bind_visibility_from(
    dropdown_encrypt_or_decrypt, "value", value="Encrypt"
) as ed:
    ed.tailwind(styles.center_card)
    # Prompt the user to select the message type
    with ui.row():
        ui.label("Choose message type:").tailwind(styles.prompt_text_h)
        dropdown_text_or_image = ui.select(["Text", "Image"], value="Text")
    # User input needed if text message type is chosen
    with ui.column().bind_visibility_from(
        dropdown_text_or_image, "value", value="Text"
    ):
        # Prompt the user for the text they want to encrypt into cover image
        with ui.row():
            ui.label("Choose message source:").tailwind(styles.prompt_text_h)
            enter_text_or_upload = ui.select(
                ["Enter Text", "Read Text from File"], value="Enter Text"
            )
        with ui.column().bind_visibility_from(
            enter_text_or_upload, "value", value="Enter Text"
        ):
            with ui.row():
                with ui.column():
                    ui.label("Enter Text:").tailwind(styles.prompt_text_h)
                with ui.column():
                    text_entry = text_to_encrypt = ui.textarea(
                        label="Message", placeholder="Hello World"
                    )

        with ui.column().bind_visibility_from(
            enter_text_or_upload, "value", value="Read Text from File"
        ):
            with ui.row():
                with ui.column():
                    ui.label("Select Text File:").tailwind(styles.prompt_text_v)
                    text_upload = ui.upload(
                        auto_upload=True, on_upload=handle_text_file_upload, max_files=1
                    )
        # Prompt the user for the image they want to encrypt a message into
        with ui.row():
            with ui.column():
                ui.label("Enter Cover Image:").tailwind(styles.prompt_text_v)
                cover_image_upload_text = ui.upload(
                    auto_upload=True,
                    on_upload=lambda e: handle_image_upload(e, cover=True),
                    max_files=1,
                )
        with ui.row() as et:
            et.tailwind(styles.button_row)
            encrypt_text_button = ui.button(
                "Encrypt",
                on_click=lambda e: encrypt_event(
                    e,
                    dropdown_text_or_image.value,
                    enter_text_or_upload.value,
                    (
                        text_to_encrypt
                        if isinstance(text_to_encrypt, str)
                        else text_to_encrypt.value
                    ),
                ),
            )
            encrypt_text_button.tailwind(styles.button_center)
    # User input needed if image message type is chosen
    with ui.column().bind_visibility_from(
        dropdown_text_or_image, "value", value="Image"
    ):
        # Prompt the user for the image they want to encrypt into cover image
        with ui.row():
            with ui.column():
                ui.label("Enter Image to Encrypt:").tailwind(styles.prompt_text_v)
                secret_image_upload = ui.upload(
                    auto_upload=True,
                    on_upload=handle_image_upload,
                    max_files=1,
                )
        # Prompt the user for the image they want to encrypt a message into
        with ui.row():
            with ui.column():
                ui.label("Enter Cover Image:").tailwind(styles.prompt_text_v)
                cover_image_upload_image = ui.upload(
                    auto_upload=True,
                    on_upload=lambda e: handle_image_upload(e, cover=True),
                    max_files=1,
                )
        with ui.row() as ei:
            ei.tailwind(styles.button_row)
            encrypt_image_button = ui.button(
                "Encrypt",
                on_click=lambda e: encrypt_event(e, dropdown_text_or_image.value, None),
            )
            encrypt_image_button.tailwind(styles.button_center)

# Card with user input needed for decrypt with decrypt button
with ui.card().bind_visibility_from(
    dropdown_encrypt_or_decrypt, "value", value="Decrypt"
) as de:
    de.tailwind(styles.center_card)
    with ui.column():
        # Prompt the user for the image they want to decrypt
        with ui.row():
            with ui.column():
                ui.label("Enter Image to Decrypt:").tailwind(styles.prompt_text_v)
                decrypt_image_upload = ui.upload(
                    auto_upload=True,
                    on_upload=lambda e: handle_image_upload(e, cover=True),
                    max_files=1,
                )
        with ui.row() as di:
            di.tailwind(styles.button_row)
            decrypt_image_button = ui.button("Decrypt", on_click=decrypt_event)
            decrypt_image_button.tailwind(styles.button_center)

# Initialize and run the GUI
ui.run()

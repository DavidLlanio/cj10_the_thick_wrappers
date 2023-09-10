import io
from dataclasses import dataclass
import os
from os import path

from PIL import Image, UnidentifiedImageError
from nicegui import app, ui
from nicegui.events import UploadEventArguments, ClickEventArguments

from helper.constant import ResizeMode, FileType, Sizing, \
    UI_STRINGS, DESCRIPTION
from helper.decrypt import decrypt_image_from_image, decrypt_text_from_image
from helper.encrypt import encrypt_image_to_image, encrypt_text_to_image
from helper.utility import image_size_compare, image_resize, exif_embed_ipp

InvalidFileError = (OSError, UnidentifiedImageError)


@dataclass
class Filepath:
    file: str
    ext: str

    def get_file(self):
        return self.file + "." + self.ext

    def get_filepath(self):
        return path.join(".static", self.file)

    def get_filepath_full(self):
        return path.join(".static", f'{self.file}.{self.ext}')


def file_find(name: str) -> str:
    return path.join(".static", name)


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


def show_output(file_path, file_type):
    # If there is output use that as the content of the markdown
    match file_type:
        case file_type.IMAGE:
            if os.path.exists(file_path):
                with ui.dialog() as dialog, ui.card():
                    ui.label("Image Output").tailwind(styles.prompt_text_v)
                    ui.image(file_path)
                    with ui.row():
                        ui.button("Download", on_click=lambda: ui.download(file_path))
                        ui.button("Close", on_click=dialog.close)
                dialog.open()
        case file_type.TEXT:
            if os.path.exists(file_path):
                with open(file_path, "r") as o:
                    text = o.read()
                with ui.dialog() as dialog, ui.card():
                    ui.label("Text Output").tailwind(styles.prompt_text_v)
                    ui.markdown(f"{text}")
                    with ui.row():
                        ui.button("Close", on_click=dialog.close)
                dialog.open()


def handle_upload(file: UploadEventArguments, file_type: FileType, file_name: str):
    match file_type:
        case FileType.TEXT:
            """Read a text file selected as an encryption message"""
            # Try to parse file as text, aborting if this fails
            with file.content as f:
                _bytes = f.read()
            try:
                text = _bytes.decode("utf-8")
                # Write to storage file
                _path = Filepath(file_name, "txt")
                with open(_path.get_filepath_full(), "w") as f:
                    f.write(text)
                    ui.notify(f'{file.name} loaded')
            except UnicodeDecodeError:
                ui.notify("File could not be read correctly")
        case FileType.IMAGE:
            """Handle user image to encrypt.

            This function will take the image that was uploaded by the user
            and put it in the .static file folder of the repository as
            user_image.(file extension of original image)
            or
            cover_image.(file extension of original image)

            param img: object that has uploaded file
            """
            # Get the binary of the tempfile object
            content = file.content.read()
            _, extension = file.name.split(".")
            _path = Filepath(file_name, extension)
            try:
                with Image.open(io.BytesIO(content)) as image:
                    image.load()
                    exif = image.getexif()
                    image.save(fp=_path.get_filepath_full(), exif=exif)
                    ui.notify(f'{file.name} loaded')
            except UnidentifiedImageError:
                ui.notify("Could not load image!")


async def encrypt_event(e: ClickEventArguments, file_type: FileType, text_input: str | None = None):
    """Function that checks if conditions for encryption are met and calls encrypt fucntion

    This function will check whether text or image is being encrypted into the cover_image.
    If it is an image it will first check if the user_image is smaller or equal
    in size to cover_image. If user_image is too large it will resize it to be the same
    size as the cover_image. Then, the appropriate function will be called to encrypt
    either the text or image into the cover_image. The output image will be saved in .static
    folder as output_image.(cover image file extension)

    param e: GUI objects for click event.
    param value: String with type of message will be encrypted. Will be "Text" or "Image".
    param text_input: Message to be encrypted into image
    """
    try:
        cover = [file for file in os.listdir(".static") if "cover" in file][0]
        with Image.open(file_find(cover)) as cimg:
            cimg.load()
    except InvalidFileError:
        ui.notify("Cover image file cannot be read!")

    match file_type:
        case file_type.IMAGE:
            try:
                secret = [file for file in os.listdir(".static") if "secret" in file][0]
                with Image.open(file_find(secret)) as uimg:
                    uimg.load()
                    w_cimg, h_cimg = cimg.size
                    w_uimg, h_uimg = uimg.size
                    size_mode = image_size_compare(w_uimg, h_uimg, w_cimg, h_cimg)
                    if size_mode != Sizing.SMALLER:
                        with ui.dialog() as resize_dialog, ui.card():
                            ui.label("Secret image exceeds cover image ratio and will be cropped.\n"
                                     "Do you want to shrink the image to scale?")
                            with ui.row():
                                ui.button("Yes", on_click=lambda: resize_dialog.submit(ResizeMode.SHRINK_TO_SCALE))
                                ui.button("No", on_click=lambda: resize_dialog.submit(ResizeMode.DEFAULT))

                    resize_mode = await resize_dialog
                    if resize_mode is None:
                        resize_mode = ResizeMode.DEFAULT
                    resized_uimg = image_resize(uimg, cimg.size, resize_mode)
                    user_image_exif_data = resized_uimg.getexif()
                    new_exif_data = exif_embed_ipp(user_image_exif_data, resized_uimg.size)
                    output_image = encrypt_image_to_image(cimg, resized_uimg)
                    output = Filepath("output", cimg.format.lower())
                    output_image.save(output.get_filepath_full(), exif=new_exif_data)
                    ui.notify("Image encryption complete!")
                    show_output(output.get_filepath_full(), file_type.IMAGE)

            except InvalidFileError:
                ui.notify("Encryption image file cannot be read!")

        case file_type.TEXT:
            if text_input is None:
                _path = Filepath("message", "txt")
                try:
                    with open(_path.get_filepath_full()) as f:
                        text_input = f.read()
                except FileNotFoundError:
                    ui.notify("Text input file not found!")
                except OSError:
                    ui.notify("Error reading text input!")
            out_image = encrypt_text_to_image(text_input, cimg)
            if out_image is None:
                ui.notify("Text message is too long for image!")
            else:
                out = Filepath("output", cimg.format.lower())
                out_image.save(out.get_filepath_full())
                ui.notify("Text encryption complete!")
                show_output(out.get_filepath_full(), file_type.IMAGE)


def decrypt_event():
    """Function that does procedures for decryption

    Loads up the cover_image gotten from the user
    and calls the decrypt functions. If the text function detects text
    a text file with the decrypted message will be saved as a text file.
    Otherwise, the decrypted image will be saved.
    """
    try:
        cover = [file for file in os.listdir(".static") if "cover" in file][0]
        with Image.open(file_find(cover)) as cimg:
            cimg.load()
            decrypt_text, end_code_found = decrypt_text_from_image(cimg)
            # Save output as text file
            if end_code_found:
                secret_message = Filepath("secret_message", "txt")
                # Remove output file if it exists
                if os.path.exists(secret_message.get_filepath_full()):
                    os.remove(secret_message.get_filepath_full())
                # Create new output file
                with open(secret_message.get_filepath_full(), "w") as f:
                    f.write(decrypt_text)
                show_output(secret_message.get_filepath_full(), FileType.TEXT)
                ui.notify("Image decryption complete!")

            else:
                dec = Filepath("decrypted", cimg.format.lower())
                decrypt_image_from_image(cimg).save(dec.get_filepath_full())
                ui.notify("Image decryption complete!")
                show_output(dec.get_filepath_full(), FileType.IMAGE)
    except InvalidFileError:
        ui.notify("Cover image file can't be read!")


# GUI Contents

# Create TailwindStyling object for components styles
styles = TailwindStyling()

# Add .static files folder
app.add_static_files("/static", ".static")
# Add dark mode config
dark_mode = ui.dark_mode()


def switch_tab(msg: dict) -> None:
    _name = msg['args']
    tabs.props(f'model-value={_name}')
    panels.props(f'model-value={_name}')


with ui.header().classes('items-center', remove='q-pa-md gap-0') as header:
    with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
        with ui.row():
            with ui.button(icon='menu'):
                with ui.menu() as menu:
                    ui.menu_item('Menu item 1')
                    ui.separator()
                    ui.menu_item('Close', on_click=app.shutdown)
        for name in UI_STRINGS["crypt_type"]:
            ui.element('q-tab').props(f'name={name} label={name}')

with ui.footer(value=False) as footer:
    ui.label(DESCRIPTION)

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=lambda: footer.set_value(not footer.value)).props('fab icon=contact_support')

# the page content consists of multiple tab panels
with ui.element('q-tab-panels').props('model-value=Encrypt animated').classes('w-full') as panels:
    with ui.element('q-tab-panel').props(f'name=Encrypt'):
        with ui.tabs().classes('w-full') as enc_tabs:
            txt = ui.tab('Text', icon='text_fields')
            txt_file = ui.tab('Text File', icon='text_snippet')
            img = ui.tab('Image', icon="image")
        with ui.tab_panels(enc_tabs, value=txt).classes('w-full'):
            with ui.tab_panel(txt):
                with ui.row():
                    text_to_encrypt = ui.textarea(label="Message", placeholder="Enter secret message")
                    ui.upload(label="Attach image to encrypt", auto_upload=True,
                              on_upload=lambda e: handle_upload(e, FileType.IMAGE, "cover"),
                              max_files=1, on_rejected=ui.notify("Image file rejected")).props(
                        'accept="image/jpg, image/jpeg, image/png"')
                    encrypt_txt_to_image_button = ui.button("Encrypt",
                                                            on_click=lambda e: encrypt_event(e, FileType.TEXT,
                                                                                             text_to_encrypt.value))
            with ui.tab_panel(txt_file):
                with ui.row():
                    ui.upload(label="Attach text file", auto_upload=True,
                              on_upload=lambda e: handle_upload(e, FileType.TEXT, "message"),
                              max_files=1, on_rejected=ui.notify("Text file rejected")).props("accept=.txt")
                    ui.upload(label="Attach image to encrypt", auto_upload=True,
                              on_upload=lambda e: handle_upload(e, FileType.IMAGE, "cover"),
                              max_files=1, on_rejected=ui.notify("Image file rejected")).props(
                        'accept="image/jpg, image/jpeg, image/png"')
                    encrypt_txtfile_to_image_button = ui.button("Encrypt",
                                                                on_click=lambda e: encrypt_event(e, FileType.TEXT,
                                                                                                 None))
            with ui.tab_panel(img):
                with ui.row():
                    cover_enc_upload = ui.upload(label="Attach image to encrypt", auto_upload=True,
                                                 on_upload=lambda e: handle_upload(e, FileType.IMAGE, "secret"),
                                                 max_files=1, on_rejected=ui.notify("Image file rejected")).props(
                        'accept="image/jpg, image/jpeg, image/png"')
                    ui.upload(label="Attach image to encrypt", auto_upload=True,
                              on_upload=lambda e: handle_upload(e, FileType.IMAGE, "cover"),
                              max_files=1, on_rejected=ui.notify("Image file rejected")).props(
                        'accept="image/jpg, image/jpeg, image/png"')
                    encrypt_image_button = ui.button("Encrypt", on_click=lambda e: encrypt_event(e, FileType.IMAGE))

    with ui.element('q-tab-panel').props(f'name=Decrypt'):
        with ui.card().bind_visibility_from(f'model-value={name}', value="Decrypt").props(f'name={name}') as cover_dec:
            # Prompt the user for the image they want to decrypt
            with ui.column().classes("items-center"):
                ui.upload(label="Attach image to decrypt", auto_upload=True,
                          on_upload=lambda e: handle_upload(e, FileType.IMAGE, "cover"),
                          max_files=1, on_rejected=ui.notify("Image file rejected")).props(
                    'accept="image/jpg, image/jpeg, image/png"')
                decrypt_image_button = ui.button("Decrypt", on_click=decrypt_event)
ui.run()

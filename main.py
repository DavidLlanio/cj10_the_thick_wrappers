from nicegui import ui

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
                ui.upload(on_upload=lambda e: ui.notify(f"Uploaded {e.name}"))
        with ui.row():
            ui.button("Encrypt", on_click=lambda: ui.notify("Encrypted!"))
    # User input needed if image message type is chosen
    with ui.column().bind_visibility_from(dropdown_text_or_image, "value", value="Image"):
        # Prompt the user for the image they want to encrypt into cover image
        with ui.row():
            with ui.column():
                ui.label("Enter Image to Encrypt:")
            with ui.column():
                ui.upload(on_upload=lambda e: ui.notify(f"Uploaded {e.name}"))
        # Prompt the user for the image they want to encrypt a message into
        with ui.row():
            with ui.column():
                ui.label("Enter Cover Image:")
            with ui.column():
                ui.upload(on_upload=lambda e: ui.notify(f"Uploaded {e.name}"))
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
                ui.upload(on_upload=lambda e: ui.notify(f"Uploaded {e.name}"))
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

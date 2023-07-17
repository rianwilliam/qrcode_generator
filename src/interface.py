"""
A library used to create an interface for a flet.
Documentation available at: https://flet.dev/docs/
"""
import shutil
from src.window_conf import configure_window
from src.qr_generator import generate_qrcode, erase_qrcode, verify_folder, get_qrcode
from flet import (
    ElevatedButton,
    FilePicker,
    Container,
    TextField,
    alignment,
    Column,
    Image,
    Page,
    Row,
)

def main(page: Page) -> None:
    """
    This is where GUI elements are added to the app

    * Args:
        \t - page: An instance of the Page class from the Flet library
    """
    configure_window(page)
    verify_folder()
    erase_qrcode()


    def save_qrcode(e) -> None:
        """
        Using lib shutil we will copy the image that was saved
        in the assets folder to the directory that the user selected
        """
        img_path = get_qrcode()
        shutil.copy(img_path,directory_selector.result.path)

    def do_not_save_qrcode(e) -> None:
        """
        Runs when the user does not want to save the image,
        the created image is deleted and the element values are reset
        """
        erase_qrcode()
        img_collumn.controls.clear()
        content_field.disabled = False
        content_field.value = ""
        main_column.update()

    def verify_text_fied(e):
        """
        Checks if the content_field has information to be converted to qrcode,
        if it is blank the button to generate qrcode will be disabled
        """
        if not content_field.value or content_field.value[0] == " ":
            create_qr_btn.disabled = True
        else:
            create_qr_btn.disabled = False
        create_qr_btn.update()

    def add_qrcode(e) -> None:
        """
        Executes the create qr code function gets the image path
        and adds it in a column to be displayed to the user
        """
        generate_qrcode(content_field.value)
        img_path = get_qrcode()

        img_container = Container(
            content=Image(src=img_path,width=300,height=300),
            alignment=alignment.center
        )

        no_save_btn = ElevatedButton(text="Não salvar", on_click=do_not_save_qrcode)
        save_btn = ElevatedButton(
            text="Salvar QRCode",
            on_click=lambda _: directory_selector.save_file(file_name="QRcode.png",initial_directory=".")
        )


        img_collumn.controls.clear()
        img_collumn.controls = [
            img_container,
            Row(controls=[save_btn, no_save_btn],spacing=20,alignment="center")
        ]

        create_qr_btn.disabled = True
        content_field.disabled = True

        directory_selector.on_result = save_qrcode
        page.update()

    content_field = TextField(label="Insira o conteúdo",on_change=verify_text_fied)

    create_qr_btn = Container(
        content=ElevatedButton(text="Gerar QR Code",on_click=add_qrcode),
        alignment=alignment.center,
        disabled=True
    )

    img_collumn = Column(
        controls=[],
        horizontal_alignment="center"
    )

    directory_selector = FilePicker()

    main_column = Column(
        controls=[content_field,create_qr_btn,img_collumn, directory_selector],
        horizontal_alignment="center",
        width=(page.window_width/2),
        alignment="center",
        expand=True
    )

    main_container = Container(
        content=main_column,
        expand=True,
        alignment=alignment.center
    )

    page.overlay.append(directory_selector)
    page.add(main_container)
    page.update()

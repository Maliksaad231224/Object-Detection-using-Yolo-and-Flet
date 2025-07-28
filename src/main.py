import flet as ft
import shutil
import os

UPLOAD_DIR = "uploads"

yolo_ultralytics_models = [
    "YOLOv5n", "YOLOv5s", "YOLOv5m", "YOLOv5l", "YOLOv5x",
    "YOLOv8n", "YOLOv8s", "YOLOv8m", "YOLOv8l", "YOLOv8x"
]

dropdown = ft.Dropdown(
    label="Select YOLO Model",
    options=[ft.dropdown.Option(model) for model in yolo_ultralytics_models],
    width=500,
    bgcolor=ft.Colors.BLACK,
)

def main(page: ft.Page):
    page.bgcolor = "#1D2837"
    page.scroll = ft.ScrollMode.AUTO  # Enable scroll on page

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    def on_file_upload(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                filename = f.name
                dest_path = os.path.join(UPLOAD_DIR, filename)
                print('file uploaded', dest_path)
        else:
            print("no files uploaded")
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_upload)
    page.overlay.append(file_picker)

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.DEEP_PURPLE),
        leading_width=30,
        title=ft.Container(
            content=ft.Text('VisionTrainer', color=ft.Colors.WHITE),
            padding=ft.padding.only(left=10)
        ),
        toolbar_height=60,
        center_title=False,
        bgcolor="black"
    )

    # Upload button
    upload_button = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.UPLOAD_FILE, color=ft.Colors.BLUE, size=30),
                ft.Text("Upload Images", color=ft.Colors.WHITE, size=18)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
        ),
        height=400,
        alignment=ft.alignment.center,
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
        ink=False
    )

    # Shared padding for horizontal layout
    content_padding = ft.padding.symmetric(horizontal=100)

    # Final page content with scrollable Column
    page.add(
        ft.Container(
            padding=content_padding,
            content=ft.Column(
                [
                    # Description text
                    ft.Container(
                        content=ft.Text(
                            "Upload your images, annotate objects and train custom Computer vision models powered by YOLOv8!",
                            size=17,
                            color=ft.Colors.GREY_200,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.only(top=20, bottom=30),
                        alignment=ft.alignment.center,
                    ),

                    # Upload Container
                    ft.Container(
                        content=upload_button,
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREY_200),
                        height=400,
                        border_radius=15,
                        border=ft.border.all(2, ft.Colors.GREY_200),
                    ),

                    ft.Container(height=30),

                    # Two bottom containers
                    ft.Row(
    controls=[
        # Left container with icon, title, and dropdown
        ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(width=10),  # Small left spacing
                            ft.Icon(ft.Icons.MODEL_TRAINING_OUTLINED, color=ft.Colors.DEEP_PURPLE, size=30),
                            ft.Text(
                                "Model Configurations",
                                size=17,
                                color=ft.Colors.GREY_200,
                                text_align=ft.TextAlign.LEFT,
                                weight=ft.FontWeight.BOLD
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10
                    ),
                    ft.Container(height=20),  # Space between title and dropdown
                    ft.Container(
                        content=dropdown,
                        padding=ft.padding.only(left=20)
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREY_200),
            height=400,
            expand=True,
            border_radius=15,
            border=ft.border.all(2, ft.Colors.GREY_200),
            padding=20,
            alignment=ft.alignment.top_left
        ),

        # Right container (empty for now)
        ft.Container(
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREY_200),
            height=400,
            expand=True,
            border_radius=15,
            border=ft.border.all(2, ft.Colors.GREY_200),
        )
    ],
    spacing=20
)

                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO  # Make sure Column itself can scroll
            )
        )
    )

    page.update()

ft.app(main, assets_dir="assets", upload_dir="assets/uploads")
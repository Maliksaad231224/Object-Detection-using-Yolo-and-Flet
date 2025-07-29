import flet as ft
import shutil
import os
from backend import *

def main(page: ft.Page):
    page.bgcolor = "#11151A"
    page.theme = ft.Theme(font_family="Space Grotesk")
    page.theme.fonts = {
        "Space Grotesk": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap"
    }

    page.scroll = ft.ScrollMode.AUTO  # Enable scroll on page

    UPLOAD_DIR = "uploads"
    VAL_DIR = "validation"

    yolo_ultralytics_models = [
    "YOLOv5n", "YOLOv5s", "YOLOv5m", "YOLOv5l", "YOLOv5x",
    "YOLOv8n", "YOLOv8s", "YOLOv8m", "YOLOv8l", "YOLOv8x"
    ]

    model_dropdown = ft.Dropdown(
    label="Select YOLO Model",
    options=[ft.dropdown.Option(model) for model in yolo_ultralytics_models],
    width=570,
    bgcolor=ft.Colors.BLACK,                     # Background color
    color=ft.Colors.WHITE,                       # Text color
    border_color=ft.Colors.BLACK,     
    enable_filter=True, # Optional: white border
    label_style=ft.TextStyle(color=ft.Colors.WHITE),  # Label text color
)

    similarity = [0.5, 0.6, 0.7, 0.8, 0.9 ,1]
    similarity_threshold = ft.Dropdown(
    label="Similarity Threshold",
    options=[ft.dropdown.Option(model) for model in similarity],
    width=570,
    bgcolor=ft.Colors.BLACK,                     # Background color
    color=ft.Colors.WHITE,                       # Text color
    border_color=ft.Colors.BLACK,                # Optional: white border
    label_style=ft.TextStyle(color=ft.Colors.WHITE),  # Label text color
    )

    yolo_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    class_to_detect = ft.Dropdown(
    label="Select Class",
    options=[ft.dropdown.Option(model) for model in yolo_classes],
    width=570,
    bgcolor=ft.Colors.BLACK,                     # Background color
    color=ft.Colors.WHITE,                       # Text color
    border_color=ft.Colors.BLACK,     
    enable_filter=True, # Optional: white border
    label_style=ft.TextStyle(color=ft.Colors.WHITE),  # Label text color
    )

    resize_option = ft.Dropdown(
    label="Resize Value",
    options=[ft.dropdown.Option(model) for model in [244,640]],
    width=570,
    bgcolor=ft.Colors.BLACK,                     # Background color
    color=ft.Colors.WHITE,                       # Text color
    border_color=ft.Colors.BLACK,     
    enable_filter=True, # Optional: white border
    label_style=ft.TextStyle(color=ft.Colors.WHITE),  # Label text color
    )
    
    myimage = ft.Image(
		src=False,
		width=300,
		height=300,
		fit="cover"

		)
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    files_list = []
    def on_file_upload(e: ft.FilePickerResultEvent):
        
        if e.files:
            for f in e.files:
                filename = f.name
                dest_path = os.path.join(UPLOAD_DIR, filename)
                files_list.append(dest_path)
            print(files_list)
        else:
            print("no files uploaded")
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_upload)
    page.overlay.append(file_picker)
    
    
    def on_validation_file_upload(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                filename = f.name
                dest_path = os.path.join(VAL_DIR, filename)
                print("file uploaded", dest_path)
        else:
            print("no files uplaoded")
        page.update()
    
    valid_file_picker = ft.FilePicker(on_result = on_validation_file_upload)
    page.overlay.append(valid_file_picker)
    page.appbar = ft.AppBar(
    leading=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.DEEP_PURPLE),
    leading_width=30,
    title=ft.Container(
        content=ft.Text('VisionTrainer', color=ft.Colors.WHITE),
        padding=ft.padding.only(left=10)
    ),
    toolbar_height=60,
    center_title=False,
    bgcolor="#212121"
)

    # Upload button
    upload_button = ft.Container(
        content=ft.Row(
            [
                
                ft.Icon(ft.Icons.UPLOAD_FILE, color=ft.Colors.BLUE, size=30),
                ft.Text("Select Files", color=ft.Colors.WHITE, size=18)
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

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text("Upload Your Images", size=18, color=ft.Colors.WHITE),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(top=20)
                            ),
                            upload_button
                        ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0
                    ),
                bgcolor="#1A1A1A",
                height=400,
                border_radius=16,
                ),

                ft.Container(height=30),

                # Two bottom containers
                ft.ResponsiveRow(
                    controls=[
                        # Left container with icon, title, and dropdown
                        ft.Container(
                            bgcolor="#1A1A1A",
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Container(width=10),  # Small left spacing
                                            ft.Icon(ft.Icons.TUNE, color=ft.Colors.DEEP_PURPLE, size=30),
                                            ft.Text(
                                                "Model Configurations",
                                                size=17,
                                                color=ft.Colors.GREY_200,
                                                text_align=ft.TextAlign.LEFT,
                                                weight=ft.FontWeight.BOLD
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        spacing=10,
                                    ),
                                    ft.Container(height=20),  # Space between title and dropdown
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                model_dropdown, 
                                                        similarity_threshold,
                                                        class_to_detect,
                                                        resize_option,
                                                        ft.ElevatedButton(
                                                            "Upload Validation Set",
                                                            icon=ft.Icons.UPLOAD,
                                                            on_click=lambda _: valid_file_picker.pick_files(allow_multiple=True),
                                                            style=ft.ButtonStyle(
                                                                bgcolor=ft.Colors.BLUE,
                                                                    color=ft.Colors.WHITE,
                                                                    shape=ft.RoundedRectangleBorder(radius=10), 
                                                                ),
                                                            height=40,
                                                            width = 260,
                                                            expand=True
                                                        ),
                                                        ft.Container(height=20),
                                                        ft.ElevatedButton(
                                                            "Process Image",
                                                            icon=ft.Icons.TUNE,
                                                            style=ft.ButtonStyle(
                                                                bgcolor=ft.Colors.BLUE,
                                                                    color=ft.Colors.WHITE,
                                                                    shape=ft.RoundedRectangleBorder(radius=10), 
                                                                ),
                                                            height=40,
                                                            width = 560,
                                                            expand=True
                                                        ),
                                                        ft.ProgressBar(width=560, color=ft.Colors.AMBER, bgcolor="#eeeeee"),
                                            ],
                                            spacing=20,
                                            expand=True
                                        ),
                                        padding=ft.padding.only(left=20)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                                expand=True
                            ),
                            height=600,
                            col={"sm": 12, "md": 6},
                            border_radius=16,
                            padding=20,
                            alignment=ft.alignment.top_left
                        ),

                        # Right container (empty for now)
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.ElevatedButton(
                                        "Start WebCam",
                                        icon=ft.Icons.CAMERA_ALT,
                                        style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    height=50,
                                    width=560,
                                    expand=True
                                ),
                                ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    bgcolor="#1A1A1A",
                    height=600,
                    col={"sm": 12, "md": 6},
                    border_radius=16,
                    padding=20  
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
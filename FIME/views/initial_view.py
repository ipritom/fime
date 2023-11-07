import flet as ft
from fletSDP.views import FletView

import imageview


class InitialView(FletView):
    def __init__(self, page: ft.Page, updater) -> None:
        super().__init__(page, updater)
    
    def controls(self):
        self.image : imageview.ImageContext = None
        self.pick_files_dialog = ft.FilePicker()
        self.image_file_picker_btn =ft.ElevatedButton(
                                        "Open Image",
                                        icon=ft.icons.UPLOAD_FILE,
                                        )
        

    def layout(self):
        # self.page.clean()
        self.page.overlay.append(self.pick_files_dialog)
        self.page.add(
            ft.Row(
                [
                    ft.Container(
                        content=self.image_file_picker_btn,
                        alignment=ft.alignment.center, 
                        expand=True),
                    
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )
    
    
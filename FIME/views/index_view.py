from fletFlow import fletFlowView
import flet as ft
from utils import imageview


class IndexView(fletFlowView):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)

    def controls(self):
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_file_result)
        self.image_file_picker_btn =ft.ElevatedButton(
                                        "Open Image",
                                        icon=ft.icons.UPLOAD_FILE,
                                        on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=False)
                                        )
    
    def pick_file_result(self, e:ft.FilePickerResultEvent):
        path = e.files[0].path
        self.page.session.set("img_path", path)
        self.page.go("/edit")


    def layout(self):
        self.page.overlay.append(self.pick_files_dialog)
        lout = ft.Row(
                [
                    ft.Container(
                        content=self.image_file_picker_btn,
                        alignment=ft.alignment.center, 
                        expand=True),
                    
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        return lout
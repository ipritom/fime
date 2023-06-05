import flet as ft
from fletSDP.views import FletView

from dataclasses import dataclass

# from appbarview import AppBarView

@dataclass
class EditOption:
    BLUR = "Blur"
    FILTER = "Filter"
    CONTRAST = "Contrast"
    BW = "Black and White"

class EditView(FletView):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)

    
    def controls(self):
        self.save_btn = ft.IconButton(ft.icons.SAVE_ALT_OUTLINED)
        self.app_bar = ft.AppBar(
            title=ft.Text("Toolbar"),
            actions=[
                self.save_btn
            ]
            )
        self.flet_image: ft.Image = None
        self.image_container = ft.Container()
        self.edit_option = ft.Dropdown(label="Edit Option",
                                  text_size=18,
                                  options=[
                                       ft.dropdown.Option(EditOption.BLUR), 
                                       ft.dropdown.Option(EditOption.FILTER), 
                                       ft.dropdown.Option(EditOption.CONTRAST),
                                       ft.dropdown.Option(EditOption.BW)],
                                      )
        self.reset_button = ft.IconButton(icon=ft.icons.REFRESH_OUTLINED, tooltip="Reload Image")
        self.edit_panel = ft.Column([ft.Row([self.edit_option, self.reset_button])])
        

        self.image_container =ft.Container(self.image_container, 
                                      padding=10, 
                                      expand=True,
                                      bgcolor=ft.colors.GREY_300, 
                                      image_fit=ft.ImageFit.FILL)
        

    def layout(self):
        self.page.appbar = self.app_bar
        self.image_container.content = self.flet_image
        
        self.page.add(
            ft.Row([self.image_container, 
                    ft.Container(self.edit_panel, 
                                padding=10,
                                expand=True,
                                #alignment= ft.alignment.top_right
                     )],
                          expand=True)
        )

       

        
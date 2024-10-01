from dataclasses import dataclass

from fletFlow import fletFlowView
import flet as ft
from utils import imageview



@dataclass
class EditOption:
    MBLUR = "Median Blur"
    GBLUR = "Gaussian Blur"
    FILTER = "Filter"
    CONTRAST = "Contrast"
    BW = "Black and White"


class EditView(fletFlowView):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)
    
    def controls(self):
        
        path = self.page.session.get("img_path")
        # print(path)
        # path = r"C:\Users\Pritom\Desktop\Bard_Generated_Image.jpg"
        # path = r"D:\Experiments\git_projects\fime\FIME\sunflower.jpg"
        self.image : imageview.ImageContext = imageview.ImageContext(path=path, preload=True)
        # self.initial_view.image = imageview.ImageContext(path=path, preload=True,height=500, width=450)
        self.flet_image = ft.Image(
            src_base64=self.image.get_base64()
        )
        self.image_container = ft.Container()
        self.edit_option = ft.Dropdown(label="Edit Option",
                                  text_size=18,
                                  options=[
                                       ft.dropdown.Option(EditOption.MBLUR), 
                                       ft.dropdown.Option(EditOption.GBLUR), 
                                       ft.dropdown.Option(EditOption.FILTER), 
                                       ft.dropdown.Option(EditOption.CONTRAST),
                                       ft.dropdown.Option(EditOption.BW)],
                                    on_change=self.on_select_edit_option,
                                      )
        self.reset_button = ft.IconButton(icon=ft.icons.REFRESH_OUTLINED, tooltip="Reload Image", on_click=self._reload_image)
        self.undo_button  = ft.IconButton(icon=ft.icons.UNDO_OUTLINED, tooltip="Undo")
        self.redo_button  = ft.IconButton(icon=ft.icons.REDO_OUTLINED, tooltip="Redo")
        self.edit_panel = ft.Column([ft.Row([self.edit_option, self.reset_button, self.undo_button, self.redo_button])])

    def on_select_edit_option(self, e:ft.ControlEvent):
        selected = e.control.value
        print("history length", self.image.history_length)
        print(len(self.edit_panel.controls))

        # discarding previous edit tool
        if len(self.edit_panel.controls)>1:
            self.edit_panel.controls.pop()


        if selected == EditOption.MBLUR:
            self.blur_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}", on_change=self._median_blur_slider_change)
            self.edit_panel.controls.append(self.blur_slider)
        
        elif selected == EditOption.GBLUR:
            self.gblur_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}", on_change=self._gaussian_blur_slider_change)
            self.edit_panel.controls.append(self.gblur_slider)
        elif selected == EditOption.CONTRAST:
            self.alpha_slider = ft.Slider(min=0, max=5, divisions=5, label="alpha {value}")
            self.beta_slider = ft.Slider(min=0, max=5, divisions=5, label="beta {value}")
            self.btn_contrast_apply = ft.ElevatedButton(text="Apply", on_click=self._on_contrast_apply)
            
            self.edit_panel.controls.append(
                ft.Column([
                self.alpha_slider,
                self.beta_slider,
                self.btn_contrast_apply
            ])
            )

        elif selected == EditOption.BW:
            self.btn_bw = ft.TextButton("Black & White", on_click=self._on_btn_bw_click)
            self.edit_panel.controls.append(self.btn_bw)


        self.page.update()

    def _on_btn_bw_click(self, e):
        self.image = imageview.image_gray(self.image)
        self.flet_image.src_base64 = self.image.get_base64()
        self.page.update()

    def _on_contrast_apply(self, e):
        alpha = self.alpha_slider.value
        beta = self.beta_slider.value
        self.image = imageview.image_conrast(self.image, alpha=alpha, beta=beta)
        self.flet_image.src_base64 = self.image.get_base64()
        self.page.update()

    def _reload_image(self, e):
        self.image.reload()
        self.flet_image.src_base64 = self.image.get_base64()
        self.page.update()

    def _median_blur_slider_change(self, e):
        k = int(2*(e.control.value)+1)
        print("k =",k)
        self.image = imageview.image_median_blur(self.image, kernal_size=k)
        self.flet_image.src_base64 = self.image.get_base64()
        self.page.update()
    
    def _gaussian_blur_slider_change(self, e):
        k = int(2*(e.control.value)+1)
        print("k =",k)
        self.image = imageview.image_gaussian_blur(self.image, kernal_size=k)
        self.flet_image.src_base64 = self.image.get_base64()
        self.page.update()

    def layout(self):
        self.image_container.content = self.flet_image
        # self.flet_image.src_base64 = self.init
        lout = ft.Row([
            self.image_container,
            ft.Container(
                self.edit_panel,
                padding=10,
                expand=True
            )
        ], expand=True)
        return lout
from fletSDP.app import FletSDPApp
import flet as ft

from views.initial_view import InitialView
from views.edit_view import EditView, EditOption

import imageview

class App(FletSDPApp):
    def __init__(self, title=None) -> None:
        super().__init__(title)
    
    def views(self, page:ft.Page):
        self.initial_view = InitialView(self.page, updater=self.initial_view_updater)
        self.edit_view = EditView(self.page, updater=self.edit_view_updater)

    def initial_view_updater(self):
        pick_files_dialog = self.initial_view.pick_files_dialog
        self.initial_view.image_file_picker_btn.on_click = lambda _: pick_files_dialog.pick_files(allow_multiple=False)
        pick_files_dialog.on_result = self._pick_files_result

    def edit_view_updater(self):
        save_files_dialog = self.edit_view.save_files_dialog
        self.edit_view.edit_option.on_change = self._on_select_edit_option
        self.edit_view.save_btn.on_click = lambda _: save_files_dialog.get_directory_path(dialog_title="Save Location")
        self.edit_view.reset_button.on_click = self._image_reload
        self.edit_view.undo_button.on_click = self._image_undo
        self.edit_view.redo_button.on_click = self._image_redo
        self.edit_view.image_container.on_hover = self._on_hover_image_container
         # add interaction logic function for edit page
        save_files_dialog.on_result = self._save_image

    def app_presentaion(self):
        self.initial_view.render()
       

    def _on_hover_image_container(self, e):
        print(e.data)
        # print(e.local_x, e.local_y)

    def _image_redo(self, e):
        self.initial_view.image.redo()
        self.edit_view.flet_image.src_base64 = self.initial_view.image.get_base64()
        self.edit_view.flet_image.update()
        self.page.update()

    def _image_undo(self, e):
        self.initial_view.image.undo()
        self.edit_view.flet_image.src_base64 = self.initial_view.image.get_base64()
        self.edit_view.flet_image.update()
        self.page.update()
        
    def _image_reload(self, e):
        self.initial_view.image.reload()
        self.edit_view.flet_image.src_base64 = self.initial_view.image.get_base64()
        self.edit_view.flet_image.update()
        self.page.update()
        # self.initial_view.image.save_state() # this causes memory leak

    def _on_select_edit_option(self, e):
        selected = e.control.value
        # saving the initial image state on which edit will be applied
        self.initial_view.image.save_state()

        # discarding previous edit tool
        if len(self.edit_view.edit_panel.controls)>1:
            self.edit_view.edit_panel.controls.pop()

        # adding selected edit tool
        if selected == EditOption.BLUR:
            self.blur_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}", on_change=self._blur_slider_change)
            self.edit_view.edit_panel.controls.append(self.blur_slider)
    
        elif selected == EditOption.BW:
            self.bw_btn = ft.ElevatedButton("Black & White", data=True, on_click=self._apply_black_and_white)
            self.edit_view.edit_panel.controls.append(self.bw_btn)

        elif selected == EditOption.FILTER:
            self.filter_options = ft.RadioGroup(content=ft.Column([
                                ft.Radio(value="v", label="Verticle Mask"),
                                ft.Radio(value="h", label="Horizontal Mask"),
                                ft.Radio(value="s", label="Sobel Mask")
                                ]), on_change=self._apply_filter)
            self.edit_view.edit_panel.controls.append(self.filter_options)

        elif selected == EditOption.CONTRAST:
            self.contast_alpha = ft.Slider(min=0,max=10.0, value=1, data="alpha", divisions=20, label="{value}", on_change=self._contrast_change)
            self.contast_beta = ft.Slider(min=0,max=20, value = 1, data="beta", divisions=20, label="{value}", on_change=self._contrast_change)
            
            self.edit_view.edit_panel.controls.append(ft.Column([ft.Text("alpha"),
                                                                 self.contast_alpha, 
                                                                 ft.Text("beta"),
                                                                 self.contast_beta]))
        self.page.update()

    def _contrast_change(self, e):
        alpha = self.contast_alpha.value
        beta = self.contast_beta.value
        self.initial_view.image.discard()

        self.initial_view.image = imageview.image_conrast(self.initial_view.image, alpha, beta)

        self.edit_view.flet_image.src_base64 = self.initial_view.image.get_base64()
        self.edit_view.flet_image.update()
        self.page.update()

    def _apply_filter(self, e):
        filter_type = e.control.value
        self.initial_view.image.discard()
    
        if filter_type=="v":
            self.initial_view.image = imageview.image_filter(self.initial_view.image, imageview.VERTICAL_KERNAL)
        elif filter_type=="h":
            self.initial_view.image = imageview.image_filter(self.initial_view.image, imageview.HORIZONTAL_KERNAL)
        elif filter_type=="s":
            self.initial_view.image = imageview.image_filter(self.initial_view.image, imageview.SOBEL_KERNAL)

        self.edit_view.flet_image.src_base64 = self.initial_view.image.get_base64()
        self.edit_view.flet_image.update()
        self.page.update()

    def _apply_black_and_white(self, e):
        # self.initial_view.image.discard()
        # taking button data state to toggle
        bw_or_not = e.control.data
        # applying changes
        if bw_or_not:
            self.initial_view.image = imageview.image_gray(self.initial_view.image)
            self.bw_btn.text = "Discard"
            self.bw_btn.data = False
        else:
            self.bw_btn.text = "Black & White"
            self.initial_view.image.discard()
            self.bw_btn.data = True
            
        self.edit_view.flet_image.src_base64 = self.initial_view.image.get_base64()
        self.edit_view.flet_image.update()
        self.page.update()

    def _blur_slider_change(self,e):
        kernal_size = 2*int(e.control.value) + 1
        self.initial_view.image.discard()
        self.initial_view.image = imageview.image_median_blur(self.initial_view.image, kernal_size=kernal_size)

        self.edit_view.flet_image.src_base64 = self.initial_view.image.get_base64()
        self.edit_view.flet_image.update()
        self.page.update()

    def _pick_files_result(self, e):
        self.initial_view.image = imageview.ImageContext(e.files[0].path, preload=True,height=500, width=450)
        self.edit_view.flet_image = ft.Image(src_base64=self.initial_view.image.get_base64())
        self.edit_view.render(clean_controls=False)

    def _save_image(self, e:ft.FilePickerResultEvent):
        imageview.image_save(self.initial_view.image,
                             name = self.edit_view.image_name_textbox.value,
                             path=e.path)

    # run() method can be overloaded
    # def run(self):
    #     ft.app(target=self.main,view=ft.WEB_BROWSER)

        

app = App(title="FIME")
app.run()
        
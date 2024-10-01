from fletFlow import fletFlowApp
from fletFlow.views import fletFlowView

from views.index_view import IndexView
from views.edit_view import EditView


class App(fletFlowApp):
    def __init__(self, title=None, debug=False) -> None:
        super().__init__(title, debug)

    def views(self, route: str = None, view_class: fletFlowView = None):
        self.register_view("/", IndexView)
        self.register_view("/edit", EditView)
    
    def app_presentaion(self):
        # self.page.go("/")
        self.page.go("/edit")


app = App(title="EDIMAGE")
app.run()
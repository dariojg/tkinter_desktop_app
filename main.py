import os

from tkinter import Tk, PhotoImage

from views.v_categoria import CategoriaView
from views.v_gasto import GastoView
from controllers.c_categoria import CategoriaController
from controllers.c_gasto import GastoController

path_icon = os.path.realpath(os.path.join(os.path.dirname(__file__), 'img',  'icon.png'))

app = Tk()
app.title("Expense manager")
app.minsize(600, 400)
image_icon = PhotoImage(file=path_icon)
app.iconphoto(True, image_icon)

contr_categoria = CategoriaController(app)
view_categoria = CategoriaView(app, contr_categoria)

contr_gasto = GastoController(app, view_categoria.view())
view_gasto = GastoView(app, contr_gasto)
tree_gasto = view_gasto.view()

view_categoria.update_treeview()
view_gasto.update_treeview()

contr_categoria.set_tree_gastos(view_gasto.get_tree())
app.mainloop()

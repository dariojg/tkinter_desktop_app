from tkinter import ttk, Button, StringVar, Label, Entry
from models import Categoria
#############################
# #    View Categorías    # #
#############################

PAD_X = 10
PAD_Y = 5


def categoria_view(app, c_categoria):
    var_categoria = StringVar()

    tree_categorias = ttk.Treeview(app)
    tree_categorias["columns"] = ("col1",)
    tree_categorias.column("#0", width=35, anchor='w')
    tree_categorias.column("col1", width=150, minwidth=80)
    tree_categorias.heading("#0", text="Id")
    tree_categorias.heading("col1", text="Categorías")
    tree_categorias.grid(row=1, column=0, padx=10)

    # botones_categoria(var_categoria)
    b_guardar = Button(text="+", command=c_categoria.controller_crear_categoria)
    b_guardar.grid(row=2, column=0, sticky="nw", padx=PAD_X, pady=PAD_Y)
    b_eliminar = Button(text="+/-", command=c_categoria.controller_editar_categoria)
    b_eliminar.grid(row=2, column=0, sticky="n", pady=PAD_Y)
    b_eliminar = Button(text="-", command=c_categoria.controller_eliminar_categoria, padx=PAD_X, pady=PAD_Y)
    b_eliminar.grid(row=2, column=0, sticky="ne", padx=PAD_X, pady=PAD_Y)

    l_categoria = Label(app, text="categoría")
    l_categoria.grid(row=3, column=0, sticky="nw")
    e_categoria = Entry(app, textvariable=var_categoria, width=15)
    e_categoria.grid(row=3, column=0, sticky="ne")

    return (tree_categorias, var_categoria)


class CategoriaView():

    def __init__(self, app, cat_controller):
        self.app = app
        self.var_categoria = StringVar()
        self.tree_categorias = ttk.Treeview(self.app)
        self.categoria = cat_controller

    def view(self):
        self.tree_categorias["columns"] = ("col1",)
        self.tree_categorias.column("#0", width=35, anchor='w')
        self.tree_categorias.column("col1", width=150, minwidth=80)
        self.tree_categorias.heading("#0", text="Id")
        self.tree_categorias.heading("col1", text="Categorías")
        self.tree_categorias.grid(row=1, column=0, padx=10)

        # botones_categoria(var_categoria)
        b_guardar = Button(text="+", command=self.controller_crear_categoria)
        b_guardar.grid(row=2, column=0, sticky="nw", padx=PAD_X, pady=PAD_Y)
        b_eliminar = Button(text="+/-", command=self.controller_editar_categoria)
        b_eliminar.grid(row=2, column=0, sticky="n", pady=PAD_Y)
        b_eliminar = Button(text="-", command=self.controller_eliminar_categoria, padx=PAD_X, pady=PAD_Y)
        b_eliminar.grid(row=2, column=0, sticky="ne", padx=PAD_X, pady=PAD_Y)

        l_categoria = Label(self.app, text="categoría")
        l_categoria.grid(row=3, column=0, sticky="nw")
        e_categoria = Entry(self.app, textvariable=self.var_categoria, width=15)
        e_categoria.grid(row=3, column=0, sticky="ne")

        return self.tree_categorias

    def controller_crear_categoria(self):
        self.categoria.crear(self.var_categoria, self.tree_categorias)

    def controller_editar_categoria(self):
        self.categoria.editar(self.var_categoria, self.tree_categorias)

    def controller_eliminar_categoria(self):
        self.categoria.eliminar(self.tree_categorias)

    def update_treeview(self):
        categorias = Categoria().select()

        for row in categorias:
            self.tree_categorias.insert("", "end", text=(row.id), values=(row.name))

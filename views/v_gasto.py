from tkinter import ttk, Button, StringVar, DoubleVar, Label, Entry
from models import Gasto

#############################
# #     View Gastos       # #
#############################

PAD_X = 10
PAD_Y = 5


class GastoView():

    def __init__(self, app, contr_gasto):
        self.app = app
        self.var_gasto = StringVar()
        self.var_monto = DoubleVar()
        self.var_filtro = StringVar()
        self.var_filtro_cat = StringVar()
        self.c_gasto = contr_gasto

    def view(self):
        app = self.app
        self.tree_gastos = ttk.Treeview(app)
        self.tree_gastos["columns"] = ("col1", "col2", "col3")
        self.tree_gastos.heading("#0", text="Id")
        self.tree_gastos.column("#0", width=40)
        self.tree_gastos.heading("col1", text="Gastos")
        self.tree_gastos.column("col1", width=100, minwidth=80)
        self.tree_gastos.heading("col2", text="Monto")
        self.tree_gastos.column("col2", width=35, minwidth=80)
        self.tree_gastos.heading("col3", text="Fecha")
        self.tree_gastos.column("col3", width=200, minwidth=80)
        self.tree_gastos.grid(row=1, column=2, padx=PAD_X)

        b_guardar = Button(text="+", command=self.controller_crear_gasto)
        b_guardar.grid(row=2, column=2, sticky="nw", padx=PAD_X, pady=PAD_Y)
        b_eliminar = Button(text="+/-", command=self.controller_editar_gasto)
        b_eliminar.grid(row=2, column=2, sticky="n", pady=PAD_Y)
        b_eliminar = Button(text="-", command=self.controller_eliminar_gasto)
        b_eliminar.grid(row=2, column=2, sticky="ne", padx=PAD_X, pady=PAD_Y)

        l_gasto = Label(app, text="gasto")
        l_gasto.grid(row=3, column=2,  sticky="w", padx=PAD_X)
        e_gasto = Entry(app, textvariable=self.var_gasto, width=15)
        e_gasto.grid(row=3, column=2,  sticky="n", padx=PAD_X)

        l_monto = Label(app, text="monto")
        l_monto.grid(row=4, column=2, sticky="w", padx=PAD_X)
        l_monto = Entry(app, textvariable=self.var_monto, width=15)
        l_monto.grid(row=4, column=2, sticky="n", padx=PAD_X)

        l_buscar = Label(app, text="Buscar gastos")
        l_buscar.grid(row=5, column=2, sticky="w", padx=PAD_X)
        e_filtro = Entry(app, textvariable=self.var_filtro, width=15)
        e_filtro.grid(row=5, column=2, sticky="n", padx=PAD_X, pady=10)
        b_buscar = Button(text="Buscar", command=self.controller_buscar_gastos)
        b_buscar.grid(row=5, column=2, sticky="e",  padx=PAD_X)

        l_fcat = Label(app, text="Filtrar categoría")
        l_fcat.grid(row=6, column=2, sticky="w", padx=PAD_X)
        e_fcat = Entry(app, textvariable=self.var_filtro_cat, width=15)
        e_fcat.grid(row=6, column=2, sticky="n", padx=PAD_X, pady=10)
        b_fcat = Button(text="Buscar", command=self.controller_buscar_gastos_por_cat)
        b_fcat.grid(row=6, column=2, sticky="e",  padx=PAD_X)

        return self.tree_gastos

    def controller_crear_gasto(self):
        self.c_gasto.crear(self.var_gasto, self.var_monto, self.tree_gastos)

    def controller_editar_gasto(self):
        self.c_gasto.editar(self.var_gasto, self.var_monto, self.tree_gastos)

    def controller_eliminar_gasto(self):
        self.c_gasto.eliminar(self.tree_gastos)

    def controller_buscar_gastos(self):
        self.c_gasto.buscar_gastos(self.var_filtro, self.tree_gastos)

    def controller_buscar_gastos_por_cat(self):
        self.c_gasto.buscar_gastos_por_cat(self.var_filtro_cat, self.tree_gastos)

    def get_tree(self):
        return self.tree_gastos

    def update_treeview(self):
        gastos = Gasto().select()

        for row in gastos:
            self.tree_gastos.insert("", "end", text=str(row.id), values=(row.name, row.amount, row.get_formated_date()))

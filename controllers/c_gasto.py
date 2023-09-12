import datetime

from tkinter.messagebox import showerror, showinfo, askyesno
from models import Gasto, Categoria
from peewee import DoesNotExist
"""
    Controlador de la vista gastos
"""


class GastoController():
    """Controlador para gestionar gastos de la aplicación.

    Este controlador proporciona métodos para crear, eliminar, editar y buscar gastos, así como para vincularlos a categorías.

    Args:
        app (Tk): La instancia de la aplicación tkinter a la que está asociado el controlador.
        view_categoria (TreeView): El widget Treeview utilizado para mostrar las categorías.

    Attributes:
        app (Tk): La instancia de la aplicación tkinter.
        view_cat (TreeView): El widget Treeview que muestra las categorías.

    Methods:
        inputs_gasto_is_ok(var_gasto, var_monto): Verifica si los valores de entrada para gasto y monto son válidos.
        crear(var_gasto, var_monto, tree_gastos): Crea un nuevo gasto y lo agrega a la lista de gastos en la interfaz.
        eliminar(tree_gastos): Elimina un gasto seleccionado.
        editar(var_gasto, var_monto, tree_gastos): Edita un gasto seleccionado.
        buscar_gastos(var_filtro, tree_gastos): Busca gastos por nombre.
        buscar_gastos_por_cat(var_filtro_cat, tree_gastos): Busca gastos por categoría.
    """

    def __init__(self, app, view_categoria):
        self.app = app
        self.view_cat = view_categoria

    def inputs_gasto_is_ok(self, var_gasto, var_monto):
        gasto = var_gasto.get()
        monto = var_monto.get()
        return gasto != "" and gasto is not None and monto != "" and monto != 0

    def crear(self, var_gasto, var_monto, tree_gastos):
        """Crea un nuevo gasto y lo agrega a la lista de gastos en la interfaz.

        Args:
            var_gasto (StringVar): Variable de control para el campo de entrada de gasto.
            var_monto (StringVar): Variable de control para el campo de entrada de monto.
            tree_gastos (Treeview): Widget Treeview que muestra la lista de gastos.
        """
        tree_categorias = self.view_cat
        try:
            gasto = var_gasto.get()
            monto = var_monto.get()
        except Exception as ex:
            showerror("Error", "Hubo un problema con el monto o el nombre, verifica que los datos son correctos")
            raise ex

        item_categoria_focus = tree_categorias.focus()
        if item_categoria_focus == "" or item_categoria_focus is None:
            showerror("Error", "El gasto debe pertenecer a una categoría, selecciona una categoría")
            return

        item_categoria_id = tree_categorias.item(item_categoria_focus)["text"]
        selected_categoria = Categoria().get(Categoria.id==item_categoria_id)
        if not self.inputs_gasto_is_ok(var_gasto, var_monto):
            showerror("Error", "Debes ingresar el gasto y el monto para crear")
            return

        if askyesno("Guardar", f"Vas a crear un gasto {gasto[0]}, monto {monto}"):
            m_gasto = Gasto(name=gasto, amount=monto, categoria=selected_categoria)
            m_gasto.save()  # self.m_gasto.model_insert_gasto(gasto, monto, date, item_categoria_id)
            tree_gastos.insert("", "end", text=str(m_gasto.id), values=(gasto, monto, m_gasto.get_formated_date()))
            showinfo("Guardado", f"Gasto \"{gasto}\" creado exitosamente")

    def eliminar(self, tree_gastos):
        """Elimina un gasto seleccionado.

        Args:
            tree_gastos (Treeview): Widget Treeview que muestra la lista de gastos.
        """
        item_focus = tree_gastos.focus()
        gasto_id = tree_gastos.item(item_focus)['text']
        tree_gastos.delete(item_focus)
        m_gasto = Gasto().get(Gasto.id==gasto_id)
        m_gasto.delete_instance()
        print(f"ELIMINASTE GASTO id {gasto_id}")

    def editar(self, var_gasto, var_monto, tree_gastos):
        """Edita un gasto seleccionado.

        Args:
            var_gasto (StringVar): Variable de control para el campo de entrada de gasto.
            var_monto (StringVar): Variable de control para el campo de entrada de monto.
            tree_gastos (Treeview): Widget Treeview que muestra la lista de gastos.
        """
        item_gastos_focus = tree_gastos.focus()
        if item_gastos_focus == "" or item_gastos_focus is None:
            return

        gasto = var_gasto.get()
        monto = var_monto.get()
        date = datetime.datetime.now()
        date_str = date.strftime("%d-%m-%Y")

        gasto_id = tree_gastos.item(item_gastos_focus)["text"]
        if not self.inputs_gasto_is_ok(var_gasto, var_monto):
            showerror("Error", "Debes ingresar el gasto y el monto para editarlo")
            return

        if askyesno("Editar", f"Vas a editar gasto {gasto}, monto {monto}"):
            m_gasto = Gasto().update(name=gasto, amount=monto, date=date).where(Gasto.id==gasto_id)
            m_gasto.execute()
            tree_gastos.insert("", "end", text=str(gasto_id), values=(gasto, monto, date_str))
            print(f"CREASTE GASTO {gasto}")

        item_focus = tree_gastos.focus()
        gasto_id = tree_gastos.item(item_focus)['text']

        tree_gastos.delete(item_focus)
        print(f"EDITASTE GASTO {gasto_id}")

    def buscar_gastos(self, var_filtro, tree_gastos):
        """Busca gastos por nombre.

        Args:
            var_filtro (StringVar): Variable de control para el campo de búsqueda.
            tree_gastos (Treeview): Widget Treeview que muestra la lista de gastos.
        """
        try:
            name_cat = var_filtro.get()
            gastos_result = Gasto.select().where(Gasto.name.startswith(name_cat))

            for item in tree_gastos.get_children():
                tree_gastos.delete(item)
                
            if len(gastos_result) > 0:
                for gasto in gastos_result:
                    print(f"*********** {gasto}")
                    tree_gastos.insert("", "end", text=str(gasto.id), values=(gasto.name, gasto.amount, gasto.get_formated_date()))
        except DoesNotExist as ex:
            print(f"Gastos Does not exist {ex.message}")
            # raise ex(f"No se encontraron Gastos para la categoría  con nombre {var_filtro.get()}")

    def buscar_gastos_por_cat(self, var_filtro_cat, tree_gastos):
        """Busca gastos por categoría.

        Args:
            var_filtro_cat (StringVar): Variable de control para el campo de búsqueda por categoría.
            tree_gastos (Treeview): Widget Treeview que muestra la lista de gastos.
        """
        try:
            r_categoria = Categoria.get(Categoria.name.startswith(var_filtro_cat.get()))
            print(f"Nombre de categoría: {r_categoria.name}")
            results_gastos = Gasto.select().where(Gasto.categoria==r_categoria.id)
            print(results_gastos)

            if len(results_gastos) > 0:
                for item in tree_gastos.get_children():
                    tree_gastos.delete(item)

                for item in results_gastos:
                    print(item)
                    tree_gastos.insert("", "end", text=str(item.id), values=(item.name, item.amount, item.get_formated_date()))
                    # tree_gastos.insert("", "end", text=str(gasto_id), values=(gasto, monto, date, item_categoria_id))
        except DoesNotExist as ex:
            print(f"Gastos Does not exist: {ex}")
            raise ex

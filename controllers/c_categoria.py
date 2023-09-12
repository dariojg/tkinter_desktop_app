from utils import es_palabra
# from models import queries
from models import Categoria, Gasto
from tkinter.messagebox import showerror, showinfo, askyesno

#############################
# # Controller Categorías # #
#############################


class CategoriaController():
    """Controlador para gestionar categorías en una aplicación.

    Este controlador proporciona métodos para crear, eliminar y editar categorías, así como para gestionar
    los gastos asociados a ellas.

    Args:
        app (Tk): La instancia de la aplicación tkinter a la que está asociado el controlador.

    Attributes:
        app (Tk): La instancia de la aplicación tkinter.
        tree_gastos (Treeview): El widget Treeview utilizado para mostrar la lista de gastos asociados a las categorías.

    Methods:
        crear(var_categoria, t_categoria): Crea una nueva categoría y la agrega a la lista de categorías en la interfaz.
        eliminar(item_focus, t_categoria): Elimina una categoría seleccionada y todos los gastos asociados a ella.
        editar(var_categoria, t_categoria): Edita el nombre de una categoría seleccionada.
        set_tree_gastos(t_gastos): Establece el widget Treeview utilizado para mostrar los gastos asociados a las categorías.
    """
    def __init__(self, app):
        self.app = app
        self.tree_gastos = None

    def crear(self, var_categoria, t_categoria):
        """Crea una nueva categoría y la agrega a la lista de categorías en la interfaz.

        Args:
            var_categoria (StringVar): Variable de control para el campo de entrada de categoría.
            t_categoria (Treeview): Widget Treeview que muestra la lista de categorías.
        """
        categoria = var_categoria.get()

        if not es_palabra(categoria):
            showerror("Error", "El valor ingresado no es válido, solo se permiten letras")
            return

        if categoria == "" or categoria is None:
            showerror("Error", "Debes ingresar una categoria para crear")
            return

        if askyesno("Guardar", f"Vas a crear la categoría {categoria}"):
            m_cat = Categoria()
            m_cat.name = categoria
            m_cat.save()
            print(f"**** {categoria}")
            t_categoria.insert("", "end", text=str(m_cat.id), values=(categoria,))
            showinfo("Guardado", f"Categoría \"{categoria}\" cr=eada exitosamente")

    def eliminar_categoria_gastos_asociados(self, gastos):
        for gasto in gastos:
            gasto.delete_instance()
     
        self.tree_gastos.delete(*self.tree_gastos.get_children())
        gastos_updated = Gasto.select()
        for row in gastos_updated:
            self.tree_gastos.insert("", "end", text=str(row.id), values=(row.name, row.amount, row.get_formated_date()))

    def eliminar(self, t_categoria):
        """Elimina una categoría seleccionada y todos los gastos asociados a ella.

        Args:
            item_focus: El ítem seleccionado en el widget Treeview.
            t_categoria (Treeview): Widget Treeview que muestra la lista de categorías.
        """
        item_focus = t_categoria.focus()
        item_id = t_categoria.item(item_focus)["text"]
        print(f"Se eliminará la categoría id: {item_id}")

        m_cat = Categoria().get(Categoria.id==item_id)
        gastos = Gasto.select().where(Gasto.categoria==m_cat.id)

        size_gastos = len(gastos)
        if size_gastos > 0 and askyesno("Continuar", f"Hay {size_gastos} gastos asociados a esta categoria y serán eliminados"):
            self.eliminar_categoria_gastos_asociados(gastos)
            m_cat.delete_instance()
            t_categoria.delete(item_focus)
            print("ELIMINASTE CATEGORIA")

        if size_gastos == 0:
            m_cat.delete_instance()
            t_categoria.delete(item_focus)

    def editar(self, var_categoria, t_categoria):
        """Edita el nombre de una categoría seleccionada.

        Args:
            var_categoria (StringVar): Variable de control para el campo de entrada de categoría.
            t_categoria (Treeview): Widget Treeview que muestra la lista de categorías.
        """
        categoria = var_categoria.get()

        if categoria == "" or categoria is None:
            return

        if askyesno("Editar", f"Vas a editar la categoría seleccionada por {var_categoria.get()}"):
            item_focus = t_categoria.focus()
            print(item_focus)
            categoria_id = t_categoria.item(item_focus)['text']
            t_categoria.delete(item_focus)

            m_cat = Categoria().update(name=categoria).where(Categoria.id==categoria_id)
            m_cat.execute()

            t_categoria.insert("", "end", text=str(categoria_id), values=(categoria,))
            print(f"EDITASTE CATEGORIA {categoria}")

    def set_tree_gastos(self, t_gastos):
        self.tree_gastos = t_gastos

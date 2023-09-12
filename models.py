import datetime
from peewee import Model, CharField, DecimalField, ForeignKeyField, DateTimeField, SqliteDatabase, OperationalError

db = SqliteDatabase("expense_manager_pew.db")


class BaseModel(Model):
    class Meta:
        database = db


class Categoria(BaseModel):
    """Clase que representa una categoría de gastos.

    Esta clase define una entidad "Categoría" que se utiliza para organizar los gastos.

    Atributos:
        name (str): El nombre de la categoría. Debe ser único.
    """
    name = CharField(unique=True)


class Gasto(BaseModel):
    """Clase que representa un gasto.

    Esta clase define una entidad "Gasto" que registra información sobre un gasto específico.

    Atributos:
        name (str): El nombre o descripción del gasto.
        amount (float): La cantidad del gasto.
        categoria (Categoria): La categoría a la que pertenece el gasto.
        date (datetime): La fecha y hora en que se realizó el gasto. Por defecto, se establece en la fecha y hora actual.
    """
    name = CharField()
    amount = DecimalField(max_digits=5, decimal_places=2)
    categoria = ForeignKeyField(Categoria, backref='gastos')
    date = DateTimeField(default=datetime.datetime.now)

    def get_formated_date(self):
        """Obtiene la fecha del gasto en formato 'dd-mm-YYYY'.

        Returns:
            str: La fecha del gasto en formato 'dd-mm-YYYY'.
        """
        return self.date.strftime("%d-%m-%Y")


try:
    db.connect()
    db.create_tables([Categoria, Gasto])
except OperationalError as ex:
    print(f"Error al conectar la base de datos o crear tablas: {ex}")
    raise ex

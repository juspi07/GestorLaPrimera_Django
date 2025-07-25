# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
#from django.db.models import UniqueConstraint, Index


class Cambios(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    cuit = models.CharField(db_column='Cuit', max_length=45)  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cantidad = models.CharField(db_column='Cantidad', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cambios'


class Clientes(models.Model):
    aid = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    #pk = models.CompositePrimaryKey('cuit', 'provincia', 'direccion')
    cuit = models.CharField(db_column='cuit', max_length=13, unique=True)  # Field name made lowercase.
    razons = models.CharField(db_column='RazonS', max_length=60)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=45)  # Field name made lowercase.
    provincia = models.CharField(db_column='Provincia', max_length=45)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=45)  # Field name made lowercase.
    responsabilidad = models.ForeignKey('RespIva', models.DO_NOTHING, db_column='Responsabilidad')  # Field name made lowercase.
    descuento = models.CharField(db_column='Descuento', max_length=45)  # Field name made lowercase.
    recargo = models.CharField(db_column='Recargo', max_length=45)  # Field name made lowercase.

    class Meta:
        #constraints = [
        #models.UniqueConstraint(fields=['cuit', 'provincia', 'direccion'], name='composite_primary_key'),
        #    Index(fields=['cuit', 'provincia', 'direccion'], name='composite_index')
        #]
        managed = False
        db_table = 'clientes'
        unique_together = (('cuit', 'provincia', 'direccion'),)


class Comprobantes(models.Model):
    descripcion = models.CharField(db_column='Descripcion', primary_key=True, max_length=45)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comprobantes'


class Cuentastc(models.Model):
    descripcion = models.CharField(db_column='Descripcion', primary_key=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cuentastc'


class Grupos(models.Model):
    idgrupo = models.IntegerField(db_column='IdGrupo', primary_key=True)  # Field name made lowercase.
    nombregrupo = models.CharField(db_column='NombreGrupo', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'grupos'

'''
class Idproductos(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=45)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.
    id_b = models.CharField(db_column='ID_B', max_length=45, blank=True, null=True)  # Field name made lowercase.
    conjunto = models.ForeignKey(Cuentastc, models.DO_NOTHING, db_column='Conjunto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'idproductos'
'''

class Listas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=30, unique=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'listas'


class Productos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    lista = models.ForeignKey(Listas, models.DO_NOTHING, to_field='nombre', db_column='Lista', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True, max_length=70)  # Field name made lowercase.
    precio = models.CharField(db_column='Precio', max_length=45, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    iva = models.CharField(db_column='Iva', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productos'


class RespIva(models.Model):
    descripcion = models.CharField(db_column='Descripcion', primary_key=True, max_length=45)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'resp_iva'


class Ventas(models.Model):
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    comprobante = models.CharField(db_column='Comprobante', max_length=45)  # Field name made lowercase.
    n_fact = models.CharField(db_column='N_fact', max_length=13)  # Field name made lowercase.
    cuit = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='cuit', to_field='cuit')  # Field name made lowercase.
    pan105 = models.CharField(db_column='Pan105', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pan21 = models.CharField(db_column='Pan21', max_length=45, blank=True, null=True)  # Field name made lowercase.
    exento = models.CharField(db_column='Exento', max_length=45, blank=True, null=True)  # Field name made lowercase.
    iva105 = models.CharField(db_column='Iva105', max_length=45, blank=True, null=True)  # Field name made lowercase.
    iva21 = models.CharField(db_column='Iva21', max_length=45, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=45, blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='Total', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ventas'
        unique_together = ('comprobante', 'n_fact')

class VentaProductos(models.Model):
    #pk = models.CompositePrimaryKey('comprobante', 'n_fact')
    comprobante = models.ForeignKey(Comprobantes, models.DO_NOTHING, db_column='Comprobante')  # Field name made lowercase.
    n_fact = models.ForeignKey(Ventas, models.DO_NOTHING, db_column='N_fact')  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=45)  # Field name made lowercase.
    cantidad = models.CharField(db_column='Cantidad', max_length=10)  # Field name made lowercase.
    precio_u = models.CharField(db_column='Precio_U', max_length=45)  # Field name made lowercase.
    cambio = models.CharField(db_column='Cambio', max_length=8)  # Field name made lowercase.
    total = models.CharField(db_column='Total', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'venta_productos'
        unique_together = (('comprobante', 'n_fact'),)

class Zonas(models.Model):
    nombre = models.CharField(db_column='Nombre', primary_key=True, max_length=45)  # Field name made lowercase.
    dgr = models.CharField(db_column='Dgr', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'zonas'

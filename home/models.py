from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password

class Accesos(models.Model):
        id = models.AutoField(primary_key=True)
        acceso_predict = models.CharField(max_length=20)
        descripcion = models.CharField(max_length=50)
        class Meta:
            db_table = 'accesos'

class Marca_Venado(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    class Meta:
        db_table = 'Marcas_Venado'
    def __str__(self):
        return self.marca

class Producto_venado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=50)
    cont_net = models.CharField(max_length=50)
    linea_producto = models.CharField(max_length=50)
    marca_id = models.ForeignKey(Marca_Venado, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Productos_venado'
    def __str__(self):
        return self.nombre_producto

class Produccion_venado(models.Model):
        id = models.AutoField(primary_key=True)
        producto = models.ForeignKey(Producto_venado, on_delete=models.CASCADE)
        marca_producto = models.ForeignKey(Marca_Venado, on_delete=models.CASCADE)
        fecha_produccion_mensual = models.CharField(max_length=15)
        cantidad_produccion = models.IntegerField()

        class Meta:
            db_table = 'produccion_venado'

class Distribuciones_venado(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto_venado, on_delete=models.CASCADE)
    fecha_distribucion_mensual = models.CharField(max_length=15)
    canal_horizontal = models.IntegerField()
    canal_tradicional = models.IntegerField()
    canal_moderno = models.IntegerField()
    total_cantidad_distribucion = models.IntegerField(default=0)

    class Meta:
        db_table = 'Distribucion_venado'

    def save(self, *args, **kwargs):
        self.total_cantidad_distribucion = self.canal_horizontal + self.canal_tradicional + self.canal_moderno
        super(Distribuciones_venado, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
class UsuariosManager(BaseUserManager):
    def create_user(self, nombre_usuario, correo, acceso, password=None):
        if not nombre_usuario:
            raise ValueError('El nombre de usuario es obligatorio')
        if not correo:
            raise ValueError('El correo es obligatorio')
        if not acceso:
            raise ValueError('El acceso es obligatorio')

        user = self.model(
            nombre_usuario=nombre_usuario,
            correo=correo,
            acceso=acceso,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, correo, acceso, password):
        user = self.create_user(
            nombre_usuario=nombre_usuario,
            correo=correo,
            acceso=acceso,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuarios(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.CharField(max_length=50, unique=True)
    acceso = models.ForeignKey(Accesos, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=100, null=True, blank=True)

    objects = UsuariosManager()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['correo', 'acceso']
    def verificar_password(self, password):
        return check_password(password, self.password)
    def __str__(self):
        return self.nombre_usuario

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'usuarios'
class AuditoriaPredicciones(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    nomproducto = models.CharField(max_length=255)
    Fechaseleccionada = models.DateField()
    fechaprediccion = models.DateField()
    horaprediccion = models.TimeField()
    cantprediccion = models.IntegerField()
    modelo = models.CharField(max_length=255)
    arL1 = models.FloatField()
    maL1 = models.FloatField()
    arSL2 = models.FloatField()
    sigma2 = models.FloatField()
    pdf = models.FileField(upload_to='pdfs/')
    class Meta:
        db_table = 'auditoria_predicciones'
    def __str__(self):
        return self.usuario

"""Peewee migrations -- 001_auto.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class AccessSecret(pw.Model):
        id = pw.AutoField()
        delete_flag = pw.BooleanField()
        create_time = pw.DateTimeField()
        update_time = pw.DateTimeField()
        access_key_id = pw.CharField(max_length=64)
        access_key_secret = pw.CharField(max_length=64)

        class Meta:
            table_name = "access_secret"

    @migrator.create_model
    class Pic(pw.Model):
        id = pw.AutoField()
        delete_flag = pw.BooleanField()
        create_time = pw.DateTimeField()
        update_time = pw.DateTimeField()
        user_id = pw.IntegerField(index=True)
        title = pw.CharField(max_length=32, null=True)
        path = pw.CharField(max_length=128)
        description = pw.CharField(max_length=64, null=True)

        class Meta:
            table_name = "pic"

    @migrator.create_model
    class Role(pw.Model):
        id = pw.AutoField()
        delete_flag = pw.BooleanField()
        create_time = pw.DateTimeField()
        update_time = pw.DateTimeField()
        codename = pw.CharField(max_length=32, unique=True)
        name = pw.CharField(max_length=32, unique=True)
        description = pw.CharField(max_length=64, null=True)

        class Meta:
            table_name = "role"

    @migrator.create_model
    class Setting(pw.Model):
        id = pw.AutoField()
        delete_flag = pw.BooleanField()
        create_time = pw.DateTimeField()
        update_time = pw.DateTimeField()
        codename = pw.CharField(max_length=64)
        name = pw.CharField(max_length=64)
        value = pw.CharField(max_length=64)

        class Meta:
            table_name = "setting"

    @migrator.create_model
    class User(pw.Model):
        id = pw.AutoField()
        delete_flag = pw.BooleanField()
        create_time = pw.DateTimeField()
        update_time = pw.DateTimeField()
        username = pw.CharField(max_length=64)
        password = pw.CharField(max_length=128)
        nickname = pw.CharField(max_length=32)
        head_img = pw.CharField(max_length=64)
        gender = pw.CharField(max_length=12)
        email = pw.CharField(max_length=64, null=True, unique=True)
        phone = pw.CharField(max_length=11, null=True, unique=True)
        role_id = pw.IntegerField()

        class Meta:
            table_name = "user"

    @migrator.create_model
    class UserSecret(pw.Model):
        id = pw.AutoField()
        delete_flag = pw.BooleanField()
        create_time = pw.DateTimeField()
        update_time = pw.DateTimeField()
        user_id = pw.IntegerField(index=True)
        secret = pw.CharField(max_length=64)

        class Meta:
            table_name = "user_secret"

    @migrator.create_model
    class Video(pw.Model):
        id = pw.AutoField()
        delete_flag = pw.BooleanField()
        create_time = pw.DateTimeField()
        update_time = pw.DateTimeField()
        user_id = pw.IntegerField(index=True)
        title = pw.CharField(max_length=32, null=True)
        description = pw.CharField(max_length=64, null=True)
        pic = pw.CharField(max_length=128)
        path = pw.CharField(max_length=128)

        class Meta:
            table_name = "video"


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('video')

    migrator.remove_model('user_secret')

    migrator.remove_model('user')

    migrator.remove_model('setting')

    migrator.remove_model('role')

    migrator.remove_model('pic')

    migrator.remove_model('access_secret')

import sqlite3
import os

from sakurajima.db.backends.base.schema import BaseSchemaAdmin
from sakurajima.utils.path import get_storage_path, join_path


class SchemaAdmin(BaseSchemaAdmin):
    def __init__(self):
        super(SchemaAdmin, self).__init__(sqlite3.connect)
        self.__connection = None

    @property
    def connection(self) -> any:
        """
        Return the database connection.
        """
        if self.__connection is None:
            storage_path = get_storage_path()
            path = join_path(storage_path, self.db_name + '.sqlite3')

            self.__connection = sqlite3.connect(path)
        return self.__connection

    def get_disconnect(self) -> None:
        """
        This is used to disconnect database.
        """
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def create_database(self, kwargs) -> None:
        """
        Create a database.
        """
        storage_path = get_storage_path()
        path = join_path(storage_path, kwargs['name'] + '.sqlite3')
        connection_object = sqlite3.connect(path)
        connection_object.close()

    def drop_database(self, kwargs):
        """
        Delete some database.
        """
        storage_path = get_storage_path()
        path = join_path(storage_path, kwargs['name'] + '.sqlite3')
        os.remove(path)

    def create_table(self, kwargs: dict) -> None:
        """
        Create some table with definitions.
        """
        template = self.schema_templates['create_table'] % kwargs
        self.connection.cursor().execute(template)
        self.connection.commit()
        self.get_disconnect()

    def drop_table(self, kwargs: dict) -> None:
        """
        Delete some table.
        """
        template = self.schema_templates['drop_table'] % kwargs
        kwargs.get('connection').cursor().execute(template)
        kwargs.get('connection').commit()
        self.get_disconnect()

    def alter_table(self, **kwargs) -> None:
        pass

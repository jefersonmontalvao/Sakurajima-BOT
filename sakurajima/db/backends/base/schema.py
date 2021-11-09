class BaseSchemaAdmin:
    # Overridable sql templates.
    schema_templates = {
        'create_database': 'CREATE DATABASE %(name)s',
        'create_table': 'CREATE TABLE IF NOT EXISTS %(to_name)s (%(to_definitions)s)',
        'drop_database': 'DROP DATABASE %(name)s',
        'drop_table': 'DROP TABLE IF EXISTS %(name)s',
        'alter': 'ALTER TABLE %(name)s --',
    }

    # Overridable sql templates.
    operation_templates = {
        'update': 'UPDATE TABLE %(name)s',
        'insert': 'INSERT INTO %(table)s (%(columns)s) VALUES (%(values)s)',
        'delete': 'DELETE FROM TABLE %(name)s WHERE %(condition)s',
        'truncate': 'TRUNCATE TABLE %(name)s'
    }

    def __init__(self, connector) -> None:
        from sakurajima.conf import DATABASE

        self.db_name = DATABASE['NAME']
        self.connector = connector
        self.__connection = None

    @property
    def connection(self) -> any:
        """
        Return the database connection.
        Need to be subscribed.
        """
        return None

    def get_disconnect(self) -> None:
        """
        This is used to disconnect database.
        Need to be subscribed.
        """
        pass

    def create_database(self, kwargs) -> None:
        pass

    def drop_database(self, kwargs) -> None:
        pass

    def create_table(self, kwargs) -> None:
        pass

    def drop_table(self, kwargs) -> None:
        pass

    def alter_table(self, kwargs) -> None:
        pass

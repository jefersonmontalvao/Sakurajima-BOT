from .schema import BaseSchemaAdmin


class BaseOperations:
    @staticmethod
    def op_update(connection, **kwargs):
        pass

    @staticmethod
    def op_insert(connection, **kwargs):
        template = BaseSchemaAdmin.operation_templates.get('insert') % kwargs
        print(template)
        cursor = connection.cursor()
        cursor.execute(template)
        connection.commit()

    @staticmethod
    def op_delete(connection, **kwargs):
        pass

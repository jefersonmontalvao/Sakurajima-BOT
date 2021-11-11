import re
import importlib


class ModelsHandler:
    """
    Class responsible to run the database dynamically and
    execute models.
    """
    def __init__(self):
        # Define few variables.
        self.backend = None
        self.schema_data = None

        # Set the database backend module.
        # Anyway, it set the "backend" variable a instance of a backend module
        # that is in "sakurajima.db.backends" module.
        self.set_db_backend()

        # Set the values of schema_data property.
        self.import_models()

        print(self.backend.schema.SchemaAdmin())
        print(self.backend.operations.Operations())


    @property
    def schema_data(self) -> tuple:
        """
        Property get of data of data.
        """
        value = getattr(self.__class__, '__schema_data')
        if value is None:
            setattr(self.__class__, '__schema_data', ())
            value = getattr(self.__class__, '__schema_data')
        return value

    @schema_data.setter
    def schema_data(self, value):
        """
        Property set of data of data.
        """
        if isinstance(value, (list, tuple)):
            setattr(self.__class__, '__schema_data', tuple(value))
        elif value is None:
            setattr(self.__class__, '__schema_data', value)
        else:
            # TODO: Implement this later.
            pass

    def set_db_backend(self):
        """
        Import dynamically the module.
        """
        from sakurajima.conf.settings import DATABASE

        module_path = DATABASE.get('BACKEND')
        components = module_path.split('.')
        module = importlib.import_module(components[0])

        for comp in components[1:]:
            module = getattr(module, comp)

        self.backend = module

    def import_models(self):
        """
        Import all models created from sakurajima.models
        and extract some data about the model.
        """
        # import few modules.
        import sakurajima.models as models

        from sakurajima.db.models import Model

        # Get a tuple with a list of components in string data.
        module_components = tuple(filter(lambda comp: not re.search('^__.+__$', comp), dir(models)))

        # Variable to store models instance that is found on module components to return it.
        models_data_repr_list = list()

        for component in module_components:
            # Get the component object:
            ModelTemplateObject = getattr(models, component)
            if isinstance(ModelTemplateObject, object.__class__) and \
                    issubclass(ModelTemplateObject.__class__, Model.__class__):
                # Instantiate the model class.
                # Is important to say that class return a dictionary with some data
                # about the database model(name, fields...).
                instance = ModelTemplateObject()
                models_data_repr_list.append(instance)

        self.schema_data = tuple(models_data_repr_list)

    def initialize_database_models(self):
        # TODO: Check if the database has the models
        # TODO: If not, create the models in database
        # TODO: else if has the model but with modifications, use alter table to alter this model in database.
        pass

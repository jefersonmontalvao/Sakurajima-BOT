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

        # Set the backend module.
        self.set_db_backend()

        # Set the values of schema_data property.
        self.import_models()

        print(self.schema_data)

    @property
    def schema_data(self):
        """
        Property get of data of data.
        """
        try:
            value = getattr(self.__class__, '_meta_data')
        except AttributeError:
            setattr(self.__class__, '_meta_data', [])
            value = getattr(self.__class__, '_meta_class')
        return value

    @schema_data.setter
    def schema_data(self, value):
        """
        Property set of data of data.
        """
        if isinstance(value, (list, tuple)):
            setattr(self.__class__, '_meta_data', tuple(value))

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
        models_instances = list()

        for component in module_components:
            # Get the component object:
            ModelTemplateObject = getattr(models, component)
            if isinstance(ModelTemplateObject, object.__class__) and \
                    issubclass(ModelTemplateObject.__class__, Model.__class__):
                # Instantiate the model class.
                # Is important to say that class return a dictionary with some data
                # about the database model(name, fields...).
                models_instances.append(ModelTemplateObject())

        self.schema_data = tuple(models_instances)

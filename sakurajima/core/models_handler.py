import re
import importlib


class ModelsHandler:
    """
    Class responsible to run the database dynamically and
    execute models.
    """
    def __init__(self):
        # Define few variables.
        self.__class__.backend = None
        self.models_data = None

        # Set the database backend module.
        # Anyway, it set the "backend" variable a instance of a backend module
        # that is in "sakurajima.db.backends" module.
        self.set_db_backend()

        # Set the values of schema_data property.
        self.import_models()

        # Initialize
        self.__initialize_database_models()

        # Tests
        self.backend.schema.SchemaAdmin()
        self.backend.operations.Operations()


    @property
    def models_data(self) -> tuple:
        """
        Property get of data of data.
        """
        value = getattr(self.__class__, '__schema_data')
        if value is None:
            setattr(self.__class__, '__schema_data', ())
            value = getattr(self.__class__, '__schema_data')
        return value

    @models_data.setter
    def models_data(self, value):
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

        self.__class__.backend = module

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

        self.models_data = tuple(models_data_repr_list)

    def __initialize_database_models(self):
        """
        This is the function that initialize the models in database if it was not created,
        and also do alter table operations to keep the database schema updated.
        """
        # Define few variables variables with data about models and tables in database.
        # Get tables that is in database.
        database_tables = self.backend.schema.SchemaAdmin().show_tables()

        # Get tables that was made in models.
        get_model_table_name = lambda dt: dt.get('NAME')
        model_names = tuple(map(get_model_table_name, self.models_data))

        # Check if some model is not in database and perform a action.
        # Return a model name string, it is used to name the table.
        for model_name in model_names:
            # Check if not in database and perform a action.
            if model_name not in database_tables:
                # Get the dict of the model name that is not in database_tables list.
                filter_by_name_function = lambda dt: dt.get('NAME') == model_name
                filtered_object = filter(filter_by_name_function, self.models_data)

                # Model dict data.
                model_data = tuple(filtered_object)[0]

                # Get fields.
                fields = model_data.get('FIELDS')

                # Module for get the from base models Field object.
                import sakurajima.db.models.models as db_models

                # Variable for accumulate data to compose definitions of a column.
                definitions_list = []
                for field in fields:
                    for item in field.items():
                        # Check if the field is really a field class
                        try:
                            field_object = getattr(db_models, item[1].__class__.__name__)
                        except AttributeError:
                            field_object = item[1].__class__
                        finally:
                            is_field_class = issubclass(field_object, db_models.Field)

                        # If attribute is a Field class, this action will take all data about
                        # about this field and insert in a dict named args to be args of field
                        # field creation template.
                        if is_field_class:
                            args = {
                                'field_name': item[0]
                            }
                            # Get type arg dynamically, it depends of database backend module.
                            args.update(self.backend.schema.SchemaAdmin.data_types)

                            # Append the definition to definitions list.
                            definitions_list.append((item[1].field_creation_template % args))

                # With definition list, make definitions separated by ', ' and use it was a arg in kwargs.
                definitions = ', '.join([definition for definition in definitions_list])
                kwargs = {
                    'to_name': model_data['NAME'],
                    'to_definitions': definitions
                }

                # Create table with kwargs.
                self.backend.schema.SchemaAdmin().create_table(kwargs)
            else:
                # TODO: else if has the model but with modifications, use alter table to alter this model in database.
                pass

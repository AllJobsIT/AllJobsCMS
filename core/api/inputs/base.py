from graphene import InputObjectType


class BaseInputObject(InputObjectType):

    def validate(self, info, error_store):
        for field_name, field_class in self._meta.fields.items():
            validate_method_name = f'validate_{field_name}'
            validate_method = getattr(self, validate_method_name, None)
            if callable(validate_method):
                try:
                    validate_method(info, error_store)
                except BaseException as err:
                    error_message = str(err)
                    field = "{}{}{}".format(err.parent_field, '.' if err.parent_field else "", field_name)
                    error_store.add_error(message=error_message, field=field)

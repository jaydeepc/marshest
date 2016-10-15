class MarshModel:

    def serialize(self, format):
        try:
            #the format is here to provide support for xml later
            serialize_function = '_object_to_{0}'.format(format)
            return getattr(self, serialize_function)()
        except:
            raise Exception("Failed to Serialize")

        return None

    @classmethod
    def deserialize(cls, serialized_str, format):
        model_obj = None
        if serialized_str and len(serialized_str) > 0:
            try:
                deserialize_function = '_{0}_to_object'.format(format)
                model_obj = getattr(cls, deserialize_function)(serialized_str)
            except:
                raise Exception("Failed to Deserialize")

        return model_obj

    # Function For Serialization
    def _object_to_json(self):
        raise Exception("No implementation found")

    # Function For Deserialization
    @classmethod
    def _json_to_object(cls, serialized_str):
        raise Exception("No implementation found")
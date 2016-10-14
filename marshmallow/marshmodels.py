class AutoMarshallingModel:

    def serialize(self, format_type):
        serialization_exception = None
        try:
            serialize_method = '_obj_to_{0}'.format(format_type)
            return getattr(self, serialize_method)()
        except Exception as serialization_exception:
            raise Exception("Failed to Serialize")

        return None

    @classmethod
    def deserialize(cls, serialized_str, format_type):
        model_object = None
        deserialization_exception = None
        if serialized_str and len(serialized_str) > 0:
            try:
                deserialize_method = '_{0}_to_obj'.format(format_type)
                model_object = getattr(cls, deserialize_method)(serialized_str)
            except Exception as deserialization_exception:
                raise Exception("Failed to Deserialize")

        return model_object

    # Serialization
    def _obj_to_json(self):
        raise NotImplementedError

    # Deserialization
    @classmethod
    def _json_to_obj(cls, serialized_str):
        raise NotImplementedError
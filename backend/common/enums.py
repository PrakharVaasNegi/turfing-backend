class Enum:
    """Minimal class-attribute Enum, matching pushowl-backend's common.enums.Enum."""

    @classmethod
    def get_all_attribute_values(cls):
        return [
            value
            for key, value in vars(cls).items()
            if not key.startswith("_") and not callable(value)
        ]

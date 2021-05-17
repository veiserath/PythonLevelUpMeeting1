from database import Base


class CaseMixin:
    """Contains method used for exporting Models to PascalCase expected in API responses."""
    __abstract__ = True

    def export(self):
        """Return dict with non-private object attributes converted to PascalCase. If object are nested returned dict
        is also nested."""
        exported_object = {}
        for attr, val in self.__dict__.items():
            if isinstance(val, Base):
                exported_object[self.to_pascal(attr)] = val.export()
            elif not attr.startswith('_'):
                exported_object[self.to_pascal(attr)] = val
        return exported_object

    @staticmethod
    def to_pascal(text):
        """Return text converted from snake_case to PascalCase with special_texts conversion."""
        special_texts = {
            'Id': 'ID',
            'Homepage': 'HomePage'
        }

        output_text = ''.join(word.capitalize() for word in text.split('_'))
        for old, new in special_texts.items():
            output_text = output_text.replace(old, new)

        return output_text

class MultipleSerializerMixin:
    # A mixin is class tha deos'nt work on it's on
    # It adds fonctionnalities to classes tha extends it
    default_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retreive' and self.default_serializer_class is not None:
            # If the action is a retrieve we return the retrieve serializer
            return self.default_serializer_class
        return super().get_serializer_class()

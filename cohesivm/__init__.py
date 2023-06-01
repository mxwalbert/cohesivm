import pint

units = pint.UnitRegistry()


class InterfaceType:
    """Contains types of interfaces as constants which are assigned to an Interface class. Each interface type is
    implemented as private class which implements the __str__ method."""
    class _HiLo:
        def __str__(self):
            return 'Consist of a "HI" terminal which is the positive or high-voltage output used for sourcing voltage' \
                   'or current and a "LO" terminal which serves as the negative or low-voltage reference.'

    HI_LO = _HiLo()

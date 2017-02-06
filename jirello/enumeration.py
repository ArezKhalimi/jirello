class Enumeration(object):
    """
    A small helper class for more readable enumerations,
    and compatible with Django's choice convention.
    You may just pass the instance of this class as the choices
    argument of model/form fields.
    """

    def __init__(self, enum_list):
        self.enum_list = [(item[0], item[2]) for item in enum_list]
        self.enum_dict = {}

        for item in enum_list:
            self.enum_dict[item[1]] = item[0]

    def __contains__(self, v):
        return (v in self.enum_list)

    def __len__(self):
        return len(self.enum_list)

    def __getitem__(self, v):
        if isinstance(v, basestring):
            return self.enum_dict[v]
        elif isinstance(v, int):
            return self.enum_list[v]

    def __getattr__(self, name):
        return self.enum_dict[name]

    def __iter__(self):
        return self.enum_list.__iter__()

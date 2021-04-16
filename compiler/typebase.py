class TypeBase:
    def __init__(self):
        ...

    def typeparams(self, typename):
        doc = getattr(self, typename).__doc__
        return [
            x for x in doc.split("\n") if x and doc is not None
        ]



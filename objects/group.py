class Group(list):
    def __init__(self, _map, iterable=None):
        self._map = _map
        if iterable is None:
            iterable = []
        return super().__init__(iterable)

    def update(self):
        auxiliar_list = self[:]
        for _object in auxiliar_list:
            _object.update()

    def append(self, value):
        self._map[value.y][value.x].append(value)
        return super().append(value)

    def remove(self, value):
        self._map[value.y][value.x].remove(value)
        return super().remove(value)
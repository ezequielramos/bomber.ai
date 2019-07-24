class Cell(list):
    def __init__(self, x, y, iterable=None):
        self.x = x
        self.y = y
        self.up = None
        self.down = None
        self.left = None
        self.right = None

        if iterable is None:
            iterable = []
        return super().__init__(iterable)

    def __eq__(self, value):
        return id(self) == id(value)

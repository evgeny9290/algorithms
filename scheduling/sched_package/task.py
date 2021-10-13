class Task:
    def __init__(self, name, start, end, weight=1):
        self.name = name
        self.start = start
        self.end = end
        self.weight = weight

    def __str__(self):
        return f'{self.name}: start: {self.start}, end: {self.end}, weight: {self.weight}'

from models.entities.Entity import Entity


class Lecture(Entity):

    def dict(self):
        return vars(self)

    def __repr__(self):
        return f'{vars(self)}'

    def __init__(self, _id=0, title='', duration=0, path='', source=''):
        super().__init__(_id=_id, title=title)
        self.duration = duration
        self.path = path
        self.source = source
        self.downloaded = False

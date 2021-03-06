from models.entities.Entity import Entity
from models.utils import Utils


class Course(Entity):

    def calculate_total_duration(self):
        duration = 0.0
        for lecture in self.lectures:
            duration += lecture.duration
        return Utils.from_secs_to_time(duration)

    def dict(self):
        return vars(self)

    def __repr__(self):
        return f'{vars(self)}'

    def __init__(self, _id=0, title='', source='', path='', description='', lectures=None):
        super().__init__(_id=_id, title=title)
        self.description = description
        self.source = source
        self.path = path
        self.downloaded = False
        self.lectures = lectures
        self.duration = 0
        if not lectures:
            self.lectures = []
            self.duration = 0


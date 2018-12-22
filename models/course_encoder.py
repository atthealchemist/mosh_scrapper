from json import JSONEncoder


class CourseEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'dict'):
            return obj.dict()
        else:
            return JSONEncoder.default(self, obj)
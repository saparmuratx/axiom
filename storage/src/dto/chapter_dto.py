from src.models.storage_models import Chapter


class ChapterDTO:
    model: str = Chapter.__name__
    _object: Chapter

    def __init__(self, object: Chapter):
        self.object = object

    @property
    def object(self):
        return self._object

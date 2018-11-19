import pathlib
from .settings import MEDIA_DIR


def _init():
    path = pathlib.Path(MEDIA_DIR)
    if not path.exists():
        path.mkdir()


_init()

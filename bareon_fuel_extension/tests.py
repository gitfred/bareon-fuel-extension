from nailgun.extensions import BaseExtension


class NoElo(BaseExtension):
    pass


def test_ext():
    NoElo()

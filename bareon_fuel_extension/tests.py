from nailgun.extensions import BaseExtension


class NoElo(BaseExtension):
    name = 'noelo'
    description = 'no elo'
    version = '1.0.0'


def test_ext():
    NoElo()

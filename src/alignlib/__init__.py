from ._core import edit_distance

from pkg_resources import get_distribution as _get_distribution, DistributionNotFound as _DistributionNotFound

try:
    __version__ = _get_distribution(__name__).version
except _DistributionNotFound:
    pass

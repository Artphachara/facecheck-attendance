###########
# Imports #
###############################################################################

from importlib.metadata import version, PackageNotFoundError

#############
# Constants #
###############################################################################

try:
    __version__ = version('facecheck-attendance')
except PackageNotFoundError:
    pass

###############################################################################

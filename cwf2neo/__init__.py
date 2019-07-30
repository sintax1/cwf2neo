import logging
from .cwf2neo import CWF, config  # NOQA


logging.getLogger(__name__).addHandler(logging.NullHandler())

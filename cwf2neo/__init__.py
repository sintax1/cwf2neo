import logging
from .cwf2neo import CWF  # NOQA


logging.getLogger(__name__).addHandler(logging.NullHandler())

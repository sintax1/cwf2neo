import logging
from .cwf2neo import CWF  # NOQA
import confuse

config = confuse.Configuration('cwf2neo', __name__)

logging.getLogger(__name__).addHandler(logging.NullHandler())

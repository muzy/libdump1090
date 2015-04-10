try:                from  pylibmodes import libModeS, modesMessage
except ImportError: from .pylibmodes import libModeS, modesMessage

__all__  = ['libModeS','modesMessage']
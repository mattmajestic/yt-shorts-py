# conf.py
from moviepy.config import change_settings

# Replace the path below with the actual path to your ImageMagick 'magick.exe' file
# For example, if you installed ImageMagick in 'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI'
# and 'magick.exe' is in that directory, then use that path.
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

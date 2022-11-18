import time
from exif import Image
from datetime import datetime


def check_time_photo(path_photo):
  permissible_time = 120 # допустимое время (2 мин. или 120 сек.)
  with open(path_photo, 'rb') as img_file:
    img = Image(img_file)
  if img.has_exif:
    dt_photo = datetime.strptime(img.get("datetime_original"), '%Y:%m:%d %H:%M:%S')
    delta_time = abs(int(time.time() - dt_photo.timestamp()))
    if delta_time <= permissible_time:
      return True
    else:
      return False
  else:
    return False
#    This file is part of the Compressor distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/1Danish-00/CompressorQueue/blob/main/License> .

from decouple import config

try:
    APP_ID = config("APP_ID", default=24810254, cast=int)
    API_HASH = config("API_HASH", default="aadb42caec01695fa0a77c09b3e0ef47")
    BOT_TOKEN = config("BOT_TOKEN", default="7766680940:AAFRLQDTwpbreK-dZ-kk8fupB6tHkMBwk2g")
    DEV = 7543269959
    OWNER = config("OWNER", default="7543269959")
    FFMPEG = config(
        "FFMPEG",
        default='ffmpeg -i "{}" -preset ultrafast -c:v libx264 -s 1080x540 -x264-params "bframes=8:psy-rd=1:ref=3:aq-mode=3:aq-strength=0.8:deblock=1,1" -metadata title="Encoded By Night Owls" -metadata:s:v title="Anime Sensei" -metadata:s:a title="The Night Owls" -metadata:s:s title="The Night Owls" -pix_fmt yuv420p -crf 28 -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 1 "{}"'
    )
    TELEGRAPH_API = config("TELEGRAPH_API", default="https://api.telegra.ph")
    THUMB = config(
        "THUMBNAIL", default="https://graph.org/file/75ee20ec8d8c8bba84f02.jpg"
    )
except Exception as e:
    print("Environment vars Missing")
    print("something went wrong")
    print(str(e))
    exit()

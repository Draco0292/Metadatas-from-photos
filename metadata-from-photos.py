from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

#metadaten aus img holen
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

#geo infos extragieren
def get_geotagging(exif):
    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

#Degree, minutes, seconds format zu lati / long
def get_decimal_from_dms(dms, ref):

    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

#funktion um geoinfos zu lati und long umzuwandeln
def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)


#funktion um alle metadaten nacheinander auszugeben
def print_all(exif, loc):
    for tag_id in exif:
        tag = TAGS.get(tag_id, tag_id)
        data = exif.get(tag_id)
        #wenn anstatt die dummen gpsinfos die neuen ausgeben
        if tag == "GPSInfo":
            print("GPS: " + str(loc))
            #continue heißt der for loop wird weiter gemacht aka das nächste element im loop wird genommen
            continue
        print(f"{tag:25}: {data}")

    if isinstance(data, bytes):
        data = data.decode(encoding= "ISO-8859-1")

    

exif = get_exif(str(input("Paste Path: \n")))
#funktion geoinfo zahl zu degress minute second format ausühren
geoinfos = get_geotagging(exif)
#funktion degrees minute second format zu lati long ausühren
cords = get_coordinates(geoinfos)
#alles ausgeben
print_all(exif, cords)
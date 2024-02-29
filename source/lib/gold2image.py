import tempfile
from mojo.roboFont import CurrentGlyph

from AppKit import NSPNGFileType, NSBitmapImageRep

g = CurrentGlyph()

result = g.getRepresentation("money.money.money")
if result:
    im, offset = result

    imagePath = tempfile.mkstemp(suffix=".png")[1]

    imageRep = NSBitmapImageRep.imageRepWithData_(im.TIFFRepresentation())
    imageData = imageRep.representationUsingType_properties_(NSPNGFileType, None)

    imageData.writeToFile_atomically_(imagePath, True)

    g.addImage(path=imagePath, position=offset)

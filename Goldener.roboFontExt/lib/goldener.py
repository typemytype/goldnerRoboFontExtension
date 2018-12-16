from AppKit import NSImage
import drawBot
from outlinePen import OutlinePen
from mojo.events import addObserver
from mojo.drawingTools import image
from mojo.pens import DecomposePointPen
from mojo.UI import dontShowAgainMessage
from defcon import Glyph, registerRepresentationFactory


def setGoldGradient(minx, miny, maxx, maxy, levels=3):
    colors = []
    for i in range(levels):
        colors.extend([(.58, .49, .16), (1, .98, .75)])
    drawBot.linearGradient((minx, maxy), (maxx, miny), colors)


def GoldFactory(glyph, font=None, offset=10):
    glyph = RGlyph(glyph)
    box = glyph.bounds

    if box is None:
        return None

    margin = offset * 2
    minx, miny, maxx, maxy = box
    w = maxx - minx + margin * 2
    h = maxy - miny + margin * 2

    drawBot.newDrawing()
    drawBot.newPage(w, h)
    drawBot.translate(-minx + margin, -miny + margin)

    if font is None:
        font = glyph.font
    glyphSet = font

    g = glyph.copy()

    for component in reversed(g.components):
        decomposePen = DecomposePointPen(glyphSet, g.getPointPen())
        component.drawPoints(decomposePen)
        g.removeComponent(component)

    g.removeOverlap()

    minx, miny, maxx, maxy = g.bounds

    setGoldGradient(minx, miny, maxx, maxy)
    drawBot.drawGlyph(g)

    pen = OutlinePen(glyphSet, offset=offset)
    g.draw(pen)
    pen.drawSettings(drawInner=True, drawOuter=True)

    dest = RGlyph()
    pen.drawPoints(dest.getPointPen())

    setGoldGradient(minx, miny, maxx, maxy, 4)
    drawBot.drawGlyph(dest)

    pdf = drawBot.pdfImage()
    page = pdf.pageAtIndex_(0)
    image = NSImage.alloc().initWithData_(page.dataRepresentation())
    return image, (minx-margin, miny-margin)

registerRepresentationFactory(Glyph, "money.money.money", GoldFactory)

class GoldMaker(object):

    def __init__(self):
        text = "Every thing you space will be gold!"
        message = "To disable this Goldener extension, simply uninstall it from the preferences and restart."
        dontShowAgainMessage(text, message, dontShowAgainKey="Goldener.warning")
        addObserver(self, "goldie", "drawPreview")
        addObserver(self, "goldie", "spaceCenterDraw")

    def goldie(self, notification):
        g = notification["glyph"]
        result = g.getRepresentation("money.money.money")
        if result:
            im, offset = result
            image(im, offset)

GoldMaker()

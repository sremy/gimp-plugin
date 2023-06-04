#!/usr/bin/python
import math
from gimpfu import *


def create_image_from_text(label, font_name, font_size, auto_size, diag_size, angle=0):

    if auto_size:
        # Compare txt_width and diag_size
        txt_width,txt_height,ascent,descent = pdb.gimp_text_get_extents_fontname(label, font_size, PIXELS, font_name)  # in pixels
        font_size = 0.75 * diag_size / txt_width * font_size
        #pdb.gimp_message("new font_size = " + str(font_size))

    txt_width, txt_height, width, height = computeRotatedTextSize(label, font_name, font_size, angle)

    image_label = pdb.gimp_image_new(width, height, RGB)
    layer = pdb.gimp_text_fontname(image_label, None, (width - txt_width)/2, (height - txt_height)/2, label, 0, True, font_size, PIXELS, font_name)

    pdb.gimp_item_transform_rotate(layer, -angle, True, 0, 0)
    # display=pdb.gimp_display_new(image_label)
    return image_label

def computeRotatedTextSize(label, font_name, font_size, angle):
    (txt_width,txt_height,ascent,descent) = pdb.gimp_text_get_extents_fontname(label, font_size, PIXELS, font_name)  # in pixels
    #pdb.gimp_message("(width,height,angle) = " + str((txt_width,txt_height,angle)))
    width = txt_width * math.cos(angle) + txt_height * math.sin(angle) # not useful, because we take reuse only the drawable, not the image
    height = txt_height * math.cos(angle) + txt_width * math.sin(angle)
    return txt_width,txt_height,width,height



def add_watermark(timg, tdrawable, label, font_name, font_size, auto_size):
    """
    plug_in_bump_map http://oldhome.schmorp.de/marc/pdb/plug_in_bump_map.html

    NAME
    plug_in_bump_map - Create an embossing effect using an image as a bump map 
SYNOPSIS
    plug_in_bump_map (run_mode,image,drawable,bumpmap,azimuth,elevation,depth,xofs,yofs,waterlevel,ambient,compensate,invert,type) 
DESCRIPTION
    This plug-in uses the algorithm described by John Schlag, "Fast Embossing Effects on Raster Image Data" in Graphics GEMS IV (ISBN 0-12-336155-9). It takes a drawable to be applied as a bump map to another image and produces a nice embossing effect. 
MENUPATH
    <Image>/Filters/Map/Bump Map...
IMAGETYPES
    RGB*, GRAY*
INPUT ARGUMENTS
    TYPE	NAME	DESCRIPTION
    INT32	run_mode	The run mode { RUN-INTERACTIVE (0), RUN-NONINTERACTIVE (1), RUN-WITH-LAST-VALS (2) }
    IMAGE	image	Input image (unused)
    DRAWABLE	drawable	Input drawable
    DRAWABLE	bumpmap	Bump map drawable
    FLOAT	azimuth	Azimuth (0 <= azimuth <= 360)
    FLOAT	elevation	Elevation (0,5 <= elevation <= 90)
    INT32	depth	Depth (1 <= depth <= 65)
    INT32	xofs	X offset
    INT32	yofs	Y offset
    FLOAT	waterlevel	Level that full transparency should represent (0 <= waterlevel <= 1)
    FLOAT	ambient	Ambient lighting factor (0 <= ambient <= 1)
    INT32	compensate	Compensate for darkening (TRUE or FALSE)
    INT32	invert	Invert bumpmap (TRUE or FALSE)
    INT32	type	Type of map (LINEAR (0), SPHERICAL (1), SINUOSIDAL (2))
    """

    #pdb.gimp_message("timg: " + str(timg))
    #pdb.gimp_message("tdrawable: " + str(tdrawable))

    image_to_mark = timg
    #pdb.gimp_message("image_to_mark" + str(image_to_mark))
    #print "image_to_mark: " + str(image_to_mark)

    image_drawable = tdrawable # image_to_mark.active_drawable
    # bump_drawable = gimp.image_list()[1].active_drawable

    diag_size = math.sqrt(image_drawable.height*image_drawable.height + image_drawable.width*image_drawable.width)
    inclinaison = math.atan(float(image_drawable.height) / image_drawable.width)
    bump_image = create_image_from_text(label, font_name, font_size, auto_size, diag_size, inclinaison)
    bump_drawable = bump_image.active_drawable
    


    azimuth = 135
    elevation = 45
    depth = 10
    xofs = bump_drawable.width/2 - image_drawable.width/2
    yofs = bump_drawable.height/2 - image_drawable.height/2
    waterlevel = 0.5  # Level that full transparency should represent (0 <= waterlevel <= 1)
    ambient = 0
    compensate = True
    invert = True
    type_of_map = 2
    pdb.plug_in_bump_map(image_to_mark, image_drawable, bump_drawable, azimuth, elevation,
                     depth, xofs, yofs, waterlevel, ambient, compensate, invert, type_of_map)

    pdb.gimp_image_delete(bump_image)


register(
    "python-fu-autowatermark",
    "Add an embossing watermark",
    "Add an embossing watermark using the filter pdb.plug_in_bump_map",
    "Sebastien REMY",
    "Sebastien REMY",
    "2023",
    "<Image>/Filters/Emboss watermark",
    "RGB*, GRAY*",
    [
        # (PF_IMAGE, "timg", "Input image"),
        # (PF_DRAWABLE, "tdrawable", "Drawable"),
        (PDB_STRING, "label", "The label to mark", ""),
        (PF_FONT, "font_name", "Font", "Sans-serif Bold"),
        (PF_SPINNER, "font_size", "Font size", 200, (1, 1000, 1)),
        (PF_BOOL, "auto_size", "Adjust automatically the font size", True),
        # (PF_INT, "azimuth", "Azimuth", 135),
        # (PF_INT, "elevation", "elevation", 45),
        # (PF_INT, "depth", "Depth", 10)
    ],
    [],
    add_watermark)

main()


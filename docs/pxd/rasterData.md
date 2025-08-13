# Pixelmator Pro (.pxd) format: Raster layer format

[Raster layers](/docs/pxd/layer.md#raster) refer to a binary file representing the pixel contents of a file. They are stored in a Pixelmator-specific format.

There's a big difference between imported images and layers created in Pixelmator Pro.

## `PTBitmapBuffer`

The proprietary image format used for `.pxd`, and stored at `/data/{UUID}`. Working decoder is at [read_pt_bitmap.py](/pxdlib/read_pt_bitmap.py)

## `OriginalContentSource`

Most imported images are copied to `/data/{UUID}-OriginalContentSource`, meaning they can easily be read by Pillow.

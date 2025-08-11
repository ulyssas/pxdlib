"""Read, decode and convert PTBitmapBuffer."""

import logging
import struct
import traceback
import zlib
from typing import Optional

from PIL import Image

logging.basicConfig(level=logging.INFO)


def read_pt_bitmap(file: str):
    """A PTBitmapBuffer decoder."""
    with open(file, "rb") as f:
        data = f.read()

        # header (PTBitmapBuffer)
        header = str(struct.unpack_from("<16s", data, 0)[0].decode())
        if header != "PTBitmapBuffer__":
            logging.error("❌ Invalid PTBitmapBuffer.")
            return

        # version?
        version = struct.unpack_from("<I", data, 16)[0]

        # width, height
        width = struct.unpack_from("<I", data, 28)[0]
        height = struct.unpack_from("<I", data, 32)[0]
        logging.info(f"Detected dimensions: {width} x {height}")

        # ICC Profile (Big Endian 3bytes), without size int
        # ! ICC profile will be required for color management later
        icc_size = int.from_bytes(data[95:98], "big")
        logging.info(f"ICC profile length (from header): {icc_size} bytes")

        # compressed pixel data
        compressed_data = data[98 + icc_size :]
        decompressed_data = decode_zlib_pixels(compressed_data)
        if decompressed_data:
            save_pixel_data_as_image(
                raw_data=decompressed_data,
                width=width,
                height=height,
                output_name="blue_square_8x8.png",
            )


def decode_zlib_pixels(compressed_data: bytes) -> Optional[bytes]:
    """
    decompress zlib (raw deflate) pixel data in PTBitmapBuffer.
    """

    try:
        decompressed_data = zlib.decompress(compressed_data, -15)
        logging.info("✅ zlib (raw deflate) successfully decoded.")
        return decompressed_data
    except Exception as e:
        logging.error(f"❌ zlib (raw deflate) decode failed: {e}")

    return None


def save_pixel_data_as_image(
    raw_data: bytes, width: int, height: int, output_name: str = "output.png"
):
    """
    save raw pixel data (BGRA) from PTBitmapBuffer as PNG file.
    """
    # verify the data length matches image dimention.
    expected_length = width * height * 4
    if len(raw_data) != expected_length:
        logging.error("❌ data length does not match the image dimention.")
        logging.error(
            f"  expected length: {expected_length} bytes ({width}x{height}x4)"
        )
        logging.error(f"  actual length:   {len(raw_data)} bytes")
        return

    try:
        # create Pillow BGRA Image
        image = Image.frombytes("RGBA", (width, height), raw_data, "raw", "BGRA")
        image.save(output_name)
        logging.info(f"✅ successfully saved as image '{output_name}'.")

    except Exception as e:
        logging.error(f"❌ An error occurred while saving image: {e}")
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    read_pt_bitmap("test/view/data/917D65E5-33FC-4AF1-AB69-BF6C39B7C931")

import traceback
import zlib
from typing import Optional

from PIL import Image


def readbin():
    """ここでどこがPTBitmapBufferのピクセルデータなのか調べようと思う"""
    with open("test/view/data/Y", "rb") as f:
        # read the whole file and efficiently convert it to hex all at once
        # どこから読むのか考えないとね
        hexdata = f.read()
        print(hexdata)


def decode_pixel_buffer(compressed_data: bytes) -> Optional[bytes]:
    # zlib (raw deflate)
    # PTBitmapBuffer uses this format
    try:
        decompressed_data = zlib.decompress(compressed_data, -15)
        print("✅ zlib (raw deflate) デコードに成功しました。")
        return decompressed_data
    except Exception as e:
        print(f"ℹ️ zlib (raw deflate) デコードに失敗しました: {e}")

    print("❌ すべてのデコード試行に失敗しました。")
    return None


def save_pixel_data_as_image(
    raw_data: bytes, width: int, height: int, output_filename: str = "output.png"
):
    """
    save raw pixel data (BGRA) from PTBitmapBuffer as PNG file.
    """
    # verify the data length matches image dimention.
    expected_length = width * height * 4
    if len(raw_data) != expected_length:
        print(f"エラー: データ長が一致しません。")
        print(f"  期待された長さ: {expected_length} バイト ({width}x{height}x4)")
        print(f"  実際の長さ: {len(raw_data)} バイト")
        return

    try:
        # create Pillow BGRA Image
        image = Image.frombytes("RGBA", (width, height), raw_data, "raw", "BGRA")
        image.save(output_filename)
        print(f"✅ 画像が正常に '{output_filename}' として保存されました。")

    except Exception as e:
        print(f"❌ 画像の作成または保存中にエラーが発生しました: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    # from 8 x 8 #3374B6 image
    pixel = b"\xdb\x56\x62\xfc\x7f\xdb\x08\xc6\x00"

    # cyan & that blue
    pixel = b"\x3B\x79\x22\xFE\xFF\xB9\x47\x39\xFF\xCF\x3D\xCC\xFE\x7F\xEA\x7A\xDA\x9F\x93\xA7\x13\x80\x6C\x20\x1F\x2C\x96\xF3\xFF\xD4\x8D\x8C\x3F\x27\xAE\xA6\xFD\x3E\xB8\x33\xFC\xFB\xB1\x23\x31\xFF\x8E\x1F\x89\xF9\x7F\xE6\x56\x26\x44\x1E\xA8\xE6\xF4\xF5\xF4\x7F\xA7\xAE\xA5\xFD\x39\xB2\x39\xF4\xFF\xD1\x9D\xE1\xFF\x0F\x2E\xF5\xFD\x7F\xFC\x60\x34\x5C\xFE\xF8\x95\x94\x9F\x87\x2F\x24\x7F\x3E\xB4\x36\xE0\xFF\xDE\xA9\xAE\xFF\xF7\xCD\x70\xFF\x7F\xFC\x40\xF4\xFF\xB3\x77\x81\x66\x3C\x00\xDA\x79\x3E\xE9\xFF\xD1\x3D\x91\xFF\x0F\xCC\xF7\xFC\xBF\x77\xB2\xF3\xFF\xDD\x9D\xF6\xFF\x0F\xAD\x0B\xFC\x7F\xF6\x7E\x16\xD8\x8C\x23\xBB\x23\xFE\x1C\x58\xEC\x0D\x14\xB7\xFB\xBF\xAB\xD5\xE6\xFF\xAE\x16\x9B\xFF\x87\x56\xFA\xC1\xE5\x77\xF7\xD8\x43\xC4\x81\x72\x3B\x9B\xAD\xC1\xEC\xBD\x53\x5D\xFE\x9F\x38\x1E\xF7\xFF\xDC\xFD\x6C\x84\x5C\xA3\xD5\xFF\xED\x15\xA6\xFF\x77\x36\x58\x82\xD5\xED\xE9\x73\xFC\x7F\x70\x89\xCF\x7F\x00"

    decoded = decode_pixel_buffer(pixel)

    # 関数を呼び出して画像として保存
    if decoded:
        save_pixel_data_as_image(
            raw_data=decoded, width=8, height=8, output_filename="blue_square_8x8.png"
        )

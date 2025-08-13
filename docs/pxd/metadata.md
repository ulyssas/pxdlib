# Pixelmator Pro (.pxd) format: Metadata

## document_meta

<a id="meta"></a>

The [`document_meta`](readme.md#metadata) table has key-value pairs:

- `selected-layers` is an [`Arry`](readme.md#blobs). Each entry, an [`Strn`](readme.md#blobs), corresponds to a selected layer's `identifier`.
- `linked-layers` is an [`Arry`](readme.md#blobs) (unknown)

## document_info

<a id="info"></a>

The [`document_info`](readme.md#metadata) table has key-value pairs:

- `size`, `BDSz`, the width and height in pixels.
- `date` is, quite literally, the date and time – though the format is still a little Byzantine to me. If the last 8 bytes are interpreted as an `unsigned long long`, it is 100% linear to the modification time of metadata.info, but it’s not to any standard I recognise.
- `version`, a `DcVr`, which (unknown) somehow points to five [`Strn`](readme.md#blobs) entries: the name of the application ('Pixelmator Pro'), the Pixelmator version, a hex blob (unknown), the version of Mac used, and the macOS version.
- `no-preview`, an optional tag (unknown);
- `format`, `Frmt` (unknown);
- `content-id`, a `Strn` of the form `HistoryState-UUID-YYMMDD-HHMMSS`; the UUID is unknown, but the latter is the modification date;
- `metadata-data`, a UTF-8 encoded JSON, a [verstruct](readme.md#json) containing:
  - `resolution`, the print resolution of the document, a vercon with the tags `value` and `units` as 1 (pixels per inch) or 2 (pixels per cm);
  - `imageMetadata`, a verstruct with the tag `xmpData`, a base-64 encoded (UTF-8) XML document containing EXIF, TIFF and XMP data about resolution and modification dates.
- `print-info-data`, a PLIST containing mundane print data;
- `rulers-origin`, [`PTPt`](readme.md#blobs), the origin of the ruler for visual display purposes.
- `guides` is an [`Arry`](readme.md#blobs) of `Guid` blobs. Each `Guid` blob contains a short (nominally 1), an integer (the coordinate of the guide) and a short (0 if horizontal, 1 if vertical.) The coordinates are given relative to the top-left of the document, rather than the bottom-left as coordinates are given in.
- `slices-data`, a list of slices specified in JSON. (unknown).

## document_info

<a id="storable"></a>

The [`storable_info`](readme.md#metadata) table has the following keys:

- `originalImportedContentDocumentInfo`: present only if a `.pxd` file is imported from a `.pxm` file created by Pixelmator Classic.

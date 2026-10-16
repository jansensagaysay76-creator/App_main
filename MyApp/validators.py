from django.core.exceptions import ValidationError


def validate_pet_photo(uploaded_file):
    max_size = 5 * 1024 * 1024
    if uploaded_file.size > max_size:
        raise ValidationError("Choose a photo smaller than 5 MB.")

    header = uploaded_file.read(12)
    uploaded_file.seek(0)
    valid_image = (
        header.startswith(b"\xff\xd8\xff")
        or header.startswith(b"\x89PNG\r\n\x1a\n")
        or header.startswith((b"GIF87a", b"GIF89a"))
        or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
    )
    if not valid_image:
        raise ValidationError("Upload a valid JPG, PNG, GIF, or WebP image.")

import json
import sys

from pypdf import PdfReader


# Extract data for the fillable form fields in a PDF and outputs JSON that
# Claude uses to fill the fields. See forms.md


# This matches the format used by PdfReader `get_fields` and `update_page_form_field_values` methods.
def get_full_annotation_field_id(annotation):
    components = []
    while annotation:
        field_name = annotation.get('/T')
        if field_name:
            components.append(field_name)
        annotation = annotation.get('/Parent')
    return '.'.join(reversed(components)) if components else None
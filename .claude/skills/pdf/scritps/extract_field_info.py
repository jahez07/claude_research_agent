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


def make_field_dict(field, field_id):
    field_dict = {"field_id": field_id}
    ft = field.get('/FT')
    if ft == '/Tx':
        field_dict["type"] = "text"
    elif ft == "/Btn":
        field_dict["type"] = "checkbox" # radio groups handled separately
        states = field.get("/_States_", [])
        if len(states) == 2:
            # "/Off" seems to always be the unchecked value, as suggested by
            # https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pd#page=448
            # It can be either first or second in the "/_States_" list.
            if "/Off" in states:
                field_dict["checked_value"] = states[0] if states[0] != "/Off" else states[1]
                field_dict["unchecked_value"] = "/Off"
            else:
                print(f"Unexpected state values for checkbox `${field_id}`. Its checked and unchecked values may not be correct; if you're trying to check it, visually verify the results.")
                field_dict["checked_value"] = states[0]
                field_dict["unchecked_value"] = states[1]
    elif ft == "/Ch":
        field_dict["type"] = "choice"
        states = field.get("/_States_", [])
        field_dict["choice_options"] = [{
            "value": state[0],
            "text": state[1],
        } for state in states]
    else:
        field_dict["type"] = f"unknown ({ft})"
    return field_dict
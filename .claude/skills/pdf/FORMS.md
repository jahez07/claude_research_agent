**CRITICAL: You MUST complete these steps in order. Do not skip ahead to writing code**

If you need fill out a PDF form, first check to see if the PDF has fillable form fields. Run this script from this file's directory:
`python scripts/check_fillable_fields <file.pdf>`, and depending on the result go to either the "Fillable fields" or "Non-fillable fields" and follow these instructions.

# Fillable fields
If the PDF has fillable form fields:
- Run this script from this file's directory: `python scripts/extract_form_field_info.py <input.pdf> <field_info.json>`. It will create a JSON file with a list of fields in this format:
```
[
    {
        "filed_id": (unique ID for the field),
        "page": (page number, 1-based),
        "rect": ([left, bottom, right, top] bounding box in PDF coordinates, y=0 is the bottom of the page),
        "type": ("text", "checkbox", "radio_group", or "choice"),
    },
    // Radio groups have a "radio_options" list with the possible choices.
    {
        "field_id": (unique ID for the field),
        "page": (page number, 1-based),
        "type": "radio_group",
        "radio_options":[
            {
                "value": (set the field to this value to select this radio option),
                "rect": (bounding box for the radio button for this option)
            },
            // Other radio options
        ]
    },
    // Multiple choice fields have a "choice_options" list with the possible choices:
    {
        "field_id": (unique ID for the field),
        "page": (page number, 1-based),
        "type": "choice",
        "choice_options":[
            {
                "value": (set the field to this value to select this option)
                "text": (display text of the option)
            },
            // Other choice options
        ],
    }
]
```

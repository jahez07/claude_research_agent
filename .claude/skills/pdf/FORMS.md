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
- Convert the PDF to PNGs (one image for each page) with this script (run from this file's directory):
`python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
Then analyze the images to determine the purpose of each form field (make sure to convert the bounding box PDF coordinates to image coordinates).
- Create a `field_value.json` file in this format with the values to be entered for each field:
```
[
    {
        "field_id": "last_name", // Must match the field_id from `extract_form_field_info.py`
        "description": "The user's last name",
        "page": 1, // Must match the "page" value in field_info.json
        "value": "Simpson"
    },
    {
        "field_id": "Checkbox12",
        "description": "Checkbox to be checked if the user is 18 or over",
        "page": 1,
        "value": "/On" // If this is a checkbox, use its "checked_value" value to check it. If it's a radio button group, use one of the "value" values in "radio_options".
    },
    // more fields
]
```
- Run the `fill_fillable_fields.py` script from this file's directory to create a filled-in PDF:
`python scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>`
This script will verify that the field IDs and values you provide are valid; if it prints error messages, correct the appropriate fields and try again.

# Non-fillable fields
If the PDF doesn't have fillable form fields, you'll need to visually determine where the data should be added and create text annotations. Follow the bellow steps **exactly**. 
You MUST perform all of these steps to ensure that the form is accurately completed. Details for each step are below.
- Convert the PDF to PNG images and determine field bounding boxes.
- Create a JSON file with field information and validation images showing the bounding boxes.
- Validate the bounding boxes.
- Use the bounding boxes to fill in the form.

## Step 1: Visual Analysis (REQUIRED)
- Convert the PDF to PNG images. Run this script from this file's directory.
`python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
The script will create a PNG image for each page in the PDF.
- Carefully examine each PNG image and identify all form fields and areas where the user should enter data. For each form field where the user should enter text, determine bounding boxes for both the form field label, and the area where the user should enter text. The label and entry bounding boxes MUST NOT INTERSECT; the text entry box should only include the area where data data should be entered. Usually this area will be immediately to the side, above, or below its label. Entry bounding boxes must be tall and wide enough to contain their text.

These are some examples of form structures that you might see:

*Label inside box*
```
┌────────────────────────┐
│ Name:                  │
└────────────────────────┘
```
The input area should be to the right of the "Name" label and extend to the edge of the box.

*Label before line*
```
Email: _______________________
```
The input area should be above the line and include its entire width.

*Label under line*
```
_______________________
Name
```
The input area should be above the line and include the entire width of the line. This is common for signature and date fields.

*Label above line*
```
Please enter any special requests:
______________________________________________
```
The input area should extend from the bottom of the label to the line, and should include the entire width of the line.

*Checkboxes*
```
Are you a US citizen? Yes □  No □
```
For checkboxes:
- Look for small square boxes (□) - these are the actual checkboxes to target. They may be to the left or right of their labels.
- Distinguish between label text ("Yes", "No") and the clickable checkbox squares.
- The entry bounding box should cover ONLY the small square, not the text label.
import unittest
import json
import io
from check_bounding_boxes import get_bounding_box_messages

# Currently this is not run automatically in CI; it's just for documentation and manual checking.
class TestGetBoundingBoxMessages(unittest.TestCase):

    def create_json_stream(self, data):
        """Helper to create a JSON stream from data"""
        return io.StringIO(json.dumps(data))
    
    def test_no_intersections(self):
        """Test case with no bounding box intersections"""
        data = {
            "form_fields": [
                {
                    "description": "Name",
                    "page_number": 1,
                    "label_bounding_box": [10, 10, 50, 30],
                    "entry_bounding_box": [60, 10, 150, 30],
                },
                {
                    "description": "Email",
                    "page_number": 1,
                    "label_bounding_box": [10, 40, 50, 60],
                    "entry_bounding_box": [60, 40, 150, 60],
                }
            ]
        }

        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("SUCCESS" in msg for msg in messages))
        self.assertFalse(any("FAILURE" in msg for msg in messages))

    def test_label_entry_intersection_same_field(self):
        """Test intersection between bounding boxes of different fields"""
        data = {
            "form_fields": [
                {
                    "description": "Name",
                    "page_number": 1,
                    "label_bounding_box": [10, 10, 60, 30],
                    "entry_bounding_box": [50, 10, 150, 30] # Overlaps with label
                }
            ]
        }

        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("FAILURE" in msg and "intersection" in msg for msg in messages))
        self.assertFalse(any("SUCCESS" in msg for msg in messages))

    def test_intersection_between_different_fields(self):
        """Test intersection between bounding boxes of different fields"""
        data = {
            "form_fields": [
                {
                    "description": "Name",
                    "page_number": 1,
                    "label_bounding_box": [10, 10, 50, 30],
                    "entry_bounding_box": [60, 10, 150, 30]
                },
                {
                    "description": "Email",
                    "page_number": 1,
                    "label_bounding_box": [40, 20, 80, 40], # Overlaps with Name's boxes
                    "entry_bounding_box": [160, 10, 250, 30]
                }
            ]
        }

        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("FAILURE" in msg and "intersection" in msg for msg in messages))
        self.assertFalse(any("SUCCESS" in msg for msg in messages))
    
    def test_different_pages_no_intersection(self):
        """Test that boxes on different pages don't count as intersecting"""
        data = {
            "form_fields": [
                {
                    "description": "Name",
                    "page_number": 1,
                    "label_bounding_box": [10, 10, 50, 30],
                    "entry_bounding_box": [60, 10, 150, 30]
                },
                {
                    "description": "Email",
                    "page_number": 2,
                    "label_bounding_box": [10, 10, 50, 30],
                    "entry_bounding_box": [60, 10, 150, 30]
                }
            ]
        }

        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("SUCCESS" in msg for msg in messages))
        self.assertFalse(any("FAILURE" in msg for msg in messages))

    def test_entry_height_too_small(self):
        """Test that entry box height is checked against font size"""
        data = {
            "form_fields": [
                {
                    "description": "Name",
                    "page_number": 1, 
                    "label_bounding_box": [10, 10, 20, 50, 30],
                    "entry_bounding_box": [60, 10, 150, 20],
                    "entry_text": {
                        "font_size": 14
                    }
                }
            ]
        }

        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("FAILURE" in msg for msg in messages))
        self.assertFalse(any("SUCCESS" in msg for msg in messages))

    def test_default_font_size(self):
        """Test that default font size is used when not specified"""
        data = {
            "form_fields": [
                {
                    "description": "Name",
                    "page_number": 1,
                    "label_bounding_box": [10, 10, 50, 30],
                    "entry_text": {
                        "font_size": 14
                    }
                }
            ]
        }

        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("SUCCESS" in msg for msg in messages))
        self.assertFalse(any("FAILURE" in msg for msg in messages))

    
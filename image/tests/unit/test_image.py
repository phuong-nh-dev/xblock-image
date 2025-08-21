"""
Unit tests for ImageBlock
"""
import unittest
from unittest.mock import Mock, patch

from xblock.field_data import DictFieldData
from xblock.fields import ScopeIds

from image.image import ImageBlock


class TestImageBlock(unittest.TestCase):
    """Test ImageBlock functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.runtime = Mock()
        self.runtime.service.return_value = Mock()
        self.scope_ids = ScopeIds('user_id', 'block_type', 'def_id', 'usage_id')
        
    def make_one(self, **field_data):
        """Create an ImageBlock for testing"""
        field_data_dict = DictFieldData(field_data)
        block = ImageBlock(self.runtime, field_data_dict, self.scope_ids)
        return block
        
    def test_init(self):
        """Test XBlock initialization"""
        block = self.make_one()
        self.assertEqual(block.display_name, "Image Display")
        self.assertEqual(block.image_url, "https://via.placeholder.com/800x400/0066cc/ffffff?text=Sample+Image")
        self.assertEqual(block.image_alt, "")

    def test_init_with_custom_values(self):
        """Test XBlock initialization with custom values"""
        block = self.make_one(
            display_name="Custom Image",
            image_url="https://example.com/custom.jpg",
            image_alt="Custom alt text"
        )
        self.assertEqual(block.display_name, "Custom Image")
        self.assertEqual(block.image_url, "https://example.com/custom.jpg")
        self.assertEqual(block.image_alt, "Custom alt text")

    def test_field_updates(self):
        """Test that fields can be updated"""
        block = self.make_one()
        
        # Update fields directly
        block.display_name = "Updated Image"
        block.image_url = "https://example.com/updated.jpg"
        block.image_alt = "Updated alt text"
        
        self.assertEqual(block.display_name, "Updated Image")
        self.assertEqual(block.image_url, "https://example.com/updated.jpg")
        self.assertEqual(block.image_alt, "Updated alt text")

    @patch('image.image.RESOURCE_LOADER')
    def test_student_view(self, mock_loader):
        """Test student view rendering"""
        block = self.make_one()
        mock_loader.render_django_template.return_value = '<div>Test HTML</div>'
        mock_loader.load_unicode.return_value = 'test-content'
        
        with patch('image.image.Fragment') as mock_fragment_class:
            mock_fragment = Mock()
            mock_fragment_class.return_value = mock_fragment
            
            result = block.student_view({})
            
            self.assertEqual(result, mock_fragment)
            mock_fragment.add_content.assert_called_once()
            mock_fragment.add_css.assert_called_once()
            mock_fragment.add_javascript.assert_called_once()
            mock_fragment.initialize_js.assert_called_with('ImageBlock')

    @patch('image.image.RESOURCE_LOADER')
    def test_studio_view(self, mock_loader):
        """Test studio view rendering"""
        block = self.make_one()
        mock_loader.render_django_template.return_value = '<div>Edit HTML</div>'
        mock_loader.load_unicode.return_value = 'test-content'
        
        with patch('image.image.Fragment') as mock_fragment_class:
            mock_fragment = Mock()
            mock_fragment_class.return_value = mock_fragment
            
            result = block.studio_view({})
            
            self.assertEqual(result, mock_fragment)
            mock_fragment.add_content.assert_called_once()
            mock_fragment.add_css.assert_called_once()
            mock_fragment.add_javascript.assert_called_once()
            mock_fragment.initialize_js.assert_called_with('ImageEditBlock')

    def test_workbench_scenarios(self):
        """Test workbench scenarios"""
        scenarios = ImageBlock.workbench_scenarios()
        self.assertEqual(len(scenarios), 1)
        self.assertEqual(scenarios[0][0], "Image scenario")
        self.assertIn("custom_image", scenarios[0][1])

    def test_template_context(self):
        """Test that the block provides the right context to templates"""
        block = self.make_one(
            display_name="Test Image",
            image_url="https://example.com/test.jpg",
            image_alt="Test alt text"
        )
        
        # The context should include the block itself
        with patch('image.image.RESOURCE_LOADER') as mock_loader:
            mock_loader.render_django_template.return_value = '<div>Test</div>'
            mock_loader.load_unicode.return_value = 'test-content'
            
            with patch('image.image.Fragment'):
                block.student_view({})
                
                # Check that render_django_template was called with the right context
                call_args = mock_loader.render_django_template.call_args
                context = call_args[1]['context']
                self.assertIn('self', context)
                self.assertEqual(context['self'], block)

    def test_default_alt_text_behavior(self):
        """Test that alt text defaults work correctly"""
        # Test with empty alt text
        block = self.make_one(
            display_name="Test Image",
            image_url="https://example.com/test.jpg",
            image_alt=""
        )
        
        self.assertEqual(block.image_alt, "")
        
        # Test with explicit alt text
        block2 = self.make_one(
            display_name="Test Image",
            image_url="https://example.com/test.jpg",
            image_alt="Explicit alt text"
        )
        
        self.assertEqual(block2.image_alt, "Explicit alt text")


if __name__ == '__main__':
    unittest.main()
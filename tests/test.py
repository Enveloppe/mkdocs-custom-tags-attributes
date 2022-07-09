import unittest
import markdown
from custom_attributes.plugin import read_custom, convert_hashtags, convert_text_attributes


class MyTestCase(unittest.TestCase):
    config = {
        'file': 'custom-attributes.css',
        'docs_dir': ''
    }
    maxDiff = None

    def attr_list(self, text):
        text = convert_hashtags(self.config, text)
        return markdown.markdown(text, extensions=['attr_list', 'nl2br'])

    def test_tags(self):
        """check [test/custom-attributes] with config."""
        css = read_custom(self.config)
        self.assertEqual(css, ['#left', '#blue'])

    def test_convert_line_with_attributes(self):
        """Test a simple line with **attributes**

        :arg text to left#left
        :return **text to left**{: #left}
        """
        line = 'text to left#left'
        markup_line = self.attr_list(line)
        markup_wait = '<p><strong id="left">text to left</strong></p>'

        self.assertEqual(markup_line, markup_wait)

    def test_convert_with_hashtags(self):
        """Test a simple hashtags.

        :arg #FFXIV
        :return: **FFXIV**{: #FFXIV .hash}
        """
        line = '#FFXIV'
        marked = self.attr_list(line)
        expected = '<p><strong class="hash" id="FFXIV">FFXIV</strong></p>'
        self.assertEqual(marked, expected)

    def test_double_hashtags(self):
        """Test a simple line with multiple hashtags.

        :arg #FFXIV #other
        :return: **FFXIV**{: #FFXIV .hash} **other**{: #other .hash}
        """
        line = '#FFXIV #other'
        markup_expected = '<p><strong class="hash" id="FFXIV">FFXIV</strong> <strong class="hash" id="other">other</strong></p>'
        markup_tested = self.attr_list(line)
        self.assertEqual(markup_expected,
                         markup_tested)

    def test_double_attributes(self):
        """Tests a multiple but same attributes.

        :arg text1#left text2#left
        :return: **text1 text2**{: #left}
        """
        line = 'text1#left text2#left'
        markup_expected = '<p><strong id="left">text1 text2</strong></p>'
        markup_tested = self.attr_list(line)
        self.assertEqual(markup_tested, markup_expected)

    def test_multiple_attributes(self):
        """Test a text with two differents attributes. Note that attributes
        lists can be applicated on entire paragraph or simple text.

        :arg Lorem ipsum dolor#blue sit amet, consectetur adipiscing elit#left
        :return: **Lorem ipsum **dolor**{: #blue} sit amet, consectetur adipiscing elit**{: #left}
        """
        line = 'Lorem ipsum dolor#blue sit amet, consectetur adipiscing elit#left'
        expected_markup = '<p><strong>Lorem ipsum </strong>dolor<strong id="left">{: #blue} sit amet, consectetur adipiscing elit</strong></p>'
        tested_markup = self.attr_list(line)
        self.assertEqual(tested_markup, expected_markup)

    def test_attributes_plus_tags(self):
        """Test an attributes coupled with a tag.

        :arg to left#left #FFXIV
        :return: to **left**{: #left} **FFXIV**{: #FFXIV .hash}
        """
        line = 'to left#left #FFXIV'
        expected_markup = '<p>to <strong id="left">left</strong> <strong class="hash" id="FFXIV">FFXIV</strong></p>'
        tested_markup = self.attr_list(line)
        self.assertEqual(expected_markup, tested_markup)

    def test_long_line_tagged(self):
        """Test a simple line with tags + attributes. Note the space and no
        word before the last tags.

        :arg lorem ipsum with #FFXIV and #left
        :return: lorem ipsum with **FFXIV**{: #FFXIV .hash} and \n{: #left}
        """
        line = 'lorem ipsum with #FFXIV and #left'
        expected_markup = '<p id="left">lorem ipsum with <strong class="hash" id="FFXIV">FFXIV</strong> and <br /></p>'
        tested_markup = self.attr_list(line)
        self.assertEqual(expected_markup, tested_markup)

    def test_entire_text(self):
        """Test a lorem ipsum with tags and attributes."""
        text = '#Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\nLorem ipsum dolor sit amet, #consectetur adipiscing elit. Morbi sollicitudin elementum vulputate. Etiam risus massa, fringilla in vestibulum id, consequat vitae metus. Sed nulla dui, finibus dapibus suscipit #nec, cursus rutrum ante. In hac habitasse platea dictumst. Duis accumsan cursus arcu eget congue. #Vestibulum ante ipsum primis in faucibus orci.#left'
        expected_markup = '<p><strong class="hash" id="Lorem">Lorem</strong> ipsum dolor sit amet, consectetur adipiscing elit.</p>\n<p><strong>Lorem ipsum dolor sit amet, </strong>consectetur<strong>{: #consectetur .hash} adipiscing elit. Morbi sollicitudin elementum vulputate. Etiam risus massa, fringilla in vestibulum id, consequat vitae metus. Sed nulla dui, finibus dapibus suscipit </strong>nec<strong>{: #nec .hash}, cursus rutrum ante. In hac habitasse platea dictumst. Duis accumsan cursus arcu eget congue. </strong>Vestibulum<strong id="left">{: #Vestibulum .hash} ante ipsum primis in faucibus orci.</strong></p>'
        tested_markup = markdown.markdown(convert_text_attributes(
            text, self.config).strip(), extensions=['attr_list', 'nl2br'])
        self.assertEqual(expected_markup.strip(), tested_markup.strip())

import unittest
import markdown
import os
from pathlib import Path
from custom_attributes.plugin import (
    read_custom,
    convert_hashtags,
    convert_text_attributes,
)


class MyTestCase(unittest.TestCase):
    config = {
        "file": "custom-attributes.css",
        "docs_dir": str(Path(os.getcwd(), "tests")),
    }
    maxDiff = None

    def attr_list(self, text):
        text = convert_hashtags(self.config, text)
        return markdown.markdown(text, extensions=["attr_list", "nl2br"])

    def test_tags(self):
        """check [test/custom-attributes] with config."""
        css = read_custom(self.config)
        self.assertEqual(css, ["#left", "#yellow", "#right", "#blue"])

    def test_convert_line_with_attributes(self):
        """Test a simple line with **attributes**

        :arg text to left#left
        :return text to left\n{: #left}
        """
        line = "text to left#left"
        markup_line = self.attr_list(line)
        markup_wait = '<p id="left">text to left<br /></p>'

        self.assertEqual(markup_line, markup_wait)

    def test_convert_with_hashtags(self):
        """Test a simple hashtags.

        :arg #FFXIV
        :return: **FFXIV**{: #FFXIV .hash}
        """
        line = "#FFXIV"
        marked = self.attr_list(line)
        expected = '<p><strong class="hash" id="FFXIV">FFXIV</strong></p>'
        self.assertEqual(marked, expected)

    def test_double_hashtags(self):
        """Test a simple line with multiple hashtags.

        :arg #FFXIV #other
        :return: **FFXIV**{: #FFXIV .hash} **other**{: #other .hash}
        """
        line = "#FFXIV #other"
        markup_expected = '<p><strong class="hash" id="FFXIV">FFXIV</strong> <strong class="hash" id="other">other</strong></p>'
        markup_tested = self.attr_list(line)
        self.assertEqual(markup_expected, markup_tested)

    def test_double_attributes(self):
        """Tests a multiple but same attributes.

        :arg text1#left text2#left
        :return: text1 text2\n{#left}
        """
        line = "text1#left text2#left"
        markup_expected = '<p id="left">text1 text2<br /></p>'
        markup_tested = self.attr_list(line)
        self.assertEqual(markup_tested, markup_expected)

    def test_multiple_attributes(self):
        """Test a text with two differents attributes. Note that attributes
        lists can be applicated on entire paragraph or simple text.

        :arg Lorem ipsum dolor#blue sit amet, consectetur adipiscing elit#left
        :return: Lorem ipsum **dolor**{: #blue} sit amet, consectetur adipiscing elit\n{: #left}'
        """
        line = "Lorem ipsum dolor#blue sit amet, consectetur adipiscing elit#left"
        expected_markup = '<p id="left">Lorem ipsum <strong id="blue">dolor</strong> sit amet, consectetur adipiscing elit<br /></p>'
        tested_markup = self.attr_list(line)
        self.assertEqual(tested_markup, expected_markup)

    def test_attributes_plus_tags(self):
        """Test an attributes coupled with a tag.

        :arg to left#left #FFXIV
        :return: to **left**{: #left} **FFXIV**{: #FFXIV .hash}
        """
        line = "to left#left #FFXIV"
        expected_markup = '<p>to <strong id="left">left</strong> <strong class="hash" id="FFXIV">FFXIV</strong></p>'
        tested_markup = self.attr_list(line)
        self.assertEqual(expected_markup, tested_markup)

    def test_long_line_tagged(self):
        """Test a simple line with tags + attributes. Note the space and no
        word before the last tags.

        :arg lorem ipsum with #FFXIV and #left
        :return: lorem ipsum with **FFXIV**{: #FFXIV .hash} and \n{: #left}
        """
        line = "lorem ipsum with #FFXIV and #left"
        expected_markup = '<p id="left">lorem ipsum with <strong class="hash" id="FFXIV">FFXIV</strong> and <br /></p>'
        tested_markup = self.attr_list(line)
        self.assertEqual(expected_markup, tested_markup)

    def test_entire_text(self):
        """Test a lorem ipsum with tags and attributes."""
        text = "#Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\nLorem ipsum dolor sit amet, #consectetur adipiscing elit. Morbi sollicitudin elementum vulputate. Etiam risus massa, fringilla in vestibulum id, consequat vitae metus. Sed nulla dui, finibus dapibus suscipit #nec, cursus rutrum ante. In hac habitasse platea dictumst. Duis accumsan cursus arcu eget congue. #Vestibulum ante ipsum primis in faucibus orci.#left"
        expected_markup = '<p><strong class="hash" id="Lorem">Lorem</strong> ipsum dolor sit amet, consectetur adipiscing elit.</p>\n<p id="left">Lorem ipsum dolor sit amet, <strong class="hash" id="consectetur">consectetur</strong> adipiscing elit. Morbi sollicitudin elementum vulputate. Etiam risus massa, fringilla in vestibulum id, consequat vitae metus. Sed nulla dui, finibus dapibus suscipit <strong class="hash" id="nec">nec</strong>, cursus rutrum ante. In hac habitasse platea dictumst. Duis accumsan cursus arcu eget congue. <strong class="hash" id="Vestibulum">Vestibulum</strong> ante ipsum primis in faucibus orci.<br /></p>'
        tested_markup = markdown.markdown(
            convert_text_attributes(text, self.config).strip(),
            extensions=["attr_list", "nl2br"],
        )
        self.assertEqual(expected_markup.strip(), tested_markup.strip())

    def test_code_blocks(self):
        """Test a code block with attributes."""
        text = """
            ```yaml
            links:
                mdlinks: boolean #convert to markdownlinks
                convert: boolean #transform to simple string with keeping alt text or file name/ title (it removes the [[]] or []())
            ```
        """
        expected_markup = text
        tested_markup = convert_text_attributes(text, self.config).strip()
        self.assertEqual(expected_markup.strip(), tested_markup.strip())

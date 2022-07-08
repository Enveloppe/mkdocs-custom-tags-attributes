import unittest
from custom_attributes.plugin import read_custom, convert_hashtags, convert_text_attributes


class MyTestCase(unittest.TestCase):
    config = {
        'file': 'custom-attributes.css',
        'docs_dir': ''
    }
    maxDiff = None

    def test_tags(self):
        """check [test/custom-attributes] with config."""
        css = read_custom(self.config)
        self.assertEqual(css, ['#left', "#blue"])

    def test_convert_line_with_attributes(self):
        """
        Test a simple line with **attributes**
        :arg text to left#left
        :return **text to left**{: #left}
        """
        line = 'text to left#left'
        self.assertEqual(convert_hashtags(self.config, line), '**text to left**{: #left}')

    def test_convert_with_hashtags(self):
        """
        Test a simple hashtags.
        :arg #FFXIV
        :return: **FFXIV**{: #FFXIV .hash}
        """
        line = '#FFXIV'
        self.assertEqual(convert_hashtags(
            self.config, line), '**FFXIV**{: #FFXIV .hash}')

    def test_double_hashtags(self):
        """
        Test a simple line with multiple hashtags
        :arg #FFXIV #other
        :return: **FFXIV**{: #FFXIV .hash} **other**{: #other .hash}
        """
        line = '#FFXIV #other'
        self.assertEqual(convert_hashtags(self.config, line),
                         '**FFXIV**{: #FFXIV .hash} **other**{: #other .hash}')

    def test_double_attributes(self):
        """
        Tests a multiple but same attributes.
        :arg text1#left text2#left
        :return: **text1 text2**{: #left}
        """
        line = 'text1#left text2#left'
        self.assertEqual(convert_hashtags(
            self.config, line), '**text1 text2**{: #left}')

    def test_multiple_attributes(self):
        """
        Test a text with two differents attributes. Note that attributes lists can be applicated on entire paragraph or simple text.
        :arg Lorem ipsum dolor#blue sit amet, consectetur adipiscing elit#left
        :return:
        """
    def test_attributes_plus_tags(self):
        """
        Test an attributes coupled with a tag
        :arg to left#left #FFXIV
        :return: **to left **FFXIV**{: #FFXIV .hash}**{: #left}
        """
        line = 'to left#left #FFXIV'
        self.assertEqual(convert_hashtags(
            self.config, line), '**to left **FFXIV**{: #FFXIV .hash}**{: #left}')

    def test_long_line_tagged(self):
        """
        Test a simple line with tags + attributes
        :arg lorem ipsum with #FFXIV and #left
        :return: **lorem ipsum with **FFXIV**{: #FFXIV .hash} and**{: #left}
        """
        line = 'lorem ipsum with #FFXIV and #left'
        self.assertEqual(convert_hashtags(self.config, line),
                         '**lorem ipsum with **FFXIV**{: #FFXIV .hash} and**{: #left}')

    def test_entire_text(self):
        """
        Test a lorem ipsum with tags and attributes
        """
        text = "#Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse in urna tincidunt arcu maximus dapibus. Cras lobortis ipsum eu vestibulum consectetur. Donec vel sapien egestas libero rhoncus euismod. Vivamus mauris diam, aliquet placerat nisi in, lacinia iaculis nibh. Duis eget tincidunt diam. Morbi pulvinar blandit mauris, eu pharetra nibh vehicula ac. Duis vehicula pulvinar mauris, quis dictum leo auctor et. Curabitur est dolor, laoreet vestibulum turpis eu, efficitur mollis neque. Nulla faucibus, nunc in porttitor sodales, augue metus tempor nulla, sit amet consectetur risus ante id lorem. Donec id vehicula magna, sed congue arcu. Fusce elementum imperdiet augue, non vehicula justo pellentesque id.\nLorem ipsum dolor sit amet, #consectetur adipiscing elit. Morbi sollicitudin elementum vulputate. Etiam risus massa, fringilla in vestibulum id, consequat vitae metus. Sed nulla dui, finibus dapibus suscipit #nec, cursus rutrum ante. In hac habitasse platea dictumst. Duis accumsan cursus arcu eget congue. #Vestibulum ante ipsum primis in faucibus orci.#left"
        converted_manually = "**Lorem**{: #Lorem .hash} ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse in urna tincidunt arcu maximus dapibus. Cras lobortis ipsum eu vestibulum consectetur. Donec vel sapien egestas libero rhoncus euismod. Vivamus mauris diam, aliquet placerat nisi in, lacinia iaculis nibh. Duis eget tincidunt diam. Morbi pulvinar blandit mauris, eu pharetra nibh vehicula ac. Duis vehicula pulvinar mauris, quis dictum leo auctor et. Curabitur est dolor, laoreet vestibulum turpis eu, efficitur mollis neque. Nulla faucibus, nunc in porttitor sodales, augue metus tempor nulla, sit amet consectetur risus ante id lorem. Donec id vehicula magna, sed congue arcu. Fusce elementum imperdiet augue, non vehicula justo pellentesque id.\n**Lorem ipsum dolor sit amet, **consectetur**{: #consectetur .hash} adipiscing elit. Morbi sollicitudin elementum vulputate. Etiam risus massa, fringilla in vestibulum id, consequat vitae metus. Sed nulla dui, finibus dapibus suscipit **nec**{: #nec .hash}, cursus rutrum ante. In hac habitasse platea dictumst. Duis accumsan cursus arcu eget congue. **Vestibulum**{: #Vestibulum .hash} ante ipsum primis in faucibus orci.**{: #left}"
        test_text = convert_text_attributes(text, self.config).strip()
        self.assertEqual(test_text, converted_manually)

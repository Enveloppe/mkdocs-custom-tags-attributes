import unittest
from mkdocs.config import config_options
from custom_attributes.plugin import read_custom, convert_hashtags, convert_text_attributes


class MyTestCase(unittest.TestCase):
    config = {
        'file': 'custom-attributes.css',
        'docs_dir': 'tests'
    }
    custom_configuration = 'custom-attributes.css'

    def test_tags(self):
        print(self.config['file'])
        css = read_custom(self.config, 'custom-attributes.css')
        self.assertEqual(css, ['#left'])

    def test_convert_line_with_attributes(self):
        line = 'text to left#left'
        self.assertEqual(convert_hashtags(self.config, line,
                         self.custom_configuration), '**text to left**{: #left}')

    def test_convert_with_hashtags(self):
        line = '#FFXIV'
        self.assertEqual(convert_hashtags(
            self.config, line, self.custom_configuration), '**FFXIV**{: #FFXIV .hash}')

    def test_double_hashtags(self):
        line = '#FFXIV #other'
        self.assertEqual(convert_hashtags(self.config, line, self.custom_configuration),
                         '**FFXIV**{: #FFXIV .hash} **other**{: #other .hash}')

    def test_double_attributes(self):
        line = 'text1#left text2#left'
        self.assertEqual(convert_hashtags(
            self.config, line, self.custom_configuration), '**text1 text2**{: #left}')

    def test_attributes_plus_tags(self):
        line = 'to left#left #FFXIV'
        self.assertEqual(convert_hashtags(
            self.config, line, self.custom_configuration), '**to left **FFXIV**{: #FFXIV .hash}**{: #left}')

    def test_long_line_tagged(self):
        line = 'lorem ipsum with #FFXIV and #left'
        self.assertEqual(convert_hashtags(self.config, line, self.custom_configuration),
                         '**lorem ipsum with **FFXIV**{: #FFXIV .hash} and**{: #left}')

    def test_entire_text(self):
        text = '''#Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse in urna tincidunt arcu maximus dapibus. Cras lobortis ipsum eu vestibulum consectetur. Donec vel sapien egestas libero rhoncus euismod. Vivamus mauris diam, aliquet placerat nisi in, lacinia iaculis nibh. Duis eget tincidunt diam. Morbi pulvinar blandit mauris, eu pharetra nibh vehicula ac. Duis vehicula pulvinar mauris, quis dictum leo auctor et. Curabitur est dolor, laoreet vestibulum turpis eu, efficitur mollis neque. Nulla faucibus, nunc in porttitor sodales, augue metus tempor nulla, sit amet consectetur risus ante id lorem. Donec id vehicula magna, sed congue arcu. Fusce elementum imperdiet augue, non vehicula justo pellentesque id.
        
        Lorem ipsum dolor sit amet, #consectetur adipiscing elit. Morbi sollicitudin elementum vulputate. Etiam risus massa, fringilla in vestibulum id, consequat vitae metus. Sed nulla dui, finibus dapibus suscipit #nec, cursus rutrum ante. In hac habitasse platea dictumst. Duis accumsan cursus arcu eget congue. #Vestibulum ante ipsum primis in faucibus orci.#left
        '''
        converted_manually = '''
        '''
        test_text = convert_text_attributes(text, self.config)
        self.assertEqual(test_text, converted_manually)

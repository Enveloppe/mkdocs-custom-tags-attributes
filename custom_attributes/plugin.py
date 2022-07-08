import re
from pathlib import Path

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


def read_custom(config: Config, custom: str) -> list:
    """Read the css file and take each selector and return it as a list."""
    css_file = Path(config.get('docs_dir'), custom)
    css = []
    with open(css_file, 'r', encoding='utf-8') as custom_attr:
        for i in custom_attr.readlines():
            if i.startswith('#'):
                css.append(i.replace('{\n', '').strip())
    return css


def convert_hashtags(config: Config, line: str, custom_configuration: str) -> str:
    """Convert the tags attributes to the list attributes when reading a
    line."""
    css = read_custom(config, custom_configuration)
    token = re.findall(r'#\w+', line)
    token = list(set(token))
    for i, value in enumerate(token):
        tags = token[i]
        if tags in css:
            original_line = line
            line = line.replace(tags, '')
            if len(line.strip()) == 0:
                return original_line
            if line.startswith('#'):
                heading = re.findall('#', line)
                heading = ''.join(heading)
                ial = (
                    heading + ' **' + line.replace('#', '').strip()
                    + '**{: ' + tags + '}'
                )
            else:
                ial = '**' + line.strip() + '**{: ' + tags + '}'
            line = line.replace(line, ial)
        else:
            ial = (
                '**'
                + tags.replace('#', ' ').strip()
                + '**{: '
                + tags.strip()
                + ' .hash}'
            )
            line = line.replace(token[i], ial, 1)
    return line


def convert_text_attributes(markdown: str, config: Config) -> str:
    """Read an entire text to convert the tags attributes to the list
    attributes."""
    files_contents = markdown.split('\n')
    custom_config = config['file']
    markdown = ''
    code_blocks = False
    for line in files_contents:
        if code_blocks and line.startswith('```'):
            code_blocks = False
        elif line.startswith('```'):
            code_blocks = True
        elif re.search(r'#\w+', line) and not re.search(
                r'(`|\[{2}|\()(.*)#(.*)(`|\]{2}|\))', line
        ) and not code_blocks:
            line = convert_hashtags(config, line, custom_config)
        markdown += line + '\n'
    return markdown


class TagsAttributePlugins(BasePlugin):
    """Reads the files and convert #tags to **tags**{: #tags .hash} Convert to
    id if found in configuration files."""
    config_scheme = (
        ('file', config_options.Type(str, default='assets/css/custom_attributes.css')),
    )

    def on_page_markdown(self, markdown: str, page: Page, config: Config, files: Files) -> str:
        """Run the conversion based on the page_markdown event."""
        return convert_text_attributes(markdown, config)

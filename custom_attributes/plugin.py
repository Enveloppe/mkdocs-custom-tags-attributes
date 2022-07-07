from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
import re
from pathlib import Path


def read_custom(config: dict, custom: str):
    css_file = Path(config.get('docs_dir'), custom)
    css = []
    with open(css_file, 'r', encoding='utf-8') as custom_attr:
        for i in custom_attr.readlines():
            if i.startswith('#'):
                css.append(i.replace('{\n', '').strip())
    return css


def convert_hashtags(config: dict, line: str, custom_configuration:str) -> str:
    css = read_custom(config, custom_configuration)
    token = re.findall(r'#\S+', line)
    token = list(set(token))
    for i in range(0, len(token)):
        tags = token[i]
        if tags in css:
            original_line = line
            line = line.replace(tags, '')
            if len(line.strip()) == 0:
                return original_line
            if line.startswith('#'):
                heading = re.findall('#', line)
                heading = "".join(heading)
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


class CalloutsPlugin(BasePlugin):
    """
    Reads the files and convert #tags to **tags**{: #tags .hash}
    Convert to id if found in configuration files
    """
    config_scheme = (
        ('file', config_options.Type(str, default='assets/css/custom_attributes.css')),
    )

    def on_page_markdown(self, markdown, page, config, files):
        files_contents = markdown.split('\n')
        custom_config = self.config['file']
        markdown = ''
        code_blocks=False
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

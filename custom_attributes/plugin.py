import re
from pathlib import Path

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

def read_custom(config: Config) -> list:
    """Read the css file and take each css ID selector and return it as a list."""
    css_file = Path(config.get('docs_dir'), config.get('file'))
    css = []
    try:
        with open(css_file, 'r', encoding='utf-8') as custom_attr:
            for i in custom_attr.readlines():
                if i.startswith('#'):
                    css.append(i.replace('{\n', '').strip())
    except FileNotFoundError :
        print('No CSS configured.')
        return []
    return css


def convert_hashtags(config: Config, line: str) -> str:
    """Convert the tags attributes to the list attributes when reading a
    line."""
    css = read_custom(config)
    token = re.findall(r'#\w+', line)
    token = list(set(token))
    for i, tags in enumerate(token):
        if tags in css:
            clean_line = line.replace(tags, '')

            if len(clean_line.strip()) == 0:
                return line
            markup = "**{: " + tags +'}'
            word_regex=r"\w+"+re.escape(tags)

            if line.startswith('#'):
                heading = re.search('^#*', line).group()
                without_heading = re.sub('^#*', '', line).strip()
                word_before_tags = re.search(word_regex, without_heading).group().strip() if re.search(word_regex,
                                                                                                       without_heading) else ""

                replaced_tags = "**" + word_before_tags.replace(tags, markup)
                ial = heading + " " + re.sub(word_regex, replaced_tags, without_heading)
            else:
                word_before_tags = re.search(word_regex, line).group().strip() if re.search(word_regex, line) else ""
                replaced_tags = "**" + word_before_tags.replace(tags, markup)
                ial = re.sub(word_regex, replaced_tags, line)

            if line.strip().rstrip().lstrip().replace('\n', '').endswith(tags):
                markup = markup.replace('**', '')
                word_regex = r"\S+"+re.escape(tags)
                if line.startswith('#'):
                    ial = clean_line + ' ' + markup
                else:
                    word_before_tags = re.search(word_regex, line).group().strip() if re.search(word_regex,
                                                                                                line) else ""
                    if word_before_tags == '':
                        ial = clean_line + '\n' + markup
                    else:
                        ial = "**" + clean_line + '**' + markup

            line = ial
        else:
            ial = (
                '**'
                + tags.replace('#', ' ').strip()
                + '**{: '
                + tags.strip()
                + ' .hash}'
            )
            line = line.replace(tags, ial, 1)
    return line


def convert_text_attributes(markdown: str, config: Config) -> str:
    """Read an entire text to convert the tags attributes to the list
    attributes."""
    files_contents = markdown.split('\n')
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
            line = convert_hashtags(config, line)
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

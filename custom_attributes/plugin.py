"""Main script that convert the #hashtags of a markdown text during the
on_page_markdown event."""

import re
from pathlib import Path

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


def read_custom(config: Config) -> list:
    """Read the css file and take each css ID selector and return it as a
    list."""
    css_file = Path(config.get('docs_dir'), config.get('file'))
    css = []
    try:
        with open(css_file, 'r', encoding='utf-8') as custom_attr:
            for i in custom_attr.readlines():
                if i.startswith('#'):
                    css.append(i.replace('{\n', '').strip())
    except FileNotFoundError:
        print('No CSS configured.')
        return []
    return css


def cleanned_word(line: str, tags: str, word_regex: str) -> str:
    word_before_tags = re.search(word_regex, line).group().strip() if re.search(word_regex,
                                                                                line) else ''
    return word_before_tags


def convert_hashtags(config: Config, line: str) -> str:
    """Convert the tags attributes to the list attributes when reading a
    line."""
    css = read_custom(config)
    token = re.findall(r'#\w+', line)
    token = list(set(token))
    for tag in token:
        if tag in css:
            clean_line = line.replace(tag, '')

            if len(clean_line.strip()) == 0:
                return line
            markup = '**{: ' + tag + '}'
            word_regex = r'\w+'+re.escape(tag)

            if line.startswith('#'):
                heading = re.search('^#*', line).group() + ' '
                without_heading = re.sub('^#*', '', line).strip()
                word_before_tags = cleanned_word(
                    without_heading, tag, word_regex)

                replaced_tags = '**' + word_before_tags.replace(tag, markup)
                ial = heading + \
                    re.sub(word_regex, replaced_tags, without_heading)
            else:
                word_before_tags = cleanned_word(line, tag, word_regex)
                replaced_tags = '**' + word_before_tags.replace(tag, markup)
                ial = re.sub(word_regex, replaced_tags, line)

            if line.strip().rstrip().lstrip().replace('\n', '').endswith(tag):
                markup = markup.replace('**', '')
                word_regex = r'\S+'+re.escape(tag)
                if line.startswith('#'):
                    ial = clean_line + ' ' + markup
                else:
                    word_before_tags = cleanned_word(line, tag, word_regex)
                    if word_before_tags == '':
                        ial = clean_line + '\n' + markup
                    else:
                        ial = '**' + clean_line + '**' + markup

            line = ial
        else:
            ial = (
                '**'
                + tag.replace('#', ' ').strip()
                + '**{: '
                + tag.strip()
                + ' .hash}'
            )
            line = line.replace(tag, ial, 1)
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
    id/attributes list if found in configuration files."""
    config_scheme = (
        ('file', config_options.Type(str, default='assets/css/custom_attributes.css')),
    )

    def on_page_markdown(self, markdown: str, page: Page, config: Config, files: Files) -> str:
        """Run the conversion based on the page_markdown event."""
        return convert_text_attributes(markdown, config)

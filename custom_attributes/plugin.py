"""Main script that convert the #hashtags of a Markdown text during the
on_page_markdown event."""

import re
from pathlib import Path

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


def read_custom(config: dict[str, str]) -> list:
    """Read the css file and take each css ID selector and return it as a
    list."""
    css_file = Path(config.get('docs_dir'), config.get('file'))
    try:
        with open(css_file, 'r', encoding='utf-8') as custom_attr:
            custom_css = custom_attr.read()
        custom_css = re.sub(r'\s*', '', custom_css)
        css = re.findall(r'#\S*', custom_css, re.MULTILINE)
    except FileNotFoundError:
        print('No CSS configured.')
        return []
    return css


def cleanned_word(line: str, word_regex: str) -> str:
    """Check the word before the attributes tags"""
    if re.search(word_regex, line):
        word_before_tags = re.search(word_regex, line).group().strip()
    else:
        word_before_tags = ''
    return word_before_tags


def convert_hashtags(config: dict[str, str], line: str) -> str:
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
                    without_heading, word_regex)

                replaced_tags = '**' + word_before_tags.replace(tag, markup)
                ial = heading + \
                    re.sub(word_regex, replaced_tags, without_heading)
            else:
                word_before_tags = cleanned_word(line, word_regex)
                replaced_tags = '**' + word_before_tags.replace(tag, markup)
                ial = re.sub(word_regex, replaced_tags, line)

            if line.strip().rstrip().lstrip().replace('\n', '').endswith(tag):
                markup = markup.replace('**', '')
                word_regex = r'\S+'+re.escape(tag)
                if line.startswith('#'):
                    ial = clean_line + ' ' + markup
                else:
                    word_before_tags = cleanned_word(line, word_regex)
                    if word_before_tags == '' or any(selector in line for selector in token):
                        ial = clean_line + '\n' + markup
                        ial = ial
                    else:
                        ial = '**' + clean_line + '**' + markup
                        ial = ial

            line = ial.strip()
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


def convert_text_attributes(markdown: str, config: dict[str, str]) -> str:
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
            r'(`|\[{2}|\()(.*)#(.*)(`|]{2}|\))', line
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
        config = {
            'docs_dir': config['docs_dir'],
            'file': self.config['file']
            }
        return convert_text_attributes(markdown, config)

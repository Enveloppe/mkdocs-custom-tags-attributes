"""Main script that convert the #hashtags of a Markdown text during the on_page_markdown event."""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


def read_custom(config: Dict[str, str]) -> List[str]:
    """Read the css file and take each css ID selector and return it as a list."""
    css_file = Path(config.get("docs_dir"), config.get("file"))  # type: ignore
    try:
        css_file_path = Path(css_file)
        with css_file_path.open("r", encoding="utf-8") as custom_attr:
            custom_css = custom_attr.read()
        custom_css = re.sub(r"[\t\n]", "", custom_css)
        custom_css = re.sub(r"\{.*?\}", ",", custom_css)
        custom_css = re.sub(r"\/\*.*?\*\/", "", custom_css, flags=re.DOTALL)
        custom_css = custom_css.split(",")
        return [i.strip() for i in custom_css if i.strip().startswith("#")]
    except FileNotFoundError:
        logging.getLogger(__name__)
        logging.warning(
            "The file %s was not found. Please check the path and try again.",
            css_file,
        )
        return []


def cleanned_word(line: str, word_regex: str) -> str:
    """Check the word before the attributes tags"""
    search = re.search(word_regex, line)
    if search:
        word_before_tags = search.group().strip()
    else:
        word_before_tags = ""
    return word_before_tags


def is_excluded(tags: Optional[str], line: str) -> bool:
    if not tags:
        return False
    link_regex = r"\[\[?(.*)" + re.escape(tags) + r"(.*)\]\]?"
    if re.search(link_regex, line):
        return True
    code_regex = r"`(.*)" + re.escape(tags) + r"(.*)`"
    if re.search(code_regex, line):
        return True
    html_regex = r"<(.*)" + re.escape(tags) + r"(.*)>"
    if re.search(html_regex, line):
        return True
    parenthesis_regex = r"\((.*)" + re.escape(tags) + r"(.*)\)"
    if re.search(parenthesis_regex, line):
        return True
    return False


def convert_hashtags(config: Dict[str, str], line: str) -> str:
    """Convert the tags attributes to the list attributes when reading a
    line."""
    css = read_custom(config)
    token = re.findall(r"#[\w\-_\/]+", line)
    token = list(set(token))
    for tag in token:
        if tag in css:
            clean_line = line.replace(tag, "")

            if len(clean_line.strip()) == 0:
                return line
            markup = "**{: " + tag + "}"
            word_regex = r"\w+" + re.escape(tag)
            startswith = re.search("^#*", line)
            if line.startswith("#") and startswith:
                heading = startswith.group() + " "
                without_heading = re.sub("^#*", "", line).strip()
                word_before_tags = cleanned_word(without_heading, word_regex)

                replaced_tags = "**" + word_before_tags.replace(tag, markup)
                ial = heading + re.sub(word_regex, replaced_tags, without_heading)
            else:
                word_before_tags = cleanned_word(line, word_regex)
                replaced_tags = "**" + word_before_tags.replace(tag, markup)
                ial = re.sub(word_regex, replaced_tags, line)

            if line.strip().rstrip().lstrip().replace("\n", "").endswith(tag):
                markup = markup.replace("**", "")
                word_regex = r"\S+" + re.escape(tag)
                if line.startswith("#"):
                    ial = clean_line + " " + markup
                else:
                    word_before_tags = cleanned_word(line, word_regex)
                    if word_before_tags == "" or any(
                        selector in line for selector in token
                    ):
                        ial = clean_line + "\n" + markup
                    else:
                        ial = "**" + clean_line + "**" + markup
            line = ial.strip()
        else:
            ial = (
                "**" + tag.replace("#", " ").strip() + "**{: " + tag.strip() + " .hash}"
            )
            line = line.replace(tag, ial, 1)
    return line


def convert_text_attributes(markdown: str, config: Dict[str, str]) -> str:
    """Read an entire text to convert the tags attributes to the list
    attributes."""
    files_contents = markdown.split("\n")
    markdown = ""
    code_blocks = False
    for line in files_contents:
        tags = re.search(r"#[\w\-_\/]+", line)
        if tags:
            tags = tags.group()
        if not code_blocks and (
            line.startswith("```")
            or (re.search("<.*?>", line) and not re.search("</.*?>", line))
            or re.search(r"^\s*```(.*)", line)
        ):
            code_blocks = True
        elif code_blocks and (
            line.startswith("```")
            or re.search("</?.*?>", line)
            or re.search(r"^\s*```", line)
        ):
            code_blocks = False

        elif (
            re.search(r"#\w+", line) and not is_excluded(tags, line) and not code_blocks
        ):
            line = convert_hashtags(config, line)  # noqa
        markdown += line + "\n"
    return markdown


class TagsAttributePlugins(BasePlugin):
    """Reads the files and convert #tags to **tags**{: #tags .hash} Convert to id/attributes list if found in configuration files."""  # noqa: E501

    config_scheme = (
        ("file", config_options.Type(str, default="assets/css/custom_attributes.css")),
    )

    def on_page_markdown(
        self,  # noqa
        markdown: str,
        page: Page,
        config: Config,
        files: Files,
    ) -> str:
        """Run the conversion based on the page_markdown event."""
        config = {"docs_dir": config["docs_dir"], "file": self.config["file"]}  # type: ignore
        return convert_text_attributes(markdown, config)  # type: ignore

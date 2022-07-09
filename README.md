This plugin attempt to create inline markdown attribute using hashtags (`#`) to mimic [attribute list](https://python-markdown.github.io/extensions/attr_list/) but in better.

This plugin will convert all `"#contents` to `**contents**{: #contents .hash}` to add custom CSS. Moreover, using a custom css file, you can also style text. The plugin will convert `somes text#attribute` to `somes text**{: #attribute}**` using this file as base!

> ↪️ `#2022/01/01` will become `**2022/01/01**{: #2022/01 .hash}`

# Installation

`pip install mkdocs-custom-tags-attributes --upgrade`

First, add the plugin in your `mkdocs.yml`:

```yml
plugins:
  - search
  - custom_attributes
```
Note: If you have no plugin entry in your config file yet, you'll likely also want to add the search plugin. MkDocs enables it by default if there is no plugin entry set, but now you have to enable it explicitly.

You need to create an `custom_attributes.css` if you want to create inline attributes!

# Configuration

You can specify the css file in your `mkdocs.yml`:
```yaml
plugins:
  - search
  - custom_attributes:
      file: assets/css/custom_attributes.css
```

Obviously, you need to update your [extra css](https://www.mkdocs.org/user-guide/configuration/#extra_css) :

```yaml
extra_css:
  - assets/css/custom_attributes.css
```

# Inline attributes

After this, in the css file, you can add inline attribute, automatically parsed by the plugin. Each tags must be an [css id](https://developer.mozilla.org/en-US/docs/Web/CSS/ID_selectors), aka prepend with `#`.

```css
#yourtags {
/* your css */
}
```

> 💭 Don't forget to escape the characters (as `\` or `/` for example!)

Little example : align to right a text. 

```css
#right {
    display: inline-block;
    width: 100%;
    text-align: right;
    font-weight: normal;
}
```

The text : 
```markdown
text to right#right
```
Will become :
```markdown
**text to right**{: #right}\n
```
or in html : 
```html
<p><strong id="right">text to right</strong></p>
```

> 💭 You can note that I choose to use bold to mark the inline attribute. You can remove it with `font-weight: normal;` in the css file when specify your tags.

Also, some inlines attribute can be a bit strange. 
First, any inline attributes placed in the end of the line will be applied on the entire paragraph. 

There is a lot of possible example, so you can check the tests to saw behavior. Please, also refer to the [attribute list documentation](https://python-markdown.github.io/extensions/attr_list/).

| original                                                             | converted attribute                                                                  | html                                                                                                                 |
|----------------------------------------------------------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `text to right#right`                                                | `**text to right**{: #right}`                                                        | `<p><strong id="right">text to right</strong></p>`                                                                   |
| `#FFXIV`                                                             | `**FFXIV**{: #FFXIV .hash}`                                                          | `<p><strong class="hash" id="FFXIV">FFXIV</strong></p>`                                                              |
| `#FFXIV #other`                                                      | `**FFXIV**{: #FFXIV .hash} **other**{: #other .hash}`                                | `<p><strong class="hash" id="FFXIV">FFXIV</strong> <strong class="hash" id="other">other</strong></p>`               |
| `text1#right text2#right`                                            | `**text1 text2**{: #right}`                                                          | `<p><strong id="right">text1 text2</strong></p>`                                                                     |
| `Lorem ipsum dolor#blue sit amet, consectetur adipiscing elit#right` | `**Lorem ipsum **dolor**{: #blue} sit amet, consectetur adipiscing elit**{: #right}` | `<p><strong>Lorem ipsum </strong>dolor<strong id="right">{: #blue} sit amet, consectetur adipiscing elit</strong></p>` |
| `to right#right #FFXIV`                                              | `to **right**{: #right} **FFXIV**{: #FFXIV .hash}`                                   | `<p>to <strong id="right">right</strong> <strong class="hash" id="FFXIV">FFXIV</strong></p>`                         |
| `lorem ipsum with #FFXIV and #right`[^1]                             | `lorem ipsum with **FFXIV**{: #FFXIV .hash} and \n{: #right}\n`                        | `<p id="right">lorem ipsum with <strong class="hash" id="FFXIV">FFXIV</strong> and </p>`                         |

[^1]: Note the absence of word before the last tags. 

> ☣️ Attention! You need at last one word before each attributes to stylize unless the attributes is in the **end** of a paragraph. 
> ☣️ An attribute in the **end** of a paragraph will stylize all the paragraph. 

<u>Error example</u>:
`lorem ipsum with #FFXIV and #blue But not right#right` -> `lorem ipsum with **FFXIV**{: #FFXIV .hash} and #blue But not right\n{: #right}\n`

# Stylize tags

You can also custom your inline tags (hello obsidian user!) using the `.hash` class!
For example:
```css
.hash {
    background-color: honeydew;
    border-radius: 5px;
}
```

# Test & dev :
- The conda environment "Publish" list all requirements for developing the plugins. 
- The package is developed using semantic-release, so please respect that.
- You can use flake8 and pyformat to correct your code.

To test the plugin : 
```python
from custom_attributes.plugin import convert_text_attributes, convert_hashtags
import markdown as mk
config = {
        'docs_dir' : 'any_folder'
        'file' : 'path/to/custom_attributes.css'
    }
text = 'any string with custom attributes'
print(convert_text_attributes(text, config))
```

### Functions : 
- `read_custom(config: dict[str, str] -> list` : Read the css file and take each css ID and return it as a list. Return empty list if file not found.
- `cleanned_word(line: str, word_regex: str) -> str` : Check and convert the word before tags attributes if any. Return empty string if no word are found.
- `convert_hashtags (config: dict[str, str], line: str) -> str`: Convert the tags attributes from the list when reading a line. 
- `convert_text_attributes(markdown: str, config: dict[str, str]) -> str` : Read an entire Markdown text to convert line per line the hashtags and tags attributes.


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
text to left#left
```
Will become :
```markdown
**text to left**{: #left}\n
```
or in html : 
```html
<p><strong id="left">text to left</strong></p>
```

> 💭 You can note that I choose to use bold to mark the inline attribute. You can remove it with `font-weight: normal;` in the css file when specify your tags.

Also, some inlines attribute can be a bit strange. 
First, any inline attributes placed in the end of the line will be applied on the entire paragraph. 

There is a lot of possible example, so you can check the tests to saw behavior. Please, also refer to the [attribute list documentation](https://python-markdown.github.io/extensions/attr_list/).

| original                                                            | converted attribute                                                                 | html                                                                                                                  |
|---------------------------------------------------------------------|-------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `text to left#left`                                                 | `**text to left**{: #left}`                                                         | <p><strong id="left">text to left</strong></p>`                                                                       |
| `#FFXIV`                                                            | `**FFXIV**{: #FFXIV .hash}`                                                         | `<p><strong class="hash" id="FFXIV">FFXIV</strong></p>`                                                               |
| `#FFXIV #other`                                                     | `**FFXIV**{: #FFXIV .hash} **other**{: #other .hash}`                               | `<p><strong class="hash" id="FFXIV">FFXIV</strong> <strong class="hash" id="other">other</strong></p>`                |
| `text1#left text2#left`                                             | `**text1 text2**{: #left}`                                                          | `<p><strong id="left">text1 text2</strong></p>`                                                                       |
| `Lorem ipsum dolor#blue sit amet, consectetur adipiscing elit#left` | `**Lorem ipsum **dolor**{: #blue} sit amet, consectetur adipiscing elit**{: #left}` | `<p><strong>Lorem ipsum </strong>dolor<strong id="left">{: #blue} sit amet, consectetur adipiscing elit</strong></p>` |
| `to left#left #FFXIV`                                               | `to **left**{: #left} **FFXIV**{: #FFXIV .hash}`                                    | `<p>to <strong id="left">left</strong> <strong class="hash" id="FFXIV">FFXIV</strong></p>`                            |
| `lorem ipsum with #FFXIV and #left`[^1]                             | `lorem ipsum with **FFXIV**{: #FFXIV .hash} and \n{: #left}`                        | `<p id="left">lorem ipsum with <strong class="hash" id="FFXIV">FFXIV</strong> and <br /></p>`                         |




[^1]: Note the absence of word before the last tags. 



# Stylize tags

You can also custom your inline tags (hello obsidian user!) using the `.hash` class!
For example:
```css
.hash {
    background-color: honeydew;
    border-radius: 5px;
}
```


import html2text


def richtext_to_md2(richtext_field):
    html_content = richtext_field
    # Инициализируем объект html2text
    converter = html2text.HTML2Text()
    converter.body_width = 0  # Ширина строки, 0 для отключения переносов строк
    markdown_content = converter.handle(html_content)
    return markdown_content.replace(';', '\n')

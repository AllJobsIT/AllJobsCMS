from django import template

register = template.Library()


@register.simple_tag
def select_language(context):
    st.markdown("<h1 style='text-align: center'>Парсер резюме</h1>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader('Загрузите резюме для анализа:')
    return

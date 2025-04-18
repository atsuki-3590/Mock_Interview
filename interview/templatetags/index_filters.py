from django import template

register = template.Library()

@register.filter
def index(sequence, i):
    """
    sequence[i] を返す。範囲外なら空文字を返す。
    使用例: {{ my_list|index:0 }}
    """
    try:
        return sequence[int(i)]
    except (IndexError, ValueError, TypeError):
        return ""
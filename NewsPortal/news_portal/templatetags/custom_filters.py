from django import template

register = template.Library()


@register.filter()
def censor(value):
    censored_words = ['ass', 'bitch', 'cock', 'fuck']
    cen_text = value.split()
    for i in censored_words:
        for words in cen_text:
            if i in words:
                psn_in_text = cen_text.index(words)
                cen_text.remove(words)
                cen_text.insert(psn_in_text, i[0] + '*' * (len(i)-1))
    return " ".join(cen_text)

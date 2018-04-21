from django import template
from factchecker.utils import (
    get_random_gender_emoji,
    get_random_skin_tone_emoji,
)

register = template.Library()


@register.filter
def randomize_gender_and_skin_tone(emoji):
    """
    Append random skin-tone and (zero-width joiner then) gender chars to emoji.
    """
    emoji += get_random_skin_tone_emoji()
    emoji += u"\u200D"
    emoji += get_random_gender_emoji()
    emoji += u"\uFE0F"
    
    return emoji


@register.filter
def randomize_gender(emoji): # Only one argument.
    """
    Append zero-width joiner and random gender characters to emoji.
    """
    emoji += u"\u200D"
    emoji += get_random_gender_emoji()
    emoji += u"\uFE0F"
    
    return emoji


@register.filter
def randomize_skin_tone(emoji): # Only one argument.
    """
    Append random skin-tone character to emoji.
    """
    emoji += get_random_skin_tone_emoji()
    emoji += u"\uFE0F"
    
    return emoji


@register.simple_tag
def random_gender():
    """Return random gender emoji."""

    return get_random_gender_emoji()


@register.simple_tag
def random_skin_tone():
    """Return random skin-tone emoji."""

    return get_random_skin_tone_emoji()

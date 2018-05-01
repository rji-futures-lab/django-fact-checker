from django.conf import settings


def custom_website_metadata(request):
    """
    Load custom metadata into response context.
    """
    metadata = {
        'CUSTOM_WEBSITE_TITLE': getattr(
            settings,
            'CUSTOM_WEBSITE_TITLE',
            'Django Fact Checker Site',
        ),
        'CUSTOM_WEBSITE_DESCRIPTION': getattr(
            settings,
            'CUSTOM_WEBSITE_DESCRIPTION',
            'Built with Django in the RJI Futures Lab.',
        ),
        'url': request.build_absolute_uri(),
    }

    try:
        metadata['CUSTOM_WEBSITE_SHARE_IMG'] = settings.CUSTOM_WEBSITE_SHARE_IMG
    except AttributeError:
        pass

    try:
        metadata['TWITTER_HANDLE'] = settings.CUSTOM_WEBSITE_SHARE_IMG
    except AttributeError:
        pass

    return metadata

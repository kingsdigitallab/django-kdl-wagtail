from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(items, page=1, page_size=10):
    if not items:
        return None

    if hasattr(settings, 'KDL_WAGTAIL_ITEMS_PER_PAGE'):
        page_size = settings.KDL_WAGTAIL_ITEMS_PER_PAGE

    paginator = Paginator(items, page_size)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return pages

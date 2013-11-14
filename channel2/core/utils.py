from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.utils.text import slugify as django_slugify
from unidecode import unidecode


def slugify(s):
    """
    Slugify based on django's slugify except uses unidecode to work with
    non-ascii characters.
    """

    return django_slugify(unidecode(s))


def paginate(object_list, page_size, page_num):
    """
    Takes an object_list, page_size, page_num and paginates the object list.
    """

    paginator = Paginator(object_list, page_size)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = Page([], 1, paginator)
        page.page_range = []
        return page

    start = page.number - 3
    if start < 0: start = 0
    end = page.number + 2
    if end > paginator.num_pages: end = paginator.num_pages

    page.page_range = paginator.page_range[start:end]

    return page

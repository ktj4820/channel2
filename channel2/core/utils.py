from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.template import loader
from django.utils.text import slugify as django_slugify
from unidecode import unidecode
from channel2.settings import EMAIL_HOST_USER, DEBUG, ADMINS


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


def get_ip_address(request):
    """
    Returns the user's ip address from the request.
    """

    ip_address = request.META.get('REMOTE_ADDR', '')
    ip_address = ip_address[:200]
    return ip_address


def email_alert(subject, template, context):
    """
    Send an email to ADMINS
    """

    if DEBUG or not EMAIL_HOST_USER: return

    recipient_list = [email for _, email in ADMINS]
    send_mail(
        subject=subject,
        message=loader.get_template(template).render(context),
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list
    )

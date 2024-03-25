import re
def is_vk_link(link):
    """
    Проверяет, является ли ссылка из ВКонтакте.
    Возвращает True, если ссылка действительно из ВК, иначе False.
    """
    # Пример логики проверки ссылки из ВКонтакте
    if "vk.com" in link:
        return True
    else:
        return False
def is_yandex_or_google_disk_link(link: str) -> bool:
    """
    Проверяет, является ли ссылка на Яндекс или Google Диск.

    :param link: Ссылка для проверки.
    :return: True, если ссылка ведет на Яндекс или Google Диск, в противном случае - False.
    """
    # Регулярное выражение для проверки ссылки на Яндекс или Google Диск
    yandex_disk_pattern = r'^https?://(?:www\.)?(?:disk\.yandex\.ru|yadi\.sk)'
    google_disk_pattern = r'^https?://(?:drive\.google\.com)'

    # Проверяем ссылку на соответствие шаблонам
    if re.match(yandex_disk_pattern, link) or re.match(google_disk_pattern, link):
        return True
    else:
        return False

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

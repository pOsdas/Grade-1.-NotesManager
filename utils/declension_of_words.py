def get_word_form(number: int, forms: tuple) -> str:
    """
    Возвращает слово в нужном падеже в зависимости от числа.
    """
    number = abs(number) % 100
    if 11 <= number <= 19:
        return forms[2]

    last_digit = number % 10
    if last_digit == 1:
        return forms[0]
    elif 2 <= last_digit <= 4:
        return forms[1]
    else:
        return forms[2]
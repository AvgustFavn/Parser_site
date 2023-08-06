import re


def price_validator(price):
    print(price)
    if type(price) == type(2):
        if price > 0:
            price = float(price)
        else:
            price = float(price * -1)

        return price
    elif type(price) != type(0.2):
        if price:
            try:
                price = price[:',']
            except:
                pass
            numbers = re.findall(r'\b\d+(?!\-)\b', price)
            print(f'ВАЛИД {numbers}')
            try:
                price = ''.join(numbers).replace(' ', '')
                print(price)
            except:
                price = None

            try:
                price = float(price)
                if not price:
                    price = int(price)
                    price = float(price)
                    return price
                else:
                    return price
            except:
                try:
                    price = int(price)
                    price = float(price)
                    return price
                except:
                    return price

        else:
            return 0
    else:
        return price

def true_validator(val):
    return True

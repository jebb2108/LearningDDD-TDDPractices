class SKUDoesntMatchError(Exception):
    """ Stack keeping unit не совпадают """
    pass

class NotEnoughQuantityError(Exception):
    """ Недостаточное количество товара """
    pass

class AvailableEqualToRequiredError(Exception):
    """ Доступное количество товара равно необходимому """
    pass

class PrefersWarehouseToShipmentError(Exception):
    """ Предпочтение партиям в складе перед партиями в доставке """
    pass

class PrefersEarlierBatchesError(Exception):
    """ Предпочтение партиям, прибывающим раньше """
    pass


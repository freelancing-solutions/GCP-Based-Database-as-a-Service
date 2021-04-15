from google.cloud import ndb
import datetime
from data_service.config import Config
from data_service.utils.utils import create_id


class Stock(ndb.Model):
    """
        A Model for keeping stock code, stored separately on datastore
        but also a sub model of StockModel
    """
    def set_string(self, value: str) -> str:
        """
            takes in string input verifies and returns the same string
            input: value: str
            output str
        """
        value: str = value.strip()
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    def set_stock_name(self, value: str) -> str:
        """
            verify stock_name
        """
        value: str = value.strip().lower()
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    stock_id: str = ndb.StringProperty(required=True, indexed=True, validator=set_string)
    stock_code: str = ndb.StringProperty(required=True, indexed=True, validator=set_string)
    stock_name: str = ndb.StringProperty(required=True, validator=set_stock_name)
    symbol: str = ndb.StringProperty(required=True, indexed=True, validator=set_string)

    def __eq__(self, other) -> bool:
        if self.stock_id != other.stock_id:
            return False
        if self.stock_code != other.stock_code:
            return False
        if self.symbol != other.symbol:
            return False
        return True

    def __str__(self) -> str:
        return "<Stock stock_code: {}, symbol: {}".format(self.stock_code, self.symbol)


class Broker(ndb.Model):
    """
        a model for storing broker data
    """

    def set_id(self, broker_id: str) -> str:
        broker_id = broker_id.strip()
        if broker_id is None or broker_id == "":
            broker_id = create_id(size=12)
        if not isinstance(broker_id, str):
            raise TypeError("{} can only be a string".format(self.name))
        return broker_id

    def set_broker_code(self, broker_code: str) -> str:
        broker_code = broker_code.strip()
        if broker_code is None or broker_code == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(broker_code, str):
            raise TypeError("{} can only be a string".format(self.name))
        return broker_code

    def set_broker_name(self, broker_name: str) -> str:
        broker_name = broker_name.strip()
        if broker_name is None or broker_name == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(broker_name, str):
            raise TypeError("{} can only be a string".format(self.name))
        return broker_name

    broker_id: str = ndb.StringProperty(required=True, indexed=True, validator=set_id)
    broker_code: str = ndb.StringProperty(required=True, indexed=True, validator=set_broker_code)
    broker_name: str = ndb.StringProperty(required=True, validator=set_broker_name)

    def __eq__(self, other) -> bool:
        if self.broker_id != other.broker_id:
            return False
        if self.broker_code != other.broker_code:
            return False
        return True

    def __str__(self) -> str:
        return "<Broker broker_code: {}".format(self.broker_code)


class StockModel(ndb.Model):
    """
        remember to set timezone info when saving date
        id,
        stock_id,
        broker_id,
        stock_code,
        stock_name,
        broker_code,
        date,
        buy_volume,
        buy_value,
        buy_ave_price,
        buy_market_val_percent,
        buy_trade_count,
        sell_volume,
        sell_value,
        sell_ave_price,
        sell_market_val_percent,
        sell_trade_count,
        net_volume,
        net_value,
        total_volume,
        total_value
    """

    def set_id(self, value: str) -> str:
        value: str = value.strip()
        if value is None or value == "":
            raise ValueError('{} cannot be Null'.format(self.name))
        if not isinstance(value, str):
            raise TypeError('{} may only be a string'.format(self.name))
        return value

    def set_stock(self, stock: Stock) -> Stock:
        if not isinstance(stock, Stock):
            raise TypeError('{}, needs to be an instance of Stock'.format(self.name))
        return stock

    def set_broker(self, broker: Broker) -> Broker:
        if not isinstance(broker, Broker):
            raise TypeError("{}, Needs to be an instance of Broker".format(self.name))
        return broker

    exchange_id: str = ndb.StringProperty(required=True, indexed=True, validator=set_id)
    transaction_id: str = ndb.StringProperty(validator=set_id)
    stock = ndb.StructuredProperty(Stock, validator=set_stock)
    broker = ndb.StructuredProperty(Broker, validator=set_broker)


class BuyVolumeModel(ndb.Model):
    """
        daily buy volumes
    """

    def set_stock_id(self, value: str) -> str:
        value = value.strip()
        if value is None or value == "":
            raise ValueError('{} cannot be Null'.format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    def set_date(self, value: object) -> object:
        if isinstance(value, object):
            return value
        raise TypeError('{} can only be an object of datetime'.format(self.name))

    def set_int_property(self, value: int) -> int:
        if value is None or value == "":
            raise ValueError("{} can not be Null".format(self.name))

        if not isinstance(value, int):
            raise TypeError("{} can only be an Integer".format(self.name))
        if value < 0:
            raise ValueError("{} can only be a positive integer".format(self.name))
        return value

    transaction_id: str = ndb.StringProperty(indexed=True, required=True, default=create_id())
    stock_id: str = ndb.StringProperty(validator=set_stock_id)
    date: object = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET), validator=set_date)
    buy_volume: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_value: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_ave_price: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_market_val_percent: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_trade_count: int = ndb.IntegerProperty(default=0, validator=set_int_property)


class SellVolumeModel(ndb.Model):
    """
        daily sell volumes
    """
    def set_id(self, value: str) -> str:
        value = value.strip()
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    def set_int(self, value: int) -> int:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, int):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    def set_transaction_id(self, transaction_id: str) -> str:
        transaction_id = transaction_id.strip()
        if transaction_id is None or transaction_id == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(transaction_id, str):
            raise TypeError("{} can only be a str".format(self.name))
        return transaction_id
    transaction_id: str = ndb.StringProperty(indexed=True, validator=set_transaction_id)

    stock_id: str = ndb.StringProperty(validator=set_id)
    # Auto now add can be over written
    date: object = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    sell_volume: int = ndb.IntegerProperty(default=0, validator=set_int)
    sell_value: int = ndb.IntegerProperty(default=0, validator=set_int)
    sell_ave_price: int = ndb.IntegerProperty(default=0, validator=set_int)
    sell_market_val_percent: int = ndb.IntegerProperty(default=0, validator=set_int)
    sell_trade_count: int = ndb.IntegerProperty(default=0, validator=set_int)


class NetVolumeModel(ndb.Model):
    """
        daily net volume
    """
    def set_id(self, value: str) -> str:
        value = value.strip()
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    def set_int(self, value: int) -> int:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, int):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    stock_id: str = ndb.StringProperty(validator=set_id)
    transaction_id: str = ndb.StringProperty(validator=set_id)
    date: object = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    net_volume: int = ndb.IntegerProperty(default=0, validator=set_int)
    net_value: int = ndb.IntegerProperty(default=0, validator=set_int)
    total_volume: int = ndb.IntegerProperty(default=0, validator=set_int)
    total_value: int = ndb.IntegerProperty(default=0, validator=set_int)
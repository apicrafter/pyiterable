import datetime
import logging

from ..common.common import get_dict_value, set_dict_value
from ..constants import DATE_PATTERNS_SHORT, DATETIME_PATTERNS

TYPE_DATE = 1
TYPE_INT = 2
TYPE_FLOAT = 3


date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else None
)


def map_keys(obj, keys, qd=None):
    """Maps object to the predefined schema from `keys`"""
    if qd is not None:
        parser = qd
        datefunc = parser.parse
    else:
        datefunc = convert_to_datetime
    result = {}
    for k in obj.keys():
        k1 = k.lstrip('@').lstrip('#')
        if k1 not in keys.keys():
            logging.info(u'Unknown key %s' % (k))
        rule = keys[k1]
        newk = rule['name']
        if 'type' in rule.keys():
            if rule['type'] == TYPE_INT:
                result[newk] = int(obj[k])
            elif rule['type'] == TYPE_DATE:
                #                parts = obj[k].split('.')
                result[newk] = datefunc(obj[k])
            elif rule['type'] == TYPE_FLOAT:
                result[newk] = float(obj[k])
        elif type(obj[k]) == type({}):
            result[newk] = map_keys(obj[k], keys, qd=qd)
        elif type(obj[k]) == type([]):
            items = []
            for item in obj[k]:
                if type(item) == type({}):
                    o = map_keys(item, keys, qd=qd)
                else:
                    o = item
                items.append(o)
            result[newk] = items
        else:
            #            print(obj)
            result[newk] = obj[k]
    return result


def convert_to_datetime(string):
    """Resource consuming but effective date time conversion"""
    try:
        if len(string) == 0:
            return None
        # Условие для случаев вида "20170001" или "20171200". Если валидный год, преобразовать в условную дату YYYY.01.01
        elif string[4:6] == '00' or string[6:] == '00':
            string = string[:4] + '0101'
    except TypeError:
        pass
    for pat in DATETIME_PATTERNS:
        try:
            return datetime.datetime.strptime(string, pat)
        except Exception as e:
            continue
    #    logging.debug('%s is not datetime' % (string))
    return None


# FIXME: This is very slow simplified date processing without known date pattern for each record
# It should be rewritten to speed up dates processing
def convert_to_date(string):
    """Resource consuming but effective date conversion"""
    try:
        if len(string) == 0:
            return None
        # Условие для случаев вида "20170001" или "20171200". Если валидный год, преобразовать в условную дату YYYY.01.01
        elif string[4:6] == '00' or string[6:] == '00':
            string = string[:4] + '0101'
    except TypeError:
        pass
    for pat in DATE_PATTERNS_SHORT:
        try:
            return datetime.datetime.strptime(string, pat)
        except Exception as e:
            continue
    #    logging.debug('%s is not datetime' % (string))
    return None


def convert_to_int(string):
    """String to integer. #FIXME """
    if len(string) == 0: return None
    try:
        return int(string)
    except Exception as e:
        logging.info(str(e))


def convert_to_float(string):
    """String to float. #FIXME """
    if type(string) == type(u"") and len(string) == 0: return None
    if not string: return None
    try:
        return float(string)
    except Exception as e:
        logging.info(str(e))


def convert_to_bool(string):
    """String to boolean. #FIXME """
    #    if len(string) == 0: return None
    if string == '0' or string.lower() == 'false':
        return False
    elif string == '1' or string.lower() == 'true':
        return True
    else:
        return string


def map_document_fields(obj, bool_fields=[], date_fields=[], float_fields=[], int_fields=[], ):
    """Convert object fields to the selected formats"""
    FUN_FIELDS = [[bool_fields, convert_to_bool], [date_fields, convert_to_datetime], [int_fields, convert_to_int],
                  [float_fields, convert_to_float]]
    result = dict()
    for key in obj.keys():
        value = obj[key]
        if value is None: continue
        found = False
        for fields, func in FUN_FIELDS:
            if key in fields:
                found = True
                if type(value) == type([]):
                    value = list(map(func, value))
                else:
                    value = func(value)
        if found:
            #            logging.info(u'%s %s' % (key, str(value)))
            result[key] = value
            continue
        if type(value) is dict and len(value):
            result[key] = map_document_fields(value, bool_fields=bool_fields, int_fields=int_fields,
                                              float_fields=float_fields, date_fields=date_fields)
        elif type(value) is list and len(value):
            result[key] = list()
            for item in value:
                if type(item) is dict:
                    result[key].append(map_document_fields(item, bool_fields=bool_fields, int_fields=int_fields,
                                                           float_fields=float_fields, date_fields=date_fields))
                else:
                    result[key].append(item)
        else:
            result[key] = value
    return result


TYPEMAP = {'bool': convert_to_bool, 'datetime': convert_to_datetime, 'date': convert_to_date, "int": convert_to_int,
           "float": convert_to_float}


def schema_to_func(schema):
    output = {}
    for key, value in schema.items():
        output[key] = TYPEMAP[value]
    return output


def simple_typemap_object(obj, schema={}):
    """Convert object fields to the selected formats using data schema
    #FIXME: This is very ineffective conversion function that try to detect data formats without knowledge. It could be much much faster
    """
    schema_func = schema_to_func(schema)
    result = obj.copy()
    datakeys = schema.keys()
    for key in datakeys:
        if key in obj.keys():
            result[key] = schema_func[key](obj[key]) if obj[key] is not None else None
        else:
            try:
                value = get_dict_value(obj, key)
                result = set_dict_value(result, key, schema_func[key](value))
            except KeyError:
                continue
    return result

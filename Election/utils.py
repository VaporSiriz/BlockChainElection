from datetime import datetime
import collections
import logging

logger = logging.getLogger(__name__)

def row_to_dict(row):

    if row is None:
        return None

    dict = {}
    columns = row.__table__.columns
    relationships = row.__mapper__.relationships.keys()

    table_name = row.__table__.name

    for column in columns:
        column_name = column.name

        if column_name in relationships:
            rel = getattr(row, column_name)
            dict[column_name] = rel.id
        else:
            value = getattr(row, column_name)
            if value:
                if isinstance(value, datetime):
                    dict[column_name] = str(value)
                else:
                    dict[column_name] = value
            else:
                if isinstance(value, int) or isinstance(value, long):
                    dict[column_name] = 0
                else:
                    dict[column_name] = None
    return dict

def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d: d[0]))
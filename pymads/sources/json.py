from __future__ import absolute_import

import json

from pymads.record import Record
from pymads.sources.dict import DictSource

try:
    basestring
except:
    basestring = str

class JSONSource(DictSource):
    '''
    Subclass of DictSource, pulls data from JSON file.

    Data format:
        {
            "mydomain.com" : [
                {
                    "rdata": "6.6.6.6"
                }
            ],
            "myotherdomain.com" : [
                {
                    "rdata": "9.9.9.9"
                },
                {
                    "type" : "AAAA",
                    "rdata": "fcd9:e703:498e:5d07:e5fc:d525:80a6:a51c"
                }
            ]
        }
    '''
    def __init__(self, source):
        if isinstance(source, basestring):
            # Source is a path
            jsonfile = open(source)
            data = json.load(jsonfile)
        elif hasattr(source, 'read'):
            # Source is a file-like object
            data = json.load(source)
        elif isinstance(source, dict):
            # Source is a dict
            data = source

        DictSource.__init__(self, toRecordDict(data))

def toRecordDict(data):
    '''
    Turn a JSON dict source dict into a dict of Records.
    '''
    if not isinstance(data, dict):
        raise TypeError("JSONSource expects top-level object to be a dict")

    for k in data:
        records = data[k]
        if not isinstance(records, list):
            raise TypeError("JSONSource expects each top-level value to be a list of records")
        data[k] = [toRecord(r, k) for r in records]

    return data

def toRecord(record, fallback_domain):
    '''
    Turn an individual record data dict into a Record object.
    '''
    if not isinstance(record, dict):
        raise TypeError("JSONSource expects each top-level value to be a list of record dicts")
    if not 'domain_name' in record:
        record['domain_name'] = fallback_domain
    return Record(**record)

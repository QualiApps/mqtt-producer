# Telemetry player
#
# works with directory trips, located at the same path as __file__
# including subdirectories

import os
import csv
import time


class Telemetry:
    ''' Incapsulation of the CSV reader functionality
    '''

    def __init__(self, init_dir = None):
        self.__current_source_id = 0
        file_dir =  init_dir or os.path.dirname(os.path.realpath(__file__))
        trips_dir = init_dir or os.path.join(file_dir, 'trips')
        self.__data_sources = []
        map(lambda a: self.__data_sources.extend(
                                  os.path.join(a[0], fname) for fname in a[2]),
            os.walk(trips_dir))

        self.__data_sources.sort()
        self.__source = None
        self.__reader = None

    def get_sources(self):
        return self.__data_sources[:] # return copy to prevent changes

    def force_data_source(self, data_source_id):
        self.__current_source_id = data_source_id
        self.open_data_source()

    def open_data_source(self):
        '''
        Generic method to open data source
        '''
        self.close_data_source()
        self.__source = open(self.__data_sources[self.__current_source_id])
        self.__reader = csv.DictReader(self.__source)
        print 'Using data source', self.__source.name
        return self

    __enter__ = open_data_source
    __iter__ = open_data_source

    def close_data_source(self):
        '''
        Generic method to close data source
        '''
        if (self.__source):
            try:
                self.__source.close()
            except:
                pass
            finally:
                del self.__source

    __exit__ = close_data_source

    def next(self):
        '''
        '''
        result = {}
        try:
            if self.__reader is None:
                return None, None
            result = self.__reader.next()
        except StopIteration:
            #in case of EOF next data source will be opened
            self.__current_source_id += 1
            if self.__current_source_id >= len(self.__data_sources):
                self.__current_source_id = 0
            self.open()
            result = self.__reader.next()
        finally:
            ret = { 'obd': {}, 'gps': {} }
            for key, value in result.iteritems():
                category, param = key.split('.')
                if ret.has_key(category):
                    ret[category][param] = float(value)

            ret['obd']['time'] = time.time()
            return ret['obd'], ret['gps']

    __next__ = next #Python 3.x support

if __name__ == '__main__':
    '''
    Just for debug purposes
    '''
    tlm = Telemetry()
    import sys
    from pprint import pprint
    pprint(tlm.get_sources())
    for record in tlm:
        pprint(record);
        time.sleep(1)

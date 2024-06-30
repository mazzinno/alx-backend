#!/usr/bin/python3

'''
MRU Caching
'''
from collections import deque
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    Inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """
        Initialize
        """
        self.frequency_of_item = {}
        self.lfu_order = []
        super().__init__()

    def put(self, key, item):
        """
       Print or discard the least recently used item (LRU algorithm)
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.frequency_of_item[key] += 1
                self.lfu_order.remove(key)
            else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    min_value = min(self.frequency_of_item.values())
                    min_keys = [keys for keys in self.frequency_of_item
                                if self.frequency_of_item[keys] == min_value]
                    for index in range(len(self.lfu_order)):
                        if self.lfu_order[index] in min_keys:
                            break
                    del self.cache_data[self.lfu_order[index]]
                    del self.frequency_of_item[self.lfu_order[index]]
                    print("DISCARD:", self.lfu_order[index])
                    self.lfu_order.pop(index)
                self.cache_data[key] = item
                self.frequency_of_item[key] = 1
            self.lfu_order.append(key)

    def get(self, key):
        """
        Return value of cache_data linked to key
        """
        if key in self.cache_data:
            self.lfu_order.remove(key)
            self.lfu_order.append(key)
            self.frequency_of_item[key] += 1
            return self.cache_data[key]
        else:
            return None

"""Модуль, реализующий кэш DNS сервера"""
import sys
import pickle
from datetime import datetime
from time import time
from threading import RLock


try:
    from dns_packet import *
except ImportError:
    sys.exit('Program module not found')


class Cache:
    """Класс, реализующий кэш"""

    def __init__(self):
        """Конструктор"""
        self.cache = {}
        self.lock = RLock()

    def add_entry(self, reply_frame: DNSPacket):
        """Добавление записи в кэш"""
        with self.lock:
            counter = 0
            for answers in [reply_frame.answers_rrs, reply_frame.authority_rrs, reply_frame.additional_rrs]:
                if answers is not None:
                    for answer in answers:
                        cache_entry = self.cache.get((answer.aname, answer.atype), None)
                        if cache_entry is None:
                            self.cache.update({(answer.aname, answer.atype): [(answer.address, time() + answer.ttl)]})
                            counter += 1
                        else:
                            flag = True
                            for entry in cache_entry:
                                if entry[0] == answer.address:
                                    flag = False
                            if flag:
                                cache_entry.append((answer.address, time() + answer.ttl))
                                counter += 1
            print(f"> {datetime.now()} > {counter} entries have been added to the cache")

    def find_entry(self, request_frame: DNSPacket):
        """Поиск записи в кеше и формирование ответного пакета"""
        with self.lock:
            query = request_frame.queries[0]
            if isinstance(query, Queries):
                cache_entries = self.cache.get((query.qname, query.qtype), None)
                if cache_entries is None:
                    return None
                else:
                    answers = []
                    for entry in cache_entries:
                        if time() > entry[1]:
                            cache_entries.remove(entry)
                        else:
                            answers.append(Answer(query.qname, query.qtype, entry[0]))
                    if len(answers) == 0:
                        return None
                    else:
                        transaction_id = request_frame.header.transaction_id
                        print(f"> {datetime.now()} > Entry found in cache. The answer is formed")
                        return DNSPacket(make_standard_header(transaction_id, 1, len(answers), 0, 0),
                                         request_frame.queries, answers)


def make_standard_header(transactions_id, quest_len, answer_len, auth_len, add_len):
    """Создание стандартного заголовка для ответа"""
    return Header(transactions_id, 1, 0, 0, 0, 1, 0, 0, quest_len, answer_len, auth_len, add_len)


def save_cache_in_file(cache: Cache):
    """Сохранить кэш в файл"""
    with open("dns.cache", "wb") as file:
        pickle.dump(cache.cache, file)


def load_cache_from_file(cache: Cache):
    """Загрузить кэш из файла"""
    with open("dns.cache", "rb") as file:
        loading_cache = pickle.load(file)
        cache.cache = loading_cache

"""Этот модуль реализуют описание и разбор DNS пакета"""
import sys

try:
    import bitstring
except ImportError:
    sys.exit('Module "bitstring" not found')


class DNS:
    """Вспомогательный класс с константами"""

    QR_TABLE = {0: 'query', 1: 'response'}
    OPCODE_TABLE = {0: 'Standard query', 1: 'Inverse query', 2: 'Server status request'}
    AUTHORITATIVE_TABLE = {0: 'not an authority', 1: 'authority'}
    TRUNCATED_TABLE = {0: 'not truncated', 1: 'truncated'}
    RECDESIRED_TABLE = {0: 'Do not query recursively', 1: 'Do query recursively'}
    RECAVAILABLE_TABLE = {0: 'can not do recursively', 1: 'can do recursively'}
    RCODE_TABLE = {0: 'No error', 1: 'Format error', 2: 'Server failure', 3: 'Name error',
                   4: 'Not implemented', 5: 'Refused'}
    TYPE_TABLE = {1: 'A', 2: 'NS', 5: 'CNAME', 6: 'SOA', 12: 'PTR', 28: 'AAAA'}


class DNSPacket:
    """Класс DNS пакета"""

    def __init__(self, header=None, queries=None, answers_rrs=None, authority_rrs=None, additional_rrs=None):
        """Контруктор"""
        self._header = header
        self._queries = queries
        self._answers_rrs = answers_rrs
        self._authority_rrs = authority_rrs
        self._additional_rrs = additional_rrs


class Header:
    """Класс заголовка DNS пакета"""

    def __init__(self, transaction_id, qr=0, opcode=0, authoritative=0, truncated=0, recursion_desired=0,
                 recursion_available=0, reply_code=0, questions=0, answer_rrs=0, authority_rrs=0, additional_rrs=0):
        """Контруктор"""
        self._transaction_id = transaction_id                # Идентификация
        self._qr = qr                                        # Тип сообщения
        self._opcode = opcode                                # Код операции
        self._authoritative = authoritative                  # Авторитетный ответ
        self._truncated = truncated                          # Обрезанное сообщение
        self._recursion_desired = recursion_desired          # Требуется рукурсия
        self._recursion_available = recursion_available      # Рекурсия возможна
        self._reply_code = reply_code                        # Код возврата
        self._questions = questions                          # Количество вопросов
        self._answer_rrs = answer_rrs                        # Количество обычных ответов
        self._authority_rrs = authority_rrs                  # Полномочный источник
        self._additional_rrs = additional_rrs                # Дополнительная информация

    @property
    def transaction_id(self):
        return self._transaction_id

    @property
    def qr(self):
        return self._qr

    @property
    def opcode(self):
        return self._opcode

    @property
    def authoritative(self):
        return self._authoritative

    @property
    def truncated(self):
        return self._truncated

    @property
    def recursion_desired(self):
        return self._recursion_desired

    @property
    def recursion_available(self):
        return self._recursion_available

    @property
    def reply_code(self):
        return self._reply_code

    @property
    def questions(self):
        return self._questions

    @property
    def answer_rrs(self):
        return self._answer_rrs

    @property
    def authority_rrs(self):
        return self._authority_rrs

    @property
    def additional_rrs(self):
        return self._additional_rrs

    def __str__(self):
        """Переопределение метода вывода"""
        result = f'  Transactions ID: {self.transaction_id}\n' \
                 f'  Response: Massage is a {DNS.QR_TABLE.get(self.qr)} ({self.qr})\n' \
                 f'  Opcode: {DNS.OPCODE_TABLE.get(self.opcode, "Reserved value")} ({self.opcode})\n'
        if self.qr == 0:
            result += f'  Truncated: Massage is {DNS.TRUNCATED_TABLE.get(self.truncated)} ({self.truncated})\n' \
                      f'  Recursion desired: {DNS.RECDESIRED_TABLE[self.recursion_desired]} ' \
                      f'({self.recursion_desired})\n'
        else:
            result += f'  Authoritative: Server is {DNS.AUTHORITATIVE_TABLE.get(self.authoritative)} for domain ' \
                      f'({self.authoritative})\n' \
                      f'  Truncated: Massage is {DNS.TRUNCATED_TABLE.get(self.truncated)} ({self.truncated})\n' \
                      f'  Recursion desired: {DNS.RECDESIRED_TABLE[self.recursion_desired]} ' \
                      f'({self.recursion_desired})\n' \
                      f'  Recursion available: Server {DNS.RECAVAILABLE_TABLE[self.recursion_available]} ' \
                      f'({self.recursion_available})\n' \
                      f'  Reply code: {DNS.RCODE_TABLE.get(self.reply_code, "Reserved value")} ({self.reply_code})\n'
        result += f'  Question: {self.questions}\n' \
                  f'  Answer RRs: {self.answer_rrs}\n' \
                  f'  Authority RRs: {self.authority_rrs}\n' \
                  f'  Additional RRs: {self.additional_rrs}'
        return result


class Queries:
    """Класс вопроса DNS пакета"""

    def __init__(self, qname, qtype, qclass):
        """Конструктор"""
        self._qname = qname     # Доменное имя
        self._qtype = qtype     # Тип запроса
        self._qclass = qclass   # Класс запроса
        
    @property
    def qname(self):
        return self._qname

    @property
    def qtype(self):
        return self._qtype
    
    @property
    def qclass(self):
        return self._qclass

    def __str__(self):
        """Переопределение метода вывода"""
        return f'  Name: {self.qname}\n' \
               f'  Type: {DNS.TYPE_TABLE.get(self.qtype, "Unknown")} ({self.qtype})\n' \
               f'  Class: IN ({self.qclass})'


class Answer:
    """Класс ответа DNS пакета"""

    def __init__(self, aname, atype, aclass, ttl, data_length, address):
        """Контруктор"""
        self._aname = aname                 # Доменное имя
        self._atype = atype                 # Тип запроса
        self._aclass = aclass               # Класс запроса
        self._ttl = ttl                     # Время жизни записи в кеше
        self._data_length = data_length     # Размер данных
        self._address = address             # адресс
        
    @property
    def aname(self):
        return self._aname
    
    @property
    def atype(self):
        return self._atype
    
    @property
    def aclass(self):
        return self._aclass 
    
    @property
    def ttl(self):
        return self._ttl
    
    @property
    def data_length(self):
        return self._data_length
    
    @property
    def address(self):
        return self._address

    def __str__(self):
        """Переопределение метода вывода"""
        return f'  Name: {self.aname}\n' \
               f'  Type: {DNS.TYPE_TABLE.get(self.atype, "Unknown")} ({self.atype})\n' \
               f'  Class: IN ({self.aclass})\n' \
               f'  Time to live: {self.ttl}\n' \
               f'  Data length: {self.data_length}\n' \
               f'  Address: {self.address}'


class DNSPacketError(Exception):
    """Ошибка возникающая при разборе пакета"""
    pass


def get_bit_packet(data):
    """Получить пакет в виде последовательности бит"""
    return bitstring.Bits(data)


def read_header(bit_packet: bitstring.Bits):
    """Чтене заголвка DNS пакета"""
    transaction_id = bit_packet[0:16].uint
    qr = bit_packet[16:17].uint
    opcode = bit_packet[17:21].uint
    authoritative = bit_packet[21:22].uint
    truncated = bit_packet[22:23].uint
    recursion_desired = bit_packet[23:24].uint
    recursion_available = bit_packet[24:25].uint
    reply_code = bit_packet[28:32].uint
    questions = bit_packet[32:48].uint
    answer_rrs = bit_packet[48:64].uint
    authority_rrs = bit_packet[64:80].uint
    additional_rrs = bit_packet[80:96].uint
    return Header(transaction_id, qr, opcode, authoritative, truncated, recursion_desired, recursion_available,
                  reply_code, questions, answer_rrs, authority_rrs, additional_rrs)


def read_questions(bit_packet: bitstring.Bits, header: Header):
    """Чтение полей запросов DNS пакета"""
    queries = []
    start_index = 96
    for index in range(header.questions):
        query, end_index = _read_question(bit_packet, start_index)
        queries.append(query)
        start_index = end_index
    return queries, start_index


def read_answers(bit_packet: bitstring.Bits, header: Header, start_index):
    """Чтение полей ответов DNS пакетай"""
    answers = []
    for index in range(header.answer_rrs):
        answer, end_index = _read_answer(bit_packet, start_index)
        answers.append(answer)
        start_index = end_index
    authority_rrs = []
    for index in range(header.authority_rrs):
        authority_rr, end_index = _read_answer(bit_packet, start_index)
        authority_rrs.append(authority_rr)
        start_index = end_index
    additional_rrs = []
    for index in range(header.additional_rrs):
        additional_rr, end_index = _read_answer(bit_packet, start_index)
        additional_rrs.append(additional_rr)
        start_index = end_index
    return answers, authority_rrs, additional_rrs


def _read_question(bit_packet: bitstring.Bits, start_index):
    """Чтение одного запроса"""
    qname, end_name_index = _read_name(bit_packet, start_index, name='')
    qtype = bit_packet[end_name_index:end_name_index + 16].uint
    qclass = bit_packet[end_name_index + 16:end_name_index + 32].uint
    return Queries(qname, qtype, qclass), end_name_index + 32


def _read_answer(bit_packet: bitstring.Bits, start_index):
    """Чтение одного ответа"""
    aname, end_name_index = _read_name(bit_packet, start_index, name='')
    atype = bit_packet[end_name_index:end_name_index + 16].uint
    aclass = bit_packet[end_name_index + 16:end_name_index + 32].uint
    ttl = bit_packet[end_name_index + 32:end_name_index + 64].uint
    data_length = bit_packet[end_name_index + 64: end_name_index + 80].uint
    address, end_index = _read_address(bit_packet, end_name_index + 80, data_length, atype)
    return Answer(aname, atype, aclass, ttl, data_length, address), end_index


def _read_name(bit_packet: bitstring.Bits, index, name):
    """Чтение доменного имени"""
    count_of_char = bit_packet[index:index + 8].uint
    while count_of_char != 0:
        if count_of_char >= 192:
            hoop_place = bit_packet[index+2:index+16].uint * 8
            name = _read_name(bit_packet, hoop_place, name)[0]
            return name, index + 16
        else:
            index += 8
            for i in range(count_of_char):
                name += bit_packet[index:index+8].bytes.decode('ASCII')
                index += 8
            name += '.'
        count_of_char = bit_packet[index:index+8].uint
    else:
        return name[:-1], index + 8


def _read_address(bit_packet: bitstring.Bits, index, data_length, type):
    """Чтение адреса"""
    if type == 1:
        address = ''
        for i in range(data_length):
            address += str(bit_packet[index:index + 8].uint)
            index = index + 8
            address += '.'
        return address[:-1], index
    elif type == 2:
        address, index = _read_name(bit_packet, index, name='')
        return address, index
    else:
        raise DNSPacketError("Unsupported format of answer.")


def read(data):
    bit_data = get_bit_packet(data)
    header = read_header(bit_data)
    queries, index = read_questions(bit_data, header)
    answer, answer_1, answer_2 = read_answers(bit_data, header, index)
    print(header)
    for q in queries:
        print(q)
    for a in answer:
        print(a)
    for a in answer_1:
        print(a)
    for a in answer_2:
        print(a)

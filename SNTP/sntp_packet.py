"""Этот модуль реализует разбор и запаковку пакета SNTP"""
import datetime
import sys

try:
    import bitstring
except ImportError:
    sys.exit("Module 'bitsting' not found.")

EPOCH = 2208988800
STRATUM = 3
ID = (235, 80, 141, 90)
PRECISION = -7
POLL = 4
DELAY = 0.20


class SNTPPacket:
    """Класс SNTP пакета"""

    def __init__(self):
        """Initialize class"""
        self._li = 0  # Индикатор коррекции
        self._vn = 0  # Номер версии
        self._mode = 0  # Режим
        self._stratum = 0  # Числовой слой
        self._poll = 0  # Интервал опроса
        self._precision = 0  # Точность
        self._root_delay = 0  # Задрежка
        self._root_dispersion = 0  # Дисперсия
        self._reference_identifier = 0  # Индикатор источника
        self._reference_timestamp = 0  # Время обновления
        self._originate_timestamp = 0  # Начально время
        self._receive_timestamp = 0  # Время приема
        self._transmit_timestamp = 0  # Время отправки

    @property
    def li(self):
        return self._li

    @property
    def vn(self):
        return self._vn

    @property
    def mode(self):
        return self._mode

    @property
    def stratum(self):
        return self._stratum

    @property
    def poll(self):
        return self._poll

    @property
    def precision(self):
        return self._precision

    @property
    def root_delay(self):
        return self._root_delay

    @property
    def root_dispersion(self):
        return self._root_dispersion

    @property
    def reference_identifier(self):
        return self._reference_identifier

    @property
    def reference_timestamp(self):
        return self._reference_timestamp

    @property
    def originate_timestamp(self):
        return self._originate_timestamp

    @property
    def receive_timestamp(self):
        return self._receive_timestamp

    @property
    def transmit_timestamp(self):
        return self._transmit_timestamp

    def read_packet(self, data):
        """Чтение пакета из байт"""
        bits_packet = bitstring.Bits(data)
        if len(bits_packet) < 48:
            raise SNTPPacketError("Invalid SNTP message size.")
        self._li = bits_packet[0:2].uint
        self._vn = bits_packet[2:5].uint
        self._mode = bits_packet[5:8].uint
        self._stratum = bits_packet[8:16].uint
        self._poll = bits_packet[16:24].uint
        self._precision = bits_packet[24:32].int
        self._root_delay = float(bits_packet[32:64].int) / 2 ** 16
        self._root_dispersion = float(bits_packet[64:96].uint) / 2 ** 16
        self._reference_identifier = tuple(bits_packet[96:128].unpack('4*uint: 8'))
        self._reference_timestamp = to_timestamp(bits_packet[128:160].uint, bits_packet[160:192].uint)
        self._originate_timestamp = to_timestamp(bits_packet[192:224].uint, bits_packet[224:256].uint)
        self._receive_timestamp = to_timestamp(bits_packet[256:288].uint, bits_packet[288:320].uint)
        self._transmit_timestamp = to_timestamp(bits_packet[320:352].uint, bits_packet[352:384].uint)


class SNTPPacketError(Exception):
    """Ошибка, возникающая при обработки пакета"""
    pass


def pack_packet(li=0, vn=4, mode=4, stratum=STRATUM, poll=POLL, precision=PRECISION, root_delay=DELAY,
                root_dispersion=0, reference_identifier=ID, reference_timestamp=0, originate_timestamp=0,
                receive_timestamp=0, transmit_timestamp=0, time_shift=0):
    """Запаковать пакет в поток байт"""
    bits_packet = bitstring.BitArray(length=384)
    bits_packet[0:2] = bitstring.pack('uint: 2', li)
    bits_packet[2:5] = bitstring.pack('uint: 3', vn)
    bits_packet[5:8] = bitstring.pack('uint: 3', mode)
    bits_packet[8:16] = bitstring.pack('uint: 8', stratum)
    bits_packet[16:24] = bitstring.pack('uint: 8', poll)
    bits_packet[24:32] = bitstring.pack('int: 8', precision)
    bits_packet[32:64] = bitstring.pack('uint: 32', root_delay)
    bits_packet[64:96] = bitstring.pack('uint: 32', root_dispersion)
    bits_packet[96:128] = bitstring.pack('4*uint: 8', *reference_identifier)
    bits_packet[128:190] = bitstring.pack('uint: 64', 0)
    bits_packet[192:224] = bitstring.pack('uint: 32', int_from_timestamp(originate_timestamp, time_shift))
    bits_packet[224:256] = bitstring.pack('uint: 32', frac_from_timestamp(originate_timestamp, time_shift))
    bits_packet[256:288] = bitstring.pack('uint: 32', int_from_timestamp(receive_timestamp, time_shift))
    bits_packet[288:320] = bitstring.pack('uint: 32', frac_from_timestamp(receive_timestamp, time_shift))
    bits_packet[320:352] = bitstring.pack('uint: 32', int_from_timestamp(transmit_timestamp, time_shift))
    bits_packet[352:384] = bitstring.pack('uint: 32', frac_from_timestamp(transmit_timestamp, time_shift))
    return bits_packet.tobytes()


def to_timestamp(integral_part, fraction_part, n=32):
    """Возвращает timestamp из целой и дробной части
    n -- количество бит в дробной части
    """
    timestamp = integral_part + float(fraction_part) / 2 ** n - EPOCH
    if timestamp < 0:
        return 0.0
    return timestamp


def int_from_timestamp(timestamp, time_shift):
    """Возвращает целую часть timestamp"""
    timestamp = timestamp + EPOCH + time_shift
    return int(timestamp)


def frac_from_timestamp(timestamp, time_shift, n=32):
    """Возвращает дробную часть timestamp"""
    timestamp = timestamp + EPOCH + time_shift
    return int(abs(timestamp - int(timestamp)) * 2 ** n)


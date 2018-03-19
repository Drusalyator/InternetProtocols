# Trace AC

Версия: 1.0

Автор: Гридин Андрей

## Описание програмы

Это программа реализует трассировку до указанного домена или IP адреса, выводя для каждого узла : IP адресс, номер автономной системы, страну и провайдера. В случае "серых" IP адресов в полях "номер автономной системы", "страна", "провайдер" будет запись "Reserved". В случае, если не удалось получить информации о чем ли, в соответсвующем поле будет записать "Unknown". Программа может работать достаточно долго.

## Необходимо

Модуль: requests

## Пример запуска

- `python main.py`
- `python main.py -a [IP address or domain name]`

## Пример вывода

```
python main.py
> Input IP or domain name: www.tni.mil.id
> Tracing to the www.tni.mil.id. Wait...
> Obtaining information about IP addresses...

№    IP                    AS             Country       Provider
---------------------------------------------------------------------------------------
01:  192.168.43.1          Reserved       Reserved      Reserved
02:  192.168.250.2         Reserved       Reserved      Reserved
03:  192.168.250.10        Reserved       Reserved      Reserved
04:  213.87.251.133        AS8359         RU            MTS PJSC
05:  212.188.12.25         AS8359         RU            MTS PJSC
06:  212.188.29.249        AS8359         RU            MTS PJSC
07:  212.188.29.85         AS8359         RU            MTS PJSC
08:  195.34.50.161         AS8359         RU            MTS PJSC
09:  212.188.2.37          AS8359         RU            MTS PJSC
10:  212.188.54.2          AS8359         RU            MTS PJSC
11:  195.34.50.146         AS8359         RU            MTS PJSC
12:  194.68.123.187        AS12552        SE            Resilans AB
13:  184.105.64.105        AS6939         US            Hurricane Electric
14:  184.105.65.29         AS6939         US            Hurricane Electric
15:  184.105.65.34         AS6939         US            Hurricane Electric
16:  184.105.80.14         AS6939         US            Hurricane Electric
17:  184.105.65.13         AS6939         US            Hurricane Electric
18:  27.50.33.110          AS6939         HK            Hurricane Electric (Hong Kong)
19:  182.253.187.5         AS17451        ID            Biznet Networks
20:  182.253.187.73        AS17451        ID            Biznet Networks
21:  118.99.90.114         AS17451        ID            Biznet Networks
22:  112.109.23.6          Unknown        ID            PT Data Utama Dinamika
23:  119.82.240.125        AS24521        ID            PT. DATA Utama Dinamika
```


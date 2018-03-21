# Самостоятельная работа по NSLOOKUP

Автор: Гридин Андрей

Группа: КН-202

##### 2. 

##### Работая с nslookup в режиме одного запроса, выясните адреса серверов имён (NS) для

- urfu.ru

```
ns1.urfu.ru     internet address = 212.193.66.21
ns2.urfu.ru     internet address = 212.193.82.21
ns3.urfu.ru     internet address = 212.193.72.21
```

- msu.ru

```
ns.msu.ru       internet address = 93.180.0.1
ns.msu.net      internet address = 212.16.0.1ns1.orc.ru
ns1.orc.ru      internet address = 212.48.128.152
ns3.nic.fr      internet address = 192.134.0.49
ns3.nic.fr      AAAA IPv6 address = 2001:660:3006:1::1:1
```

##### выясните ip-адреса хостов для символьных имён

- urfu.ru

```
Address:  212.193.82.20
```

- rbc.ru

```
Addresses:  80.68.253.9
            185.72.229.9
```

##### 3. Перейти в режим командной строки nslookup. Выяснить имя и адрес dns-сервера, которому будут отправляться запросы:

```
Server:  A.ROOT-SERVERS.NET
Addresses:  2001:503:ba3e::2:30
          198.41.0.4
```

##### 4. Изучить команды перехода между серверами – server, lserver и root.

```
Server:  UnKnown
Address:  192.168.43.1

> server 194.226.235.1
Server:  [194.226.235.1]
Address:  194.226.235.1

> server ns1.urfu.ru
DNS request timed out.
    timeout was 2 seconds.
DNS request timed out.
    timeout was 2 seconds.
DNS request timed out.
    timeout was 2 seconds.
DNS request timed out.
    timeout was 2 seconds.
*** Не найден адрес для сервера ns1.urfu.ru: Timed out

> lserver ns1.urfu.ru                  #нужная команда
Server:  ns1.urfu.ru
Address:  212.193.66.21
```

Команда Server устанавливает сервер по умолчанию, используя текущий сервер по умолчанию и поэтому, когда мы пытаемся, после перехода на несущетсвующий сервер, задать нормальный DNS сервер мы не можем этого сделать так как несуществующий не отвечает на запросы

А команда LServer для назначения нового сервера использует сервер, который прописан, когда мы введем команду root

```
> server 194.226.235.1
Server:  [194.226.235.1]
Address:  194.226.235.1

> root
Server:  A.ROOT-SERVERS.NET
Addresses:  2001:503:ba3e::2:30
          198.41.0.4
```

##### 5. Перейти в режим запроса записей NS (set q=ns или set type=ns), выяснить адреса серверов имён для доменов верхнего уровня (и их общее количество):

- com

```
com     nameserver = c.gtld-servers.net      #Количество 13
com     nameserver = k.gtld-servers.net
com     nameserver = m.gtld-servers.net
com     nameserver = b.gtld-servers.net
com     nameserver = f.gtld-servers.net
com     nameserver = l.gtld-servers.net
com     nameserver = g.gtld-servers.net
com     nameserver = h.gtld-servers.net
com     nameserver = d.gtld-servers.net
com     nameserver = j.gtld-servers.net
com     nameserver = a.gtld-servers.net
com     nameserver = i.gtld-servers.net
com     nameserver = e.gtld-servers.net
a.gtld-servers.net      internet address = 192.5.6.30
a.gtld-servers.net      AAAA IPv6 address = 2001:503:a83e::2:30
b.gtld-servers.net      internet address = 192.33.14.30
b.gtld-servers.net      AAAA IPv6 address = 2001:503:231d::2:
c.gtld-servers.net      internet address = 192.26.92.30
c.gtld-servers.net      AAAA IPv6 address = 2001:503:83eb::30
k.gtld-servers.net      internet address = 192.52.178.30
k.gtld-servers.net      AAAA IPv6 address = 2001:503:d2d::30
m.gtld-servers.net      internet address = 192.55.83.30
m.gtld-servers.net      AAAA IPv6 address = 2001:501:b1f9::30
f.gtld-servers.net      internet address = 192.35.51.30
f.gtld-servers.net      AAAA IPv6 address = 2001:503:d414::30
l.gtld-servers.net      internet address = 192.41.162.30
l.gtld-servers.net      AAAA IPv6 address = 2001:500:d937::30
g.gtld-servers.net      internet address = 192.42.93.30
g.gtld-servers.net      AAAA IPv6 address = 2001:503:eea3::30
e.gtld-servers.net      internet address = 192.12.94.30
e.gtld-servers.net      AAAA IPv6 address = 2001:502:1ca1::30
j.gtld-servers.net      internet address = 192.48.79.30
j.gtld-servers.net      AAAA IPv6 address = 2001:502:7094::30
h.gtld-servers.net      internet address = 192.54.112.30
h.gtld-servers.net      AAAA IPv6 address = 2001:502:8cc::30
i.gtld-servers.net      internet address = 192.43.172.30
i.gtld-servers.net      AAAA IPv6 address = 2001:503:39c1::30
d.gtld-servers.net      internet address = 192.31.80.30
d.gtld-servers.net      AAAA IPv6 address = 2001:500:856e::30
```

- org

```
org     nameserver = a0.org.afilias-nst.info   #Количесвто 6
org     nameserver = a2.org.afilias-nst.info
org     nameserver = b2.org.afilias-nst.org
org     nameserver = d0.org.afilias-nst.org
org     nameserver = c0.org.afilias-nst.info
org     nameserver = b0.org.afilias-nst.org
a0.org.afilias-nst.info AAAA IPv6 address = 2001:500:e::1
a2.org.afilias-nst.info AAAA IPv6 address = 2001:500:40::1
b0.org.afilias-nst.org  AAAA IPv6 address = 2001:500:c::1
b2.org.afilias-nst.org  AAAA IPv6 address = 2001:500:48::1
c0.org.afilias-nst.info AAAA IPv6 address = 2001:500:b::1
d0.org.afilias-nst.org  AAAA IPv6 address = 2001:500:f::1
a0.org.afilias-nst.info internet address = 199.19.56.1
a2.org.afilias-nst.info internet address = 199.249.112.1
b0.org.afilias-nst.org  internet address = 199.19.54.1
b2.org.afilias-nst.org  internet address = 199.249.120.1
c0.org.afilias-nst.info internet address = 199.19.53.1
d0.org.afilias-nst.org  internet address = 199.19.57.1
```

- ru

```
RU      nameserver = e.dns.ripn.net     # Количество 5
RU      nameserver = f.dns.ripn.net
RU      nameserver = a.dns.ripn.net
RU      nameserver = d.dns.ripn.net
RU      nameserver = b.dns.ripn.net
a.dns.RIPN.net  AAAA IPv6 address = 2001:678:17:0:193:232:128:6
b.dns.RIPN.net  AAAA IPv6 address = 2001:678:16:0:194:85:252:62
d.dns.RIPN.net  AAAA IPv6 address = 2001:678:18:0:194:190:124:17
e.dns.RIPN.net  AAAA IPv6 address = 2001:678:15:0:193:232:142:17
f.dns.RIPN.net  AAAA IPv6 address = 2001:678:14:0:193:232:156:17
a.dns.RIPN.net  internet address = 193.232.128.6
b.dns.RIPN.net  internet address = 194.85.252.62
d.dns.RIPN.net  internet address = 194.190.124.17
e.dns.RIPN.net  internet address = 193.232.142.17
f.dns.RIPN.net  internet address = 193.232.156.17
```

##### 6. Пройти по цепочке серверов имён от корня и, по необходимости меняя в запросе тип записей (set q=…), найти ip-адрес для символьного имени и записать промежуточные данные в виде цепочки результатов запросов

- cs.usu.edu.ru.

```
>ru.               a.dns.ripn.net  internet address = 193.232.128.6
>edu.ru.           ns.MSU.RU  internet address = 93.180.0.1
>usu.eduru.        ns.urgu.org     internet address = 212.193.68.254
cs.usu.edu.ru.     Address:  212.193.68.254
```

- www.imm.uran.ru.

```
>ru.                  a.dns.RIPN.net  internet address = 193.232.128.6
>uran.ru.             ns.URAN.RU      internet address = 195.19.137.69
>imm.uran.ru.         ns.uran.ru      internet address = 195.19.137.69
>www.imm.uran.ru.     Address:  195.19.137.125
```

- kma.imkn.urfu.ru.

```
>ru.                  a.dns.RIPN.net  internet address = 193.232.128.6
>urfu.ru.             ns1.URFU.RU     internet address = 212.193.66.21
>imkn.urfu.ru.        Address:  212.193.66.21
>kma.imkn.urfu.ru.    Address:  212.193.68.65
```

##### 7. Изучить способы получения с сервера всех записей (команда ls). Подключиться к нужному серверу, вывести на экран и сохранить в файл записи для:

- edu.ru    ----> Файл edu.ru.txt
- urfu.ru   ----> Все DNS сервера отклонили запрос из-за параметров безопасности
- mail.ru   ----> Все DNS сервера отклонили запрос из-за параметров безопасности

##### 8. Получить «начальную запись зоны» (SOA – start of authority), выяснить вероятную дату последнего обновления зоны, время жизни записей в промежуточных кеширующих серверах и прочую информацию для:

- ya.ru

```
ya.ru
        primary name server = ns1.yandex.ru
        responsible mail addr = sysadmin.yandex.ru
        serial  = 2018031600
        refresh = 900 (15 mins)
        retry   = 600 (10 mins)
        expire  = 2592000 (30 days)
        default TTL = 900 (15 mins)
```

- urfu.ru

```
urfu.ru
        primary name server = ns1.urfu.ru
        responsible mail addr = hostmaster.urfu.ru
        serial  = 2012091861
        refresh = 3600 (1 hour)
        retry   = 1800 (30 mins)
        expire  = 2419200 (28 days)
        default TTL = 3600 (1 hour)
```

- mail.ru

```
mail.ru
        primary name server = ns1.mail.ru
        responsible mail addr = hostmaster.mail.ru
        serial  = 3312856144
        refresh = 900 (15 mins)
        retry   = 900 (15 mins)
        expire  = 604800 (7 days)
        default TTL = 60 (1 min)
```

##### 9. Найти на www.iana.org (www.icann.org) полный список доменов верхнего уровня. Выяснить на www.nic.ru стоимость регистрации собственного домена в различных зонах, необходимые для этого документы и способы оплаты. Найти (например, в google) регистратора с минимальной стоимостью домена в зоне ru. Найти регистратора с минимальной стоимость домена в зонах com и org

Полный список доменов ферхнего уровня ---> файл top_level_domains.txt

http://nic.ru/dns/contract-zao - документы, регламенты и соглашения о регистрации доменов.

.ru - 189 руб.

.shop - 1190 руб.

.club - 590 руб.

.xyz - 90 руб.

godaddy.com  - 69р. Можно .com и .org


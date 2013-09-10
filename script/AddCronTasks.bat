SCHTASKS /RU work /RP vm123@vrp /Create /TN "update_all_xml_1" /SC DAILY /ST 00:00:00 /TR "python D:\autopack\script\fetchxml.py -f -d -t -b"

SCHTASKS /RU work /RP vm123@vrp /Create /TN "update_daily_xml_1" /SC DAILY /ST 08:00:00 /TR "python D:\autopack\script\fetchxml.py -dtb"

SCHTASKS /RU work /RP vm123@vrp /Create /TN "update_daily_xml_2" /SC DAILY /ST 16:00:00 /TR "python D:\autopack\script\fetchxml.py -dtb"
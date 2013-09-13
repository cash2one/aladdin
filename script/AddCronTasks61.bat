SCHTASKS /RU administrator /RP 1qaz2wsx /Create /TN "update_all_xml_1" /SC DAILY /ST 00:00:00 /TR "python D:\autopack\script\fetchxml.py -fdtb"

SCHTASKS /RU administrator /RP 1qaz2wsx /Create /TN "update_daily_xml_1" /SC DAILY /ST 08:00:00 /TR "python D:\autopack\script\fetchxml.py -dtb"

SCHTASKS /RU administrator /RP 1qaz2wsx /Create /TN "update_daily_xml_2" /SC DAILY /ST 16:00:00 /TR "python D:\autopack\script\fetchxml.py -dtb"

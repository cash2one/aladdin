:loop

fetchxml.py -fdt

aladdin.py -bcrRt baidusd -s 15726 -g bind1
aladdin.py -bcRt baidusd -g bind1
aladdin.py -bcRt baidusd -p ..\info\95_aladin_id.txt -P ..\info\ignored.txt -g bind1

aladdin.py -bcrRt baidusd -s 15726 -g bind2
aladdin.py -bcRt baidusd -g bind2
aladdin.py -bcRt baidusd -p ..\info\95_aladin_id.txt -P ..\info\ignored.txt -g bind2

aladdin.py -bcrRt baidusd -s 15726 -g bind3
aladdin.py -bcRt baidusd -g bind3
aladdin.py -bcRt baidusd -p ..\info\95_aladin_id.txt -P ..\info\ignored.txt -g bind3

aladdin.py -bcrRt baidusd -s 15726 -g bind4
aladdin.py -bcRt baidusd -g bind4
aladdin.py -bcRt baidusd -p ..\info\95_aladin_id.txt -P ..\info\ignored.txt -g bind4

aladdin.py -bcrRt baidusd -s 15726 -g bind5
aladdin.py -bcRt baidusd -g bind5
aladdin.py -bcRt baidusd -p ..\info\95_aladin_id.txt -P ..\info\ignored.txt -g bind5

aladdin.py -bcrRt baidusd -s 15726 -g bind6
aladdin.py -bcRt baidusd -g bind6
aladdin.py -bcRt baidusd -p ..\info\95_aladin_id.txt -P ..\info\ignored.txt -g bind6

goto loop
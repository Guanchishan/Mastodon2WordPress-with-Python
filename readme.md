## 文件构成

- json2csv
	- outbox_json2csv_one_attachment_one_line.py 将Mastodon所导出outbox.json中有attachment（图片、影片等附件）的orderedItems（项目）筛检出，并以一项attachment一行的方式列出。亦即，如一条嘟文有三张图，则会每张图各占一行，整个嘟嘟总共输出三行。如果嘟文无附件，则不输出于.csv文件中。
	- outbox_json2csv_one_id_one_line.py 将Mastodon所导出outbox.json扁平化，非announce（转嘟）的orderedItems逐行列出
	- outbox_json2csv_one_id_one_line_change_timezone.py 将outbox_json2csv_one_id_one_line.py所输出的.csv文件中的嘟文发表时间修改为指定时区（须编辑.py文件中的指定位置），方便导入到位于该时区的WordPress服务器
	- outbox_json2csv_one_id_one_line_id_checking.py 用于检查json转换为csv的过程中有无缺失行
 - json2xml
 	- likes.py 使用方法参见脚本中的注释。

## 使用方式

请在运行.py文件前，将代码中的文件名及其路径修改好。

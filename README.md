# download_studeo-ostasiendeutsche.de
download jpg &amp; desc from studeo-ostasiendeutsche.de

安装，参考57行附近的注释

结果保存在file目录下

图是jpg，描述是同名html。

中间可以停止，url的中间结果保存在pickle.dump里面，想重开删掉可以。

结果jpg不重复下载，除非删掉。

结果描述会重写，因为搜索时候已经拿到内存了，不浪费流量。

单线程的，怕对方服务器屏蔽，反正可以重开，慢慢下吧。

# -*- coding: UTF-8 -*-
"""
获取授信信息
"""

import MySQLdb

# 创建数据库连接
db=MySQLdb.connect(host="localhost", user="test", passwd="test",db="test", port=3306)
cursor=db.cursor()
def main():
    try:
        fw = open('test.sql', 'w')
        fw.truncate()
        # 查询出表
        tables=getTables()
        for t in tables:
            # 生成建表语句
            fw.write(genCreate(t))
          
            # 生成insert语句
            fw.write(genInsert(t))
    finally:
        print "db close"
        db.close() 
        fw.close()

def getTables():
     cursor.execute("show tables");
     tables=cursor.fetchall()
     _t=[]
     for t in tables:
            _t.append(t[0])
     return _t

def genCreate(tn):
     cursor.execute("show create table %s" % tn);
     ct=cursor.fetchall()
     dropSql="drop table %s;\n" % tn;
     return dropSql + ct[0][1]+";\n"

def genInsert(tn):
    cursor.execute("desc %s" % tn)
    fields=cursor.fetchall()
    cursor.execute("select * from " + tn)
    data=cursor.fetchall()
    tf=[]
    for f in fields:
        tf.append(f[0])
    sql="insert into " + tn
    sql+=" (`%s`) \n values " % "`,`".join(tf)
    for d in data:
        val=""
        for v in d:
            if v is None:
                val+="null,"
            else:
                val+="'%s'," % ("%s" % v).replace('\n','\\n').replace('\'',"\\'")
        sql+="\n (%s)," % val[:-1]
    return sql[:-1] + ";\n"

if __name__=='__main__':    
    main() 

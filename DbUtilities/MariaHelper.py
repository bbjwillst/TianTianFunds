from Interfaces.IDbHelper import IDbHelper
import pymysql


class MariaHelper(IDbHelper):
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'port': 3307,
            'user': 'root',
            'password': 'root',
            'db': 'ttfunds',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()

    def connectTo(self, db):
        pass

    def query(self):
        pass

    def queryBySql(self, sql):
        if len(sql) == 0:
            pass
        self.sql = sql

        try:
            self.cursor.execute(self.sql)
            results = self.cursor.fetchall()
            print('成功通过SQL获取数据%s条.' % self.cursor.rowcount)
            return results
        except Exception as e:
            print('Error: failed to fetch data from sql: %s, 错误: %s' %
                  (self.sql, e))

    def queryByCodeno(self, tName, codeno):
        if len(tName) == 0:
            pass
        if len(codeno) == 0:
            pass

        self.sql = "select * from %s where codeno = '%s'" % (tName, codeno)

        try:
            self.cursor.execute(self.sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print('Error: failed to fetch data from table: 【%s】 and codeno: 【%s】, 错误: 【%s】' %
                  (tName, codeno, e))

    def queryLsjzByCodeno(self, codeno):
        if len(codeno) == 0:
            pass

        self.sql = "select fsrq, convert(dwjz, decimal(6, 4)) dwjz, convert(ljjz, decimal(6, 4)) ljjz, jzzzl from t_funds_lsjz where fundcode = '%s'" % codeno

        try:
            self.cursor.execute(self.sql)
            result = self.cursor.fetchall()

            self.cursor.close()
            self.conn.close()
            return result
        except Exception as e:
            print('Error: failed to fetch data from table: 【t_funds_lsjz】 and codeno: 【%s】, 错误: 【%s】' % (
                codeno, e))

    def queryByFundName(self, fName):
        pass

    def queryByTableName(self, tName):
        if len(tName) == 0:
            pass

        self.sql = "select * from %s" % tName

        try:
            self.cursor.execute(self.sql)
            results = self.cursor.fetchall()
            print('成功从表%s中获取数据%s条.' % (tName, self.cursor.rowcount))
            return results
        except Exception as e:
            print('Error: failed to fetch data from table: %s, 错误: %s' %
                  (tName, e))

    def save(self):
        pass

    def saveToTable(self, table, list):
        if len(table) == 0:
            pass
        if len(list) == 0:
            pass

        self.sql = "truncate table " + table
        # print(table)
        # print(list)

        try:
            self.cursor.execute(self.sql)
            print('成功清除表%s中的数据' % table)
        except Exception as e:
            print('清除表%s失败，错误%s' % (table, e))
        if table == 't_funds':
            self.sql = "insert into " + table + " values (%s, %s, %s)"
        elif table == 't_funds_lsjz':
            self.sql = "insert into " + table + \
                " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        try:
            self.cursor.executemany(self.sql, list)
            self.conn.commit()
            print('成功插入', self.cursor.rowcount, '条数据')
        except Exception as e:
            self.conn.rollback()
            print('事务处理失败', e)

    def close(self):
        self.cursor.close()
        self.conn.close()

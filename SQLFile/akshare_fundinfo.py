import akshare as ak
import pandas as pd
import sqlite3
"""
获取akshare的公募基金信息数据
注意请求频率，不要超过akshare的限制
"""

# 连接sqlite3数据库
conn = sqlite3.connect('./test_langchain.db') 

# 公募基金信息数据
fund_name_em_df = ak.fund_name_em()
# 保存公募基金信息数据在本地
df = pd.DataFrame(fund_name_em_df)
# 将公募基金信息数据写入sqlite3数据库
df.to_sql('FUND_INFO', conn, if_exists='replace', index=False)
df.to_excel('FUND_INFO.xlsx', index=False)
# 关闭数据库连接
conn.close()

df_read = pd.read_sql_query("SELECT * FROM FUND_INFO", conn)
print(df_read)
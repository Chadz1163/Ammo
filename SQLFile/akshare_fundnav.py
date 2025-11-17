import akshare as ak
import pandas as pd
import sqlite3
"""
获取akshare的开放式基金净值数据
注意请求频率，不要超过akshare的限制
"""

# 连接sqlite3数据库
conn = sqlite3.connect('./test_langchain.db') 

# 公募基金信息数据 混合型
df_read = pd.read_sql_query(""" SELECT 基金代码 FROM 
(SELECT 基金代码,substring(基金类型,5) AS 基金分类_level2
,ROW_NUMBER() over(PARTITION BY substring(基金类型,5) ORDER BY 基金代码 ASC) AS RN 
FROM FUND_INFO t WHERE t.基金类型 LIKE '混合型%'
) A 
WHERE A.RN <= 10 """, conn)

for x in df_read['基金代码']:
    # 开放式基金净值数据
    fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol=x, indicator="单位净值走势")
    # 保存开放式基金净值数据在本地
    df_fund_nav = pd.DataFrame(fund_open_fund_info_em_df)
    df_fund_nav['基金代码'] = x
    df_fund_nav = df_fund_nav[['净值日期','基金代码','单位净值','日增长率']]

    # 将公募基金信息数据写入sqlite3数据库
    df_fund_nav.to_sql('FUND_NAV', conn, if_exists='append', index=False)
    df_fund_nav.to_excel('FUND_NAV.xlsx', index=False)


# 关闭数据库连接
conn.close()
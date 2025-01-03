import requests
from bs4 import BeautifulSoup


def fetch_oil_price(address):

    # 动态构建URL，地址作为路径的一部分
    url = f"http://jiage.10260.com/youjia/{address}/"  # 根据传入的地址动态构建 URL

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=5)

    # 显式设置响应内容的编码为 GBK（针对国内网站的常见编码）
    response.encoding = 'gbk'

    response.raise_for_status()  # 检查请求是否成功

    soup = BeautifulSoup(response.text, 'html.parser')

    # cpbaojia标签存储油价信息
    exposition = soup.find("div", class_="cpbaojia")

    if not exposition:
        raise ValueError("未查询到油价信息")  # 未找到 class_ 为 cpbaojia 的父级元素

    # 找到包含油价的表格
    oil_price_table = exposition.find("table", width="98%")  # 通过宽度来定位表格，您可以根据实际情况修改选择器

    if not oil_price_table:
        raise ValueError("未找到油价表格")

    oil_prices = {}

    # 遍历表格中的所有行（跳过标题行）
    rows = oil_price_table.find_all("tr")[2:]
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 4:
            fuel_name = columns[0].get_text(strip=True)  # 油品名称（如：江苏92#汽油）
            price = columns[1].get_text(strip=True)  # 价格
            oil_prices[fuel_name] = price

    return oil_prices

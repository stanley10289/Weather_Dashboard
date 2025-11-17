import requests
import streamlit as st
import pandas as pd

st.title("🌦️ 台灣氣象資料 Dashboard")

# 您的授權碼已填入
API_KEY = "CWA-58ED05F5-0F62-4F5D-B0E4-E179C082CD7F"
LOCATION = st.selectbox("選擇城市", ["Taipei", "Taichung", "Kaohsiung"])

# 組合 API 網址
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={LOCATION}"
res = requests.get(url, verify=False)
data = res.json()

# 解析 JSON 資料
# 假設 data["records"]["location"] 是一個列表
location_list = data["records"]["location"]

if location_list: # 檢查列表是否非空
    location = location_list[0]
    # 在這裡繼續處理 location 數據
    print("成功獲取位置數據:", location)
else:
    # 處理列表為空的情況，可能是 API 沒有返回數據
    print("錯誤：API 返回的 'location' 列表是空的。")
    # 可以選擇給 location 一個預設值，或跳過後續操作
    location = None
st.subheader(f"📍 {location['locationName']} 36小時預報")

# 顯示天氣資訊
for element in location["weatherElement"]:
    name = element["elementName"]
    value = element["time"][0]["parameter"]["parameterName"]

    st.write(f"{name} : {value}")


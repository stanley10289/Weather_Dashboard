import requests
import streamlit as st
import pandas as pd

st.title("🌦️ 台灣氣象資料 Dashboard")

# 您的授權碼已填入
API_KEY = "CWA-58ED05F5-0F62-4F5D-B0E4-E179C082CD7F"
LOCATION = st.selectbox("選擇城市", ["Taipei", "Taichung", "Kaohsiung"])

# 組合 API 網址
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={LOCATION}"
res = requests.get(url)
data = res.json()

# 解析 JSON 資料
location = data["records"]["location"][0]
st.subheader(f"📍 {location['locationName']} 36小時預報")

# 顯示天氣資訊
for element in location["weatherElement"]:
    name = element["elementName"]
    value = element["time"][0]["parameter"]["parameterName"]
    st.write(f"{name} : {value}")
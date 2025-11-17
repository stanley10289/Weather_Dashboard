import requests
import streamlit as st
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 由於氣象署 API 的 SSL 憑證問題，我們禁用安全警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

st.title("🌦️ 台灣氣象資料 Dashboard")

# 您的授權碼已填入 (請務必保護您的金鑰)
API_KEY = "CWA-58ED05F5-0F62-4F5D-B0E4-E179C082CD7F"

# 讓使用者選擇城市
# 為了確保 API 能正確找到資料，這裡使用 API 預期的中文名稱
LOCATION_MAP = {
    "臺北市": "臺北市",
    "臺中市": "臺中市",
    "高雄市": "高雄市",
    "臺南市": "臺南市",
    "新北市": "新北市",
    "桃園市": "桃園市",
    "宜蘭縣": "宜蘭縣",
    "花蓮縣": "花蓮縣",
    "臺東縣": "臺東縣",
}
selected_location_name = st.selectbox("選擇城市", list(LOCATION_MAP.keys()))
location_param = LOCATION_MAP[selected_location_name]

# 組合 API 網址
# 數據集 F-C0032-001 提供縣市36小時天氣預報
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={location_param}"

# 嘗試發出請求，並禁用 SSL 驗證
# ⚠️ 注意: verify=False 會降低安全性，但這是為了解決氣象署 API 的憑證問題
res = requests.get(url, verify=False)

# --- 錯誤處理：檢查 API 請求狀態 ---
if res.status_code != 200:
    st.error(f"❌ API 請求失敗，狀態碼: {res.status_code}. 請檢查您的授權碼是否正確。")
    st.stop()

try:
    data = res.json()
except requests.exceptions.JSONDecodeError:
    st.error("❌ 無法解析 API 回應，伺服器可能返回了非 JSON 格式的錯誤。")
    st.stop()

# 檢查 API 返回的 'records' 和 'location' 數據結構是否存在
# 使用 .get() 避免 KeyError
records = data.get("records")
if not records:
    st.error("❌ API 回應格式錯誤或無效的 'records' 欄位。")
    st.stop()

location_list = records.get("location", [])

# --- 解決 IndexError 的關鍵步驟：檢查列表是否為空 (Line 17 修正) ---
if location_list:
    # 列表非空，安全地取出第一個元素 (這就是我們需要的城市數據)
    location = location_list[0]
else:
    # 列表為空，說明 API 找不到該城市數據
    st.error(f"❌ 找不到 {selected_location_name} 的預報資料。")
    st.stop()


# --- 成功取得數據後，顯示預報標題 (Line 29 修正) ---
# 這裡 location 確定是一個字典，不會出現 TypeError
st.subheader(f"📍 {location.get('locationName', selected_location_name)} 36小時預報")

# 準備顯示天氣資訊
weather_data = []

# 遍歷所有天氣元素
for element in location.get("weatherElement", []):
    name = element.get("elementName", "未知元素")
    
    # 假設我們只顯示第一個時間點的數據
    time_data = element.get("time", [{}])
    if time_data:
        parameter = time_data[0].get("parameter", {})
        value = parameter.get("parameterName", "N/A")
        description = parameter.get("parameterUnit", "")
        
        weather_data.append({
            "天氣元素": name,
            "預報值": f"{value} {description}",
        })

# 使用 DataFrame 顯示預報資訊，讓介面更美觀
if weather_data:
    df = pd.DataFrame(weather_data)
    # st.table(df) # table 比較簡單
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ 預報數據元素不完整。")

st.markdown(
    """
    ---
    <small>資料來源：交通部中央氣象署開放資料平台（F-C0032-001 鄉鎮天氣預報）。</small>
    """,
    unsafe_allow_html=True
)

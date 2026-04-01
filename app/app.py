import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. إعدادات الصفحة (شكل احترافي)
st.set_page_config(page_title="محلل عقارات التجمع وزايد", layout="wide", initial_sidebar_state="expanded")

# تصميم بسيط بالـ CSS لتحسين المظهر
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ منصة تحليل العقارات الذكية - أحمد السقا")
st.info("هذا التطبيق يحلل البيانات التي تم سحبها آلياً من مواقع العقارات في مصر.")

# 2. تحميل البيانات (بالمسار الصحيح)
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "..", "data", "scraped_realestate_data.csv")

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    # --- القائمة الجانبية (Sidebar) للفلاتر ---
    st.sidebar.header("🔍 فلاتر البحث الذكية")
    
    # فلتر المنطقة
    all_regions = df["Region"].unique()
    selected_regions = st.sidebar.multiselect("اختر المناطق:", options=all_regions, default=all_regions)
    
    # فلتر السعر (اللي بيكشف فرق التجمع وزايد)
    min_p, max_p = int(df["Price_EGP"].min()), int(df["Price_EGP"].max())
    price_range = st.sidebar.slider("حدد نطاق السعر (جنيه):", min_p, max_p, (min_p, max_p))

    # فلتر المساحة
    min_a, max_a = int(df["Area_m2"].min()), int(df["Area_m2"].max())
    area_range = st.sidebar.slider("حدد نطاق المساحة (م2):", min_a, max_a, (min_a, max_a))

    # تطبيق الفلاتر على الداتا
    mask = (df["Region"].isin(selected_regions)) & \
           (df["Price_EGP"].between(price_range[0], price_range[1])) & \
           (df["Area_m2"].between(area_range[0], area_range[1]))
    
    filtered_df = df[mask]

    # --- عرض أرقام سريعة (Metrics) ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("عدد الوحدات", len(filtered_df))
    col2.metric("متوسط السعر", f"{int(filtered_df['Price_EGP'].mean()):,} ج.م")
    col3.metric("متوسط المساحة", f"{int(filtered_df['Area_m2'].mean())} م2")
    col4.metric("سعر المتر التقريبي", f"{int(filtered_df['Price_per_m2'].mean()):,} ج")

    st.markdown("---")

    # --- الرسومات البيانية (التي كانت في dashboard.py) ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 توزيع الأسعار حسب المنطقة")
        fig1 = px.box(filtered_df, x="Region", y="Price_EGP", color="Region", points="all", template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("📈 العلاقة بين المساحة والسعر")
        fig2 = px.scatter(filtered_df, x="Area_m2", y="Price_EGP", color="Region", 
                         size="Rooms", hover_data=["Title"], template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    # --- عرض البيانات النهائية ---
    with st.expander("👁️ عرض جدول البيانات المفلترة"):
        st.dataframe(filtered_df.sort_values("Price_EGP", ascending=False), use_container_width=True)

    # زر تحميل البيانات
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 تحميل البيانات المفلترة (Excel/CSV)", data=csv, file_name='filtered_data.csv', mime='text/csv')

else:
    st.error("❌ ملف البيانات غير موجود في فولدر data. يرجى تشغيل السكرابر أولاً.")
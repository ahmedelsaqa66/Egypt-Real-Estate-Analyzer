import pandas as pd
import plotly.express as px
import os

# 1. تحميل البيانات
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "..", "data", "scraped_realestate_data.csv")

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print("✅ تم تحميل البيانات بنجاح.. جاري رسم الداشبورد!")
    
    # --- الرسمة الأولى: مقارنة متوسط سعر المتر بين المناطق ---
    avg_price = df.groupby('Region')['Price_per_m2'].mean().reset_index()
    fig1 = px.bar(avg_price, x='Region', y='Price_per_m2', 
                 title='متوسط سعر المتر: التجمع vs زايد',
                 color='Region',
                 labels={'Price_per_m2': 'متوسط سعر المتر (جنيه)'})
    fig1.show()

    # --- الرسمة الثانية: العلاقة بين المساحة والسعر (Scatter Plot) ---
    fig2 = px.scatter(df, x='Area_m2', y='Price_EGP', 
                     color='Region', 
                     size='Rooms',
                     hover_data=['Title'],
                     title='توزيع الأسعار حسب المساحة وعدد الغرف')
    fig2.show()

else:
    print("❌ الملف مش موجود، اتأكد إنك شغلت الـ Scraper الأول!")
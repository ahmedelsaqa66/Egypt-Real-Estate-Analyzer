import pandas as pd
import random
import os

def generate_market_data():
    """
    دالة لتوليد بيانات عقارية واقعية لسوق التجمع وزايد 
    عشان نبدأ شغل التحليل والداشبورد فوراً
    """
    data = []
    regions = ["Tagamoa", "Sheikh Zayed"]
    titles = [
        "Apartment for sale in Prime Location", 
        "Luxury Apartment with View", 
        "Modern Studio", 
        "Family House near Services",
        "Finished Apartment for Sale"
    ]
    
    print("🚀 جاري تجهيز بيانات السوق العقاري...")

    # توليد 100 وحدة عقارية (50 لكل منطقة)
    for _ in range(100):
        region = random.choice(regions)
        
        # أسعار ومساحات منطقية للسوق المصري حالياً
        if region == "Tagamoa":
            price = random.randint(4000000, 15000000)
            size = random.randint(120, 300)
        else: # الشيخ زايد
            price = random.randint(3000000, 11000000)
            size = random.randint(100, 250)
            
        rooms = random.randint(2, 4)
        baths = random.randint(1, 3)
        
        # حساب سعر المتر
        price_per_m2 = round(price / size, 2)
        
        data.append({
            'Title': f"{random.choice(titles)} - {region}",
            'Price_EGP': price,
            'Area_m2': size,
            'Price_per_m2': price_per_m2,
            'Rooms': int(rooms),
            'Baths': int(baths),
            'Region': region
        })
    
    return pd.DataFrame(data)

def save_data(df):
    """حفظ البيانات في المسار الصحيح وتجنب أخطاء الفولدرات"""
    # تحديد مسار الفولدر الرئيسي (بره scripts)
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, "..", "data")

    # إنشاء الفولدر لو مش موجود
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"📂 تم إنشاء فولدر جديد: {data_dir}")

    # حفظ الملف
    file_path = os.path.join(data_dir, "scraped_realestate_data.csv")
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    
    print("-" * 40)
    print(f"✅ تم بنجاح! الملف جاهز هنا: \n{file_path}")
    print(f"📊 إجمالي الوحدات: {len(df)}")
    print("-" * 40)

if __name__ == "__main__":
    # 1. توليد الداتا
    df_final = generate_market_data()
    
    # 2. حفظ الداتا
    save_data(df_final)
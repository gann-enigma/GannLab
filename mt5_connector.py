import MetaTrader5 as mt5
import os

# --- ضریب خود را اینجا تنظیم کنید ---
# برای ضرب در ۱۰ از 10.0، برای تقسیم بر ۱۰ از 0.1 و غیره استفاده کنید
OUTPUT_FACTOR = 1.0

def send_levels_to_mt5(price_levels, factor):
    """
    این تابع لیستی از قیمت‌ها را گرفته، آنها را در ضریب ضرب کرده و در فایلی می‌نویسد
    که اندیکاتور متاتریدر بتواند بخواند.
    """
    if not mt5.initialize():
        print("اتصال به ترمینال متاتریدر ۵ برقرار نشد. لطفاً از باز بودن آن اطمینان حاصل کنید.")
        mt5.shutdown()
        return

    # اعمال ضریب مقیاس‌دهی به هر سطح قیمت
    scaled_levels = [level * factor for level in price_levels]

    data_path = mt5.terminal_info().data_path
    file_path = os.path.join(data_path, "MQL5", "Files", "gann_levels.csv")
    
    try:
        with open(file_path, 'w') as f:
            for level in scaled_levels:
                f.write(f"{level}\n")
        print(f"موفقیت: {len(scaled_levels)} سطح مقیاس‌دهی شده به متاتریدر ارسال شد.")
        print("اعداد اصلی:", price_levels)
        print("اعداد مقیاس‌دهی شده:", scaled_levels)
    except Exception as e:
        print(f"خطا: امکان نوشتن در فایل وجود نداشت. {e}")
    
    mt5.shutdown()


# --- اعداد هدف کپی شده خود را اینجا قرار دهید ---
if __name__ == "__main__":
    # مثال: اگر برنامه مربع گن شما اعداد 64, 81, 100 را محاسبه کرده است
    target_prices = [3990.0, 4000, 4010.0] 

    if not target_prices:
        print("لیست 'target_prices' خالی است. لطفاً اعداد محاسبه شده را وارد کنید.")
    else:
        send_levels_to_mt5(target_prices, OUTPUT_FACTOR)
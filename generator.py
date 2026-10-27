import os
import subprocess
import shutil
from jinja2 import Environment, FileSystemLoader

def find_edge_path():
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge")
    ]
    for path in paths:
        if path and os.path.exists(path):
            return path
    raise FileNotFoundError("Microsoft Edge browser nahi mila.")

def render_document_pdf(data: dict, mode: str = "physical_stamp", output_filename: str = "document.pdf"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("base_document.html")
    
    # Physical Stamp Paper: 3.4 inches space for government note/stamp
    # E-Stamp Paper: 0.6 inches margin
    top_margin = "3.4in" if mode == "physical_stamp" else "0.6in"
    
    rendered_html = template.render(
        doc_title=data.get("title"),
        top_margin=top_margin,
        party1=data.get("party1"),
        party2=data.get("party2"),
        clauses=data.get("clauses", []),
        date_urdu=data.get("date_urdu", "23 اکتوبر 2026ء")
    )
    
    os.makedirs("output", exist_ok=True)
    temp_html_path = os.path.abspath("output/temp_render.html")
    pdf_out_path = os.path.abspath(os.path.join("output", output_filename))
    
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    edge_path = find_edge_path()
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--prefer-css-page-size",
        f"--print-to-pdf={pdf_out_path}",
        f"file:///{temp_html_path}"
    ]
    
    subprocess.run(cmd, check=True)
    
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)
        
    print(f"Kamyabi se PDF generate ho gayi: {pdf_out_path}")
    return pdf_out_path

if __name__ == "__main__":
    # Asal Kachehri Data (Mukammal Tafseelat o Hadood Arba'a)
    batwara_data = {
        "title": "اقرار نامہ تقسیمِ جائیداد غیر منقولہ بحصہ مساوی (پورشن وائز)",
        "date_urdu": "23 اکتوبر 2026ء",
        "party1": {
            "name": "محمد احمد خان",
            "father_name": "عبدالرشید خان مرحوم",
            "cnic": "37405-1111111-1",
            "address": "مکان نمبر 45، گلی نمبر 3، سیکٹر ایف سکس، اسلام آباد",
            "role": "فریق اول / قابض گراؤنڈ فلور"
        },
        "party2": {
            "name": "محمد طارق خان",
            "father_name": "عبدالرشید خان مرحوم",
            "cnic": "37405-2222222-2",
            "address": "مکان نمبر 45، گلی نمبر 3، سیکٹر ایف سکس، اسلام آباد",
            "role": "فریق دوم / قابض فرسٹ فلور"
        },
        "clauses": [
            "یہ کہ فریقین آپس میں سگے بھائی ہیں اور مکان واقع پلاٹ نمبر 45، گلی نمبر 3، سیکٹر ایف سکس، اسلام آباد، جس کا کل رقبہ 500 مربع گز ہے، کے اپنے والد مرحوم عبدالرشید خان کے بلا شرکت غیرے اکلوتے شرعی و قانونی وارثان ہیں۔",
            "یہ کہ باہمی رضامندی، خاندانی تصفیہ اور روبرو گواہان کے فیصلے کے تحت فریق اول کو مکان کا مکمل گراؤنڈ فلور مع گیراج، فرنٹ لان، اور پچھلا صحن دے دیا گیا ہے جس کا حدود اربعہ: مشرق گلی عام، مغرب مکان نمبر 46، شمال پلاٹ نمبر 44، اور جنوب مین روڈ ہے۔ اس پر فریق اول کا بلا شرکت غیرے قبضہ و تصرف تسلیم کیا جاتا ہے۔",
            "یہ کہ فریق دوم کو مکان کی بالائی منزل (فرسٹ فلور) مع علیحدہ داخلی راستہ، سیڑھیاں اور چھت کے مکمل ملکیتی حقوق دیے گئے ہیں۔ چھت پر پانی کی ٹینکی کی صفائی اور مرمت کے لیے فریق اول کو باہمی اطلاع کے بعد معقول رسائی حاصل ہوگی۔",
            "یہ کہ بجلی کے دو الگ الگ میٹرز (میٹر نمبر 1 برائے گراؤنڈ فلور اور میٹر نمبر 2 برائے فرسٹ فلور) فریقین اپنے اپنے نام پر منتقل کروانے کے پابند ہوں گے اور بلز کی بروقت ادائیگی اپنے اپنے استعمال کے مطابق خود کریں گے۔",
            "یہ کہ سرکاری بقایاجات، واٹر سپلائی ٹیکس، پراپرٹی ٹیکس اور سوئی گیس کے بلز کی ذمہ داری دونوں فریقین پر نصف نصف (50-50%) عائد ہوگی۔",
            "یہ کہ فریقین میں سے کوئی بھی فریق اگر مستقبل میں اپنا پورشن فروخت کرنا چاہے تو وہ پہلے دوسرے بھائی کو خریدنے کی پیشکش کرے گا (حقِ شفع)۔ خاندانی رضامندی کے بغیر کسی غیر شخص یا اجنبی کو فروخت کرنے کی قطعاً اجازت نہ ہوگی۔",
            "یہ کہ آئندہ فریقین یا ان کے ورثاء میں سے کوئی فریق اس تقسیم کے خلاف کسی بھی سول کورٹ، ریونیو کورٹ یا تھانے میں کوئی عذرداری یا دعویٰ دائر نہیں کرے گا، اور دائر شدہ دعویٰ باطل و کالعدم تصور ہوگا۔"
        ]
    }
    
    render_document_pdf(batwara_data, mode="physical_stamp", output_filename="batwara_stamp.pdf")
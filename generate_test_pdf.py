import os
import subprocess
import shutil

def find_edge_path():
    """Windows par Microsoft Edge ka path talash karta hai"""
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge")
    ]
    for path in paths:
        if path and os.path.exists(path):
            return path
    raise FileNotFoundError("Microsoft Edge browser nahi mila.")

def create_legal_document(mode="physical_stamp"):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    html_filename = os.path.join(output_dir, f"temp_{mode}.html")
    pdf_filename = os.path.abspath(os.path.join(output_dir, f"test_{mode}.pdf"))
    
    # Margin logic:
    # Physical Stamp Paper: 3.8 inches top margin (note ke neechay print hone ke liye)
    # E-Stamp Paper: 0.8 inches top margin (full page)
    top_margin = "3.8in" if mode == "physical_stamp" else "0.8in"
    
    html_content = f"""<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
        
        @page {{
            size: A4 portrait;
            margin-top: {top_margin};
            margin-bottom: 0.8in;
            margin-left: 0.8in;
            margin-right: 0.8in;
        }}
        
        body {{
            font-family: 'Noto Nastaliq Urdu', 'Urdu Nastaliq', serif;
            direction: rtl;
            text-align: justify;
            font-size: 14pt;
            line-height: 2.4;
            color: #000;
        }}
        
        h1 {{
            text-align: center;
            font-size: 22pt;
            margin-bottom: 25px;
            font-weight: 700;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
            width: 60%;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .clause {{
            margin-bottom: 16px;
        }}
        
        .signatures {{
            margin-top: 50px;
            display: flex;
            justify-content: space-between;
            font-size: 13pt;
        }}
        
        .sig-box {{
            width: 45%;
            text-align: center;
            border-top: 1px dotted #000;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>اقرار نامہ کرایہ داری</h1>
    
    <div class="clause">
        منکہ مسمی <strong>علی خان</strong> ولد محمد خان، شناختی کارڈ نمبر <code>37405-1234567-1</code>، ساکن مکان نمبر 12، جی ٹین، اسلام آباد۔ (جو کہ بعد میں <strong>فریق اول / مالک مکان</strong> کہلائے گا)
    </div>
    
    <div class="clause">
        اور مسمی <strong>عثمان احمد</strong> ولد نذیر احمد، شناختی کارڈ نمبر <code>37405-7654321-1</code>، ساکن راولپنڈی۔ (جو کہ بعد میں <strong>فریق دوم / کرایہ دار</strong> کہلائے گا)
    </div>
    
    <div class="clause">
        یہ کہ فریق اول نے اپنا مکان واقع مکان نمبر 12، اسٹریٹ 4، جی ٹین، اسلام آباد، فریق دوم کو مبلغ <strong>45,000 روپے</strong> ماہوار پر کرایہ پر دینے کا اقرar کیا ہے۔
    </div>
    
    <div class="clause">
        یہ کہ کرایہ کی مدت ایک سال یعنی 11 ماہ کے لیے مقرر کی جاتی ہے جو کہ باہمی رضامندی سے قابل تجدید ہو گی۔
    </div>
    
    <div class="clause">
        یہ کہ فریق دوم نے مبلغ <strong>90,000 روپے</strong> بطور سیکیورٹی ایڈوانس فریق اول کو ادا کر دیے ہیں، جو کہ مکان خالی کرنے پر قابل واپسی ہوں گے۔
    </div>

    <div class="signatures">
        <div class="sig-box">
            دستخط فریق اول (مالک مکان)<br><br>
            ______________________
        </div>
        <div class="sig-box">
            دستخط فریق دوم (کرایہ دار)<br><br>
            ______________________
        </div>
    </div>
</body>
</html>
"""
    
    # Save temporary HTML file
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    edge_path = find_edge_path()
    html_abs_path = os.path.abspath(html_filename)
    
    # Headless Edge se print to PDF
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_filename}",
        f"file:///{html_abs_path}"
    ]
    
    subprocess.run(cmd, check=True)
    
    # Cleanup temp HTML
    if os.path.exists(html_filename):
        os.remove(html_filename)
        
    print(f"Kamyabi se PDF tayyar ho gayi: {pdf_filename}")

if __name__ == "__main__":
    print("Generating Physical Stamp PDF (3.8 inch Top Margin)...")
    create_legal_document(mode="physical_stamp")
    
    print("Generating E-Stamp PDF (Full Page)...")
    create_legal_document(mode="e_stamp")
    print("\nSab PDFs tayyar hain! Browser mein refresh karke check karein.")
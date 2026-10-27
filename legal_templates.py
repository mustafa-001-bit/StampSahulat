# legal_templates.py
# Comprehensive Legal Documents Library for StampSahulat.com

LEGAL_TEMPLATES = {
    # =========================================================================
    # 1. REAL ESTATE & PROPERTY (خرید و فروخت و جائیداد)
    # =========================================================================
    "bayana_property": {
        "category_ur": "خرید و فروخت جائیداد",
        "category_en": "Property & Real Estate",
        "title_ur": "اقرار نامہ بیعانہ جائیداد (مکان / پلاٹ / زمین)",
        "title_en": "Earnest Money Agreement (Bayana Deed for Property)",
        "party1_role_ur": "فروشندہ (مالک)",
        "party1_role_en": "Seller / Vendor",
        "party2_role_ur": "خریدار",
        "party2_role_en": "Purchaser / Buyer",
        "fields": [
            {"id": "property_address", "label_ur": "جائیداد کا مکمل پتہ و رقبہ", "label_en": "Property Address & Area", "default": "پلاٹ نمبر 12، گلی نمبر 4، سیکٹر جی-11، اسلام آباد، رقبہ 5 مرلہ"},
            {"id": "total_price", "label_ur": "کل طے شدہ قیمت (روپے)", "label_en": "Total Sale Consideration (PKR)", "default": "15,000,000"},
            {"id": "bayana_amount", "label_ur": "ادا شدہ بیعانہ رقم (روپے)", "label_en": "Earnest Money Paid (PKR)", "default": "2,000,000"},
            {"id": "remaining_amount", "label_ur": "بقیہ واجب الادا رقم (روپے)", "label_en": "Balance Amount (PKR)", "default": "13,000,000"},
            {"id": "final_payment_date", "label_ur": "بقیہ رقم و رجسٹری کی آخری تاریخ", "label_en": "Final Payment & Transfer Deadline", "default": "30 دسمبر 2026ء"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول مذکورہ جائیداد واقع {property_address} کا مکمل، بااختیار اور بلا شرکت غیرے قانونی مالک و قابض ہے اور یہ جائیداد ہر قسم کے تنازعات، رہن، بار اور عدالتی سٹے آرڈر سے بالکل پاک و صاف ہے۔",
            "یہ کہ فریق اول نے مذکورہ جائیداد کا سودا فریق دوم کے ساتھ کل مبلغ {total_price} روپے میں طے کیا ہے، جس کے عوض فریق اول نے مبلغ {bayana_amount} روپے بطور بیعانہ فریق دوم سے روبرو گواہان وصول پا کر رسید جاری کر دی ہے۔",
            "یہ کہ بقیہ رقم مبلغ {remaining_amount} روپے فریق دوم مورخہ {final_payment_date} تک فریق اول کو ادا کرنے کا پابند ہوگا۔",
            "یہ کہ بقیہ رقم کی مکمل ادائیگی کے ساتھ ہی فریق اول متعلقہ رجسٹرار آفس یا ہاؤسنگ سوسائٹی میں فریق دوم کے نام پر قانونی رجسٹری / ٹرانسفر کروانے اور اصل رجسٹری و فرد سمیت خالی موقع کا قبضہ حوالے کرنے کا پابند ہوگا۔",
            "یہ کہ اگر فریق اول مقررہ تاریخ تک رجسٹری کروانے سے انکار کرے تو فریق دوم کو عدالت مجاز سے تعمیلِ مختص (Specific Performance) کے ذریعے یکطرفہ ٹرانسفر حاصل کرنے اور دگنا بیعانہ مع ہرجانہ وصول کرنے کا مکمل قانونی حق حاصل ہوگا۔"
        ],
        "clauses_en": [
            "That the First Party is the absolute, lawful owner and in peaceful possession of the property situated at {property_address}, which is free from all encumbrances, mortgages, liens, or court litigation.",
            "That the First Party has agreed to sell the said property to the Second Party for a total sale consideration of PKR {total_price}/-, against which earnest money (Bayana) of PKR {bayana_amount}/- has been received in presence of attesting witnesses.",
            "That the balance sale consideration amounting to PKR {remaining_amount}/- shall be paid by the Second Party on or before {final_payment_date}.",
            "That upon full payment of the balance amount, the First Party shall execute the registered sale deed/transfer in the relevant Registrar office or Housing Society and hand over physical possession along with original title documents.",
            "That in case of breach by the First Party, the Second Party shall have the unconditional legal right to enforce Specific Performance through the Civil Court along with damages."
        ]
    },

    "mukammal_farokht_property": {
        "category_ur": "خرید و فروخت جائیداد",
        "category_en": "Property & Real Estate",
        "title_ur": "اقرار نامہ بیع قطعی و حوالگی قبضہ (مکمل موقع پر خریداری)",
        "title_en": "Absolute Sale & Immediate Possession Handover Deed",
        "party1_role_ur": "فروشندہ (سابقہ مالک)",
        "party1_role_en": "Seller / Previous Owner",
        "party2_role_ur": "خریدار (نیا مالک)",
        "party2_role_en": "Purchaser / Absolute Owner",
        "fields": [
            {"id": "property_address", "label_ur": "جائیداد کا پتہ، خسرہ / کھاتہ نمبر و رقبہ", "label_en": "Full Property Particulars & Area", "default": "مکان نمبر 45، گلی نمبر 3، سیکٹر ایف-8/1، اسلام آباد، رقبہ 10 مرلہ"},
            {"id": "full_paid_amount", "label_ur": "کل وصول شدہ رقم بیع (روپے)", "label_en": "Total Received Consideration (PKR)", "default": "35,000,000"},
            {"id": "payment_mode", "label_ur": "ادائیگی کا طریقہ (بینک ڈرافٹ / چیک / کیش)", "label_en": "Mode of Payment (Pay Order / Cheque)", "default": "پے آرڈر نمبر 09876541 بینک الفلاح اسلام آباد"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول نے اپنی ملکیت و ملکیتی جائیداد مندرجہ بالا واقع {property_address} کو معہ تمام حقوقِ ملکیت، راستہ، بجلی، گیس و پانی کنکشنز کل مبلغ {full_paid_amount} روپے کے عوض فریق دوم کے ہاتھ قطعی و حتمی طور پر فروخت کر دی ہے۔",
            "یہ کہ فریق اول نے کل زرِ بیعانہ و ثمن مبلغ {full_paid_amount} روپے بذریعہ {payment_mode} فریق دوم سے بلا کم و کاست وصول پا لیا ہے اور اب فریق اول کا کوئی مطالبہ یا لین دین باقی نہ رہا ہے۔",
            "یہ کہ فریق اول نے موقع پر جائیداد کا خالی و پرامن قبضہ فریق دوم کے حوالے کر دیا ہے اور تمام اصل ملکیتی دستاویزات، فرد، سابقہ بیع نامہ جات اور این او سی فریق دوم کے سپرد کر دیے ہیں۔",
            "یہ کہ آج کے بعد فریق دوم مذکورہ جائیداد کا مالکِ کامل و بااختیار ہے اور وہ اسے اپنے نام رجسٹر کروانے، تعمیر کرنے یا آگے فروخت کرنے کا مکمل قانونی حق رکھتا ہے۔",
            "یہ کہ اگر آئندہ کبھی اس جائیداد کے حقِ ملکیت میں کوئی قانونی نقص، وراثتی دعویٰ یا مالیاتی تنازعہ سامنے آیا تو اس کے تمام نقصانات اور ہرجانے کا مکمل ذمہ دار فریق اول ذاتی حیثیت میں ہوگا۔"
        ],
        "clauses_en": [
            "That the First Party has sold, transferred, and conveyed all rights, title, interest, and easements of the property located at {property_address} to the Second Party absolutely and forever against total sale consideration of PKR {full_paid_amount}/-.",
            "That the First Party acknowledges receipt of the entire sale consideration of PKR {full_paid_amount}/- via {payment_mode} without any deduction, leaving zero financial liability outstanding.",
            "That actual physical and peaceful vacant possession has been handed over on the spot to the Second Party along with all original title deeds, allotment letter, and utility clearance receipts.",
            "That henceforth the Second Party is the absolute lawful owner of the property with full legal rights to register, transfer, alienate, or construct upon the said premises.",
            "That the First Party covenants that if any defect in title, encumbrance, or inheritance claim arises in future, the First Party shall indemnify and hold the Second Party harmless against all losses."
        ]
    },

    # =========================================================================
    # 2. TENANCY & COMMERCIAL LEASES (کرایہ داری و کمرشل لیز)
    # =========================================================================
    "kirayanama_plaza_hall": {
        "category_ur": "کرایہ داری و کمرشل لیز",
        "category_en": "Tenancy & Commercial Leases",
        "title_ur": "معاہدہ کرایہ داری کمرشل پلازہ / ہال / فلور",
        "title_en": "Commercial Plaza Hall / Whole Floor Lease Deed",
        "party1_role_ur": "مالک پلازہ / فریق اول",
        "party1_role_en": "Plaza Owner / Lessor",
        "party2_role_ur": "کرایہ دار / فریق دوم",
        "party2_role_en": "Tenant / Commercial Lessee",
        "fields": [
            {"id": "plaza_details", "label_ur": "پلازہ کا نام، فلور / ہال نمبر و رقبہ", "label_en": "Plaza Name, Floor/Hall No & Covered Area", "default": "الرحمان کمرشل سینٹر، دوسری منزل، مکمل اوپن ہال، رقبہ 3500 مربع فٹ، بلیو ایریا اسلام آباد"},
            {"id": "monthly_rent", "label_ur": "ماہانہ کرایہ (روپے)", "label_en": "Monthly Rent (PKR)", "default": "350,000"},
            {"id": "security_deposit", "label_ur": "سیکیورٹی ایڈوانس رقم (روپے)", "label_en": "Security Deposit Advance (PKR)", "default": "1,500,000"},
            {"id": "lease_period", "label_ur": "مدتِ کرایہ داری", "label_en": "Lease Tenancy Period", "default": "3 سال (36 ماہ)"},
            {"id": "annual_increase", "label_ur": "سالانہ کرایہ اضافہ شرح (%)", "label_en": "Annual Rent Escalation (%)", "default": "10%"},
            {"id": "business_nature", "label_ur": "کاروبار کی نوعیت / سرگرمی", "label_en": "Nature of Business / Office Use", "default": "سافٹ ویئر ہاؤس و آئی ٹی کارپوریٹ آفس"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول نے کمرشل پلازہ واقع {plaza_details} فریق دوم کو برائے استعمال {business_nature} بحساب ماہوار کرایہ مبلغ {monthly_rent} روپے کرایہ پر دے دیا ہے۔",
            "یہ کہ مدت کرایہ داری کل {lease_period} کے لیے مقرر کی گئی ہے، اور ہر سال کے اختتام پر ماہوار کرایہ میں {annual_increase} خودکار اضافہ لاگو ہوگا۔",
            "یہ کہ فریق دوم نے مبلغ {security_deposit} روپے بطور سیکیورٹی ڈپازٹ (غیر سودی امانت) فریق اول کے پاس جمع کروا دیا ہے جو کہ خالی کرنے کے وقت کلیئرنس کے بعد قابلِ واپسی ہوگا۔",
            "یہ کہ فریق دوم ہر ماہ کا کرایہ 10 تاریخ تک ادا کرے گا، نیز ہال کا بجلی بل، گیس بل، کمرشل جنریٹر چارجز اور پلازہ بلڈنگ کی مینٹیننس فیس خود ادا کرنے کا پابند ہوگا۔",
            "یہ کہ فریق دوم مذکورہ ہال / فلور کو کسی تیسرے فریق کو سب لیٹ (Sublet) نہیں کرے گا، اور کوئی بھی عارضی پارٹیشن فریق اول کی پیشگی تحریری اجازت کے بعد کر سکے گا۔",
            "یہ کہ کسی بھی فریق کی جانب سے معاہدہ وقت سے پہلے ختم کرنے کی صورت میں دوسرے فریق کو کم از کم 2 ماہ کا پیشگی تحریری نوٹس دینا لازمی ہوگا۔"
        ],
        "clauses_en": [
            "That the Lessor leases out the commercial premises situated at {plaza_details} to the Lessee for the lawful purpose of {business_nature} at a monthly rental of PKR {monthly_rent}/-.",
            "That the lease tenure shall strictly be {lease_period}, with an agreed annual rent escalation of {annual_increase} applicable at the expiration of each 12-month period.",
            "That the Lessee has deposited an interest-free refundable security deposit of PKR {security_deposit}/- with the Lessor, refundable upon peaceful vacation after settling dues.",
            "That the monthly rent shall be payable by the 10th of each calendar month; utility bills (electricity, commercial generator backup, water, maintenance) shall be paid directly by the Lessee.",
            "That the Lessee shall not sublet, assign, or create third-party rights on any portion of the leased floor/hall without prior written approval of the Lessor.",
            "That either party wishing to terminate this commercial lease prior to expiry shall serve a mandatory 2-month prior written notice."
        ]
    },

    "kirayanama_commercial_dukan": {
        "category_ur": "کرایہ داری و کمرشل لیز",
        "category_en": "Tenancy & Commercial Leases",
        "title_ur": "معاہدہ کرایہ داری کمرشل دکان / دفتر",
        "title_en": "Commercial Shop / Retail Office Tenancy Deed",
        "party1_role_ur": "مالک دکان",
        "party1_role_en": "Shop Landlord",
        "party2_role_ur": "کرایہ دار",
        "party2_role_en": "Commercial Tenant",
        "fields": [
            {"id": "shop_address", "label_ur": "دکان کا نمبر، مارکیٹ و مکمل پتہ", "label_en": "Shop No, Market & Location", "default": "دکان نمبر 14، رحمان پلازہ، مین مارکیٹ جی-9، اسلام آباد"},
            {"id": "monthly_rent", "label_ur": "ماہوار کرایہ (روپے)", "label_en": "Monthly Rent (PKR)", "default": "45,000"},
            {"id": "advance_amount", "label_ur": "سیکیورٹی ایڈوانس رقم (روپے)", "label_en": "Security Advance Deposit (PKR)", "default": "250,000"},
            {"id": "duration", "label_ur": "مدت کرایہ داری", "label_en": "Duration", "default": "11 ماہ"},
            {"id": "annual_increment", "label_ur": "سالانہ اضافہ شرح (%)", "label_en": "Annual Increment (%)", "default": "10%"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول نے اپنی ملکیت واقع {shop_address} فریق دوم کو بغرضِ کاروبار بحساب ماہانہ کرایہ مبلغ {monthly_rent} روپے کرایہ پر دی ہے۔",
            "یہ کہ فریق دوم نے مبلغ {advance_amount} روپے بطور سیکیورٹی ڈپازٹ فریق اول کو ادا کر دیے ہیں جو معاہدہ کے اختتام پر دکان کے بقایا جات کلیئر کر کے واپس ہوں گے۔",
            "یہ کہ کرایہ داری کی کل مدت {duration} ہوگی اور تجدید کی صورت میں کرایہ میں {annual_increment} سالانہ اضافہ ہوگا۔",
            "یہ کہ فریق دوم دکان کا کرایہ ہر انگریزی مہینے کی 5 تاریخ تک ادا کرنے اور بجلی کا بل خود ادا کرنے کا پابند ہوگا۔",
            "یہ کہ دکان خالی کرنے یا کروانے کی صورت میں فریقین ایک ماہ قبل تحریری نوٹس دینے کے پابند ہوں گے۔"
        ],
        "clauses_en": [
            "That the Landlord lets out commercial shop located at {shop_address} to the Tenant against a monthly rent of PKR {monthly_rent}/-.",
            "That the Tenant has deposited PKR {advance_amount}/- as refundable security deposit with the Landlord.",
            "That the tenancy term shall be {duration}, subject to renewal with {annual_increment} annual increment.",
            "That the Tenant shall pay rent by the 5th of each month and bear independent commercial electricity bills.",
            "That either party may vacate or demand vacation by serving 1-month prior written notice."
        ]
    },

    "kirayanama_makan": {
        "category_ur": "کرایہ داری و کمرشل لیز",
        "category_en": "Tenancy & Commercial Leases",
        "title_ur": "معاہدہ کرایہ داری رہائشی مکان / فلیٹ",
        "title_en": "Residential House / Apartment Tenancy Agreement",
        "party1_role_ur": "مالک مکان",
        "party1_role_en": "Landlord",
        "party2_role_ur": "کرایہ دار",
        "party2_role_en": "Tenant",
        "fields": [
            {"id": "property_address", "label_ur": "مکان / فلیٹ کا مکمل پتہ", "label_en": "House / Flat Address", "default": "مکان نمبر 102، سٹریٹ 15، سیکٹر آئی-8/2، اسلام آباد"},
            {"id": "rent_amount", "label_ur": "ماہوار کرایہ (روپے)", "label_en": "Monthly Rent (PKR)", "default": "60,000"},
            {"id": "advance_deposit", "label_ur": "سیکیورٹی ایڈوانس رقم (روپے)", "label_en": "Security Advance (PKR)", "default": "120,000"},
            {"id": "tenancy_period", "label_ur": "مدت کرایہ داری", "label_en": "Tenancy Period", "default": "11 ماہ"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول نے مذکورہ رہائشی مکان واقع {property_address} فریق دوم کو بغرض رہائش ماہوار کرایہ مبلغ {rent_amount} روپے پر دیا ہے۔",
            "یہ کہ فریق دوم نے مبلغ {advance_deposit} روپے بطور سیکیورٹی ڈپازٹ فریق اول کے حوالے کر دیا ہے جو کہ مکان خالی کرنے کے وقت واپس ہوگی۔",
            "یہ کہ مدت کرایہ داری {tenancy_period} ہوگی، جس کی توسیع باہمی تحریری رضامندی سے ممکن ہوگی۔",
            "یہ کہ فریق دوم بجلی، سوئی گیس اور پانی کے تمام ماہانہ بل خود ادا کر کے اصل پیڈ رسیدیں فریق اول کو دکھانے کا پابند ہوگا۔",
            "یہ کہ مکان صرف اور صرف ذاتی خاندانی رہائش کے لیے استعمال ہوگا، کسی تجارتی، غیر قانونی یا غیر اخلاقی سرگرمی کی قطعی ممانعت ہوگی۔"
        ],
        "clauses_en": [
            "That the Landlord rents out residential house situated at {property_address} to the Tenant for residential family purpose at PKR {rent_amount}/- per month.",
            "That the Tenant has furnished an interest-free refundable security deposit of PKR {advance_deposit}/- to the Landlord.",
            "That the tenancy duration is {tenancy_period}, extendable only through mutual written consent.",
            "That the Tenant shall clear electricity, gas, and water bills on regular monthly basis.",
            "That the premises shall solely be utilized for peaceful domestic family accommodation."
        ]
    },

    # =========================================================================
    # 3. BUSINESS, PARTNERSHIPS & SERVICES (کاروبار، شراکت داری و سروسز)
    # =========================================================================
    "partnership_deed": {
        "category_ur": "کاروبار و شراکت داری",
        "category_en": "Business & Partnerships",
        "title_ur": "شراکت نامہ کاروبار (2 یا 3 پارٹنرز باہمی شراکت)",
        "title_en": "Partnership Deed (Multi-Partner Business Agreement)",
        "party1_role_ur": "پارٹنر اول (منیجنگ پارٹنر)",
        "party1_role_en": "First Partner / Managing Partner",
        "party2_role_ur": "پارٹنر دوم / سوم",
        "party2_role_en": "Second / Third Partner",
        "fields": [
            {"id": "firm_name", "label_ur": "کاروبار / فرم کا نام", "label_en": "Firm / Business Name", "default": "المدینہ ٹریڈرز اینڈ ڈسٹری بیوٹرز"},
            {"id": "business_address", "label_ur": "کاروبار کا پرنسپل آفس پتہ", "label_en": "Principal Office Address", "default": "دکان نمبر 12، کمرشل مارکیٹ راولپنڈی"},
            {"id": "total_capital", "label_ur": "کل لگایا گیا مشترکہ سرمایہ (روپے)", "label_en": "Total Invested Capital (PKR)", "default": "3,000,000"},
            {"id": "p1_share", "label_ur": "پارٹنر اول سرمایہ و منافع شرح (%)", "label_en": "Partner 1 Capital & Profit Share (%)", "default": "50%"},
            {"id": "p2_share", "label_ur": "پارٹنر دوم سرمایہ و منافع شرح (%)", "label_en": "Partner 2 Capital & Profit Share (%)", "default": "50%"},
            {"id": "bank_operation", "label_ur": "بینک اکاؤنٹ آپریٹ کرنے کا اختیار", "label_en": "Bank Account Operating Authority", "default": "دونوں پارٹنرز کے مشترکہ دستخط سے (Joint Signatures)"}
        ],
        "clauses_ur": [
            "یہ کہ فریقین نے باہمی رضامندی سے فرم بعنوان '{firm_name}' بمقام {business_address} کے تحت مشترکہ شراکت داری کا کاروبار شروع کرنے کا فیصلہ کیا ہے۔",
            "یہ کہ کاروبار کا کل ابتدائی سرمایہ مبلغ {total_capital} روپے ہے، جس میں فریق اول کا حصہ {p1_share} اور فریق دوم کا حصہ {p2_share} ہوگا اور تمام منافع و نقصان اسی شرح تناسب سے فریقین میں تقسیم ہوگا۔",
            "یہ کہ فرم کا شیڈولڈ کمرشل بینک میں باقاعدہ اکاؤنٹ کھولا جائے گا جو کہ {bank_operation} کے اصول پر آپریٹ ہوگا۔",
            "یہ کہ فریقین کاروبار کے تمام حسابات، لیجر اور کھاتہ جات کو شفاف رکھیں گے اور ہر انگریزی ماہ / سال کے اختتام پر باقاعدہ مالیاتی آڈٹ اور تقسیم منافع عمل میں لائی جائے گی۔",
            "یہ کہ کوئی بھی پارٹنر دوسرے پارٹنر کی پیشگی تحریری اجازت کے بغیر فرم کے نام پر قرض نہیں لے گا اور نہ ہی فرم کے اثاثے کسی تیسرے فریق کے پاس گروی رکھے گا۔",
            "یہ کہ اگر کوئی پارٹنر شراکت داری ختم کرنا چاہے تو وہ کم از کم 3 ماہ کا تحریری نوٹس دے گا، جس کے بعد اثاثہ جات کا باقاعدہ حساب کر کے اس کا حصہ ادا کر دیا جائے گا۔"
        ],
        "clauses_en": [
            "That the partners agree to carry on joint business under the name and style of '{firm_name}' at {business_address}.",
            "That the initial joint capital of the firm is PKR {total_capital}/-, shared as {p1_share} by First Partner and {p2_share} by Second Partner; net profits and losses shall be distributed in this exact agreed ratio.",
            "That the firm's commercial bank account shall be operated strictly under {bank_operation}.",
            "That all accounting books, vouchers, and registers shall be maintained transparently and open for inspection by all partners with periodic profit reconciliation.",
            "That no partner shall borrow money or pledge the firm's goodwill or assets without prior written consent of all other partners.",
            "That any partner desiring to dissolve or retire from the partnership shall serve at least 3 months prior written notice for orderly settlement of accounts."
        ]
    },

    "service_milestone_contract": {
        "category_ur": "کاروبار و شراکت داری",
        "category_en": "Business & Partnerships",
        "title_ur": "معاہدہ فراہم خدمات و ادائیگی بمطابق کام (سروسز کنٹریکٹ)",
        "title_en": "Service Provider Agreement with Milestone-Based Payments",
        "party1_role_ur": "سروس فراہم کنندہ (کمپنی / ڈویلپر / ٹھیکیدار)",
        "party1_role_en": "Service Provider / Contractor",
        "party2_role_ur": "کلائنٹ / فریق دوم",
        "party2_role_en": "Client / Hiring Party",
        "fields": [
            {"id": "scope_of_work", "label_ur": "تفصیلاتِ کام / پراجیکٹ کا دائرہ کار", "label_en": "Scope of Services / Project Scope", "default": "کسٹم ویب سائٹ ڈویلپمنٹ مع موبائل ایپ، ڈیٹا بیس ڈیزائن اور 3 ماہ مفت مینٹیننس"},
            {"id": "total_contract_fee", "label_ur": "کل طے شدہ کنٹریکٹ فیس (روپے)", "label_en": "Total Agreed Contract Fee (PKR)", "default": "450,000"},
            {"id": "initial_advance", "label_ur": "شروعاتی ایڈوانس رقم (روپے)", "label_en": "Initial Kickoff Advance (PKR)", "default": "100,000"},
            {"id": "milestone_breakdown", "label_ur": "مرحلہ وار ادائیگیوں کی تفصیل (Milestones)", "label_en": "Milestone Payment Schedule Details", "default": "مبلغ 150,000 یو آئی ڈیزائن و فرنٹ اینڈ فائنل ہونے پر، مبلغ 200,000 مکمل ڈیلیوری اور ٹیسٹنگ کے بعد"},
            {"id": "completion_timeline", "label_ur": "کام کی تکمیل کی آخری تاریخ", "label_en": "Project Completion Timeline Deadline", "default": "45 یوم (بمطابق 15 دسمبر 2026ء)"}
        ],
        "clauses_ur": [
            "یہ کہ فریق دوم نے فریق اول کو خدماتِ مذکورہ برائے '{scope_of_work}' فراہم کرنے کا کنٹریکٹ سونپا ہے، اور فریق اول اسے پیشہ ورانہ معیار پر مکمل کرنے کا اقرار کرتا ہے۔",
            "یہ کہ اس پراجیکٹ کی کل فیس مبلغ {total_contract_fee} روپے طے پائی ہے، جس میں سے مبلغ {initial_advance} روپے فریق دوم نے بطور ابتدائی ایڈوانس فریق اول کو ادا کر دیے ہیں۔",
            "یہ کہ بقیہ ادائیگی مرحلہ وار ہوگی یعنی: {milestone_breakdown}۔ فریق دوم مرحلہ مکمل ہونے پر 5 دن کے اندر ادائیگی ریلیز کرنے کا قانونی پابند ہوگا۔",
            "یہ کہ فریق اول مورخہ {completion_timeline} تک کام کی مکمل اور فعال ڈیلیوری فراہم کرنے کا پابند ہوگا، تاہم کلائنٹ کی تاخیر کی صورت میں ڈیڈ لائن میں اتنے دن کا خودکار اضافہ ہوگا۔",
            "یہ کہ مکمل ادائیگی کی وصولی کے بعد اس پراجیکٹ کے تمام انٹلیکچوئل پراپرٹی حقوق اور کوڈ فریق دوم کی ملکیت تصور ہوں گے۔",
            "یہ کہ اگر فریق دوم کام مکمل ہونے کے بعد بلا جواز ادائیگی روکتا ہے تو فریق اول کو قانونی نوٹس کے ذریعے ہرجانہ اور رکی ہوئی رقم ریکور کروانے کا مکمل حق حاصل ہوگا۔"
        ],
        "clauses_en": [
            "That the Client engages the Service Provider to execute services pertaining to '{scope_of_work}', which the Service Provider covenants to deliver with professional diligence.",
            "That total contract consideration is PKR {total_contract_fee}/-, out of which PKR {initial_advance}/- has been paid as non-refundable mobilization advance.",
            "That the balance consideration shall be released strictly on milestone delivery basis: {milestone_breakdown}; Client must clear invoices within 5 days of milestone verification.",
            "That the project shall be completed on or before {completion_timeline}, subject to timely provision of required access and approvals by the Client.",
            "That upon full and final payment, all intellectual property rights and deliverables shall stand transferred to the Client.",
            "That in case of non-payment of verified milestones, the Service Provider reserves the right to suspend services and claim contractual damages through legal process."
        ]
    },

    # =========================================================================
    # 4. VEHICLES & TRANSPORT (گاڑی و موٹر سائیکل)
    # =========================================================================
    "farokht_car": {
        "category_ur": "گاڑی و ٹرانسپورٹ",
        "category_en": "Vehicles & Transport",
        "title_ur": "اقرار نامہ بیع قطعی و حوالگی کار / موٹر کار",
        "title_en": "Motor Car Final Sale & Physical Delivery Deed",
        "party1_role_ur": "فروشندہ (مالک گاڑی)",
        "party1_role_en": "Seller / Registered Owner",
        "party2_role_ur": "خریدار",
        "party2_role_en": "Purchaser / Buyer",
        "fields": [
            {"id": "car_reg_no", "label_ur": "گاڑی کا رجسٹریشن نمبر", "label_en": "Vehicle Registration No", "default": "ICT-LE-1234"},
            {"id": "car_make_model", "label_ur": "میک و ماڈل (گاڑی کا نام)", "label_en": "Make & Model (e.g. Corolla 2022)", "default": "Toyota Corolla Altis 1.6 - 2022"},
            {"id": "chassis_no", "label_ur": "چیسس نمبر", "label_en": "Chassis Number", "default": "NZE170-9876543"},
            {"id": "engine_no", "label_ur": "انجن نمبر", "label_en": "Engine Number", "default": "1ZR-5432109"},
            {"id": "sale_price", "label_ur": "طے شدہ قیمتِ فروخت (روپے)", "label_en": "Agreed Sale Price (PKR)", "default": "4,200,000"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول گاڑی نمبری {car_reg_no} ماڈل {car_make_model} چیسس نمبر {chassis_no} انجن نمبر {engine_no} کا بلا شرکت غیرے مکمل قانونی مالک و قابض ہے۔",
            "یہ کہ فریق اول نے مذکورہ گاڑی کل مبلغ {sale_price} روپے میں فریق دوم کے ہاتھ فروخت کر کے پوری رقم یکمشت نقد / بینک وصول کر لی ہے۔",
            "یہ کہ فریق اول نے گاڑی کا موقع پر قبضہ، اصل سمارٹ کارڈ، کمپیوٹرائزڈ نمبر پلیٹس اور فائل فریق دوم کے حوالے کر دی ہے۔",
            "یہ کہ آج بتاریخ و بوقتِ دستخط سے قبل کے تمام چالان، ٹوکن ٹیکس، ایکسائز واجبات یا حادثات کا ذمہ دار فریق اول ہوگا، جبکہ آج کے وقت کے بعد کے تمام چالان، ٹریفک معاملات اور قانونی ذمہ داری فریق دوم پر عائد ہوگی۔",
            "یہ کہ فریق دوم 30 یوم کے اندر اندر مذکورہ گاڑی کو ایکسائز آفس سے اپنے نام پر بائیو میٹرک ٹرانسفر کروانے کا پابند ہوگا۔"
        ],
        "clauses_en": [
            "That the Seller is absolute owner and lawful possessor of vehicle registration {car_reg_no}, make/model {car_make_model}, chassis {chassis_no}, engine {engine_no}.",
            "That the Seller has sold the said vehicle to the Purchaser for total consideration of PKR {sale_price}/-, received in full.",
            "That physical possession, smart card, biometric clearance, and original number plates have been handed over on the spot.",
            "That all prior traffic violations, challans, and excise token liabilities prior to this execution date are the liability of Seller; subsequent liabilities belong strictly to Purchaser.",
            "That the Purchaser undertakes to transfer the vehicle title in Excise & Taxation records within 30 days."
        ]
    },

    "farokht_bike": {
        "category_ur": "گاڑی و ٹرانسپورٹ",
        "category_en": "Vehicles & Transport",
        "title_ur": "اقرار نامہ بیع قطعی موٹر سائیکل",
        "title_en": "Motorcycle Sale Deed & Handover",
        "party1_role_ur": "فروشندہ (مالک بائیک)",
        "party1_role_en": "Seller",
        "party2_role_ur": "خریدار",
        "party2_role_en": "Buyer",
        "fields": [
            {"id": "bike_reg_no", "label_ur": "موٹر سائیکل رجسٹریشن نمبر", "label_en": "Bike Registration No", "default": "RIL-5678"},
            {"id": "bike_model", "label_ur": "ماڈل و کمپنی (Honda 125 وغیرہ)", "label_en": "Make / Model", "default": "Honda CG 125 - 2023"},
            {"id": "chassis_no", "label_ur": "چیسس نمبر", "label_en": "Chassis Number", "default": "CG125-8765432"},
            {"id": "engine_no", "label_ur": "انجن نمبر", "label_en": "Engine Number", "default": "E-9871234"},
            {"id": "price", "label_ur": "قیمت فروخت (روپے)", "label_en": "Sale Price (PKR)", "default": "185,000"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول نے موٹر سائیکل نمبری {bike_reg_no} ماڈل {bike_model} بمطابق چیسس نمبر {chassis_no} اور انجن نمبر {engine_no} فریق دوم کو مبلغ {price} روپے کے عوض فروخت کر کے پوری رقم وصول پا لی ہے۔",
            "یہ کہ فریق اول نے موٹر سائیکل کا فزیکل قبضہ، اصل رجسٹریشن بک / سمارٹ کارڈ اور ایکسائز کاغذات فریق دوم کے حوالے کر دیے ہیں۔",
            "یہ کہ آج کے بعد اس موٹر سائیکل کے تمام پولیس امور، چالان یا قانونی معاملات کا ذمہ دار فریق دوم ہوگا۔"
        ],
        "clauses_en": [
            "That the Seller has sold motorcycle {bike_reg_no}, model {bike_model}, chassis {chassis_no}, engine {engine_no} to the Buyer for PKR {price}/- received in full.",
            "That physical possession and registration smart card have been delivered on the spot.",
            "That subsequent traffic, excise, and legal responsibilities lie exclusively with the Buyer."
        ]
    },

    # =========================================================================
    # 5. FINANCIAL & DEBT ACKNOWLEDGMENTS (مالیاتی لین دین و قرض)
    # =========================================================================
    "iqrar_nama_qarz": {
        "category_ur": "مالی لین دین و قرض",
        "category_en": "Financial & Debt Settlements",
        "title_ur": "اقرار نامہ وصولی قرضِ حسنہ و ضمانتِ ادائیگی",
        "title_en": "Promissory Note & Loan Debt Acknowledgment",
        "party1_role_ur": "مقروض (قرض لینے والا)",
        "party1_role_en": "Borrower / Debtor",
        "party2_role_ur": "قرض خواہ (رقم دینے والا)",
        "party2_role_en": "Creditor / Lender",
        "fields": [
            {"id": "loan_amount", "label_ur": "قرض کی رقم (روپے)", "label_en": "Loan Principal Amount (PKR)", "default": "800,000"},
            {"id": "repayment_date", "label_ur": "واپسی کی آخری طے شدہ تاریخ", "label_en": "Repayment Maturity Date", "default": "25 جنوری 2027ء"},
            {"id": "security_cheque", "label_ur": "بطور ضمانت دیا گیا چیک نمبر و بینک", "label_en": "Security Cheque No & Bank Details", "default": "چیک نمبر 45678912 حبیب بینک لمیٹڈ اسلام آباد"}
        ],
        "clauses_ur": [
            "یہ کہ فریق اول نے اپنی اشد ذاتی و گھریلو ضرورت کے تحت فریق دوم سے بلا سود قرضِ حسنہ مبلغ {loan_amount} روپے نقد وصول پا کر قرض کی موجودگی کا باقاعدہ اعتراف کرتا ہے۔",
            "یہ کہ فریق اول یہ اقرار کرتا ہے کہ وہ یہ رقم مورخہ {repayment_date} تک فریق دوم کو بلا حیل و حجت یکمشت واپس لوٹانے کا سختی سے پابند ہوگا۔",
            "یہ کہ برائے تسلی و سیکیورٹی فریق اول نے فریق دوم کو اپنے اکاؤنٹ کا {security_cheque} پیش کیا ہے، اور اگر مقررہ تاریخ تک رقم واپس نہ کی گئی تو فریق دوم کو چیک ڈس آنر کروا کر ایف آئی آر زیر دفعہ 489-F ت پ درج کروانے کا قانونی حق حاصل ہوگا۔"
        ],
        "clauses_en": [
            "That the Debtor expressly acknowledges receiving an interest-free personal loan of PKR {loan_amount}/- from the Creditor.",
            "That the Debtor undertakes and promises to repay the entire sum on or before {repayment_date} without excuse.",
            "That as assurance, the Debtor has issued security cheque {security_cheque}, and in event of default the Creditor reserves full right to initiate criminal proceedings under Section 489-F PPC."
        ]
    },

    # =========================================================================
    # 6. GENERAL & FAMILY DEEDS (عام اقرار نامہ و فیملی)
    # =========================================================================
    "mukhtar_nama_khas": {
        "category_ur": "عام اقرار نامہ و فیملی",
        "category_en": "General & Family Deeds",
        "title_ur": "مختار نامہ خاص (سپیشل پاور آف اٹارنی)",
        "title_en": "Special Power of Attorney Deed",
        "party1_role_ur": "مقر (اصیل)",
        "party1_role_en": "Principal / Grantor",
        "party2_role_ur": "مختارِ خاص (وکیل)",
        "party2_role_en": "Special Attorney",
        "fields": [
            {"id": "purpose_scope", "label_ur": "مختار نامہ کا مخصوص مقصد و کارروائی", "label_en": "Specific Scope & Purpose of Authority", "default": "پلاٹ نمبر 50 سیکٹر ڈی-12 اسلام آباد کے ایکسائز و سی ڈی اے دفاتر میں حاضری، دستاویزات وصولی و دیکھ بھال"},
            {"id": "validity_period", "label_ur": "مدتِ اختیار", "label_en": "Validity Period", "default": "1 سال (تا اختتام دسمبر 2027ء)"}
        ],
        "clauses_ur": [
            "یہ کہ چونکہ مقر بوجہ ذاتی مصروفیات / بیماری متعلقہ دفاتر میں بذاتِ خود حاضر ہونے سے قاصر ہے، لہٰذا وہ فریق دوم کو اپنا بااختیار مختارِ خاص برائے {purpose_scope} مقرر کرتا ہے۔",
            "یہ کہ مختارِ خاص کو مذکورہ امور کے سلسلے میں دستخط کرنے، رسیدیں لینے اور دفتری کارروائی مکمل کرنے کا مکمل مجاز اختیار حاصل ہوگا، اور اس کا کیا گیا ہر فعل ایسے مانا جائے گا جیسے خود اصیل نے کیا ہو۔",
            "یہ کہ مختارِ خاص کو جائیداد کو آگے بیچنے یا کسی تیسرے کے نام رجسٹری کروانے کا حق نہیں ہوگا تاوقتیکہ اس کے پاس اس کا الگ اختیار نہ ہو، اور یہ مختار نامہ {validity_period} تک مؤثر رہے گا۔"
        ],
        "clauses_en": [
            "That the Principal hereby appoints the Special Attorney to represent and act in respect of {purpose_scope}.",
            "That all lawful acts, signatures, and submissions executed by the Attorney under this deed shall be deemed to have been done directly by the Principal.",
            "That this power is restricted to the specific terms stated and does not authorize sale of property, remaining valid for {validity_period}."
        ]
    }
}

def get_categories(lang="ur"):
    """Returns sorted unique categories list based on language"""
    cat_key = "category_ur" if lang == "ur" else "category_en"
    cats = sorted(list(set(doc[cat_key] for doc in LEGAL_TEMPLATES.values())))
    return cats
import os
import random
import pandas as pd

os.makedirs("data", exist_ok=True)

employees = ["أحمد علي", "خالد محمد", "سارة حسن", "عمر صالح", "ياسر ناصر", "منى عبدالله"]
normal_actions = ["تسجيل دخول", "إدخال فاتورة", "تعديل فاتورة", "عرض تقرير"]

rows = []

for _ in range(285):
    action = random.choice(normal_actions)
    rows.append({
        "employee_name": random.choice(employees),
        "hour": random.randint(8, 16),
        "action": action,
        "amount": random.randint(5000, 150000) if "فاتورة" in action else 0,
        "records_exported": random.randint(0, 15)
    })

suspicious_cases = [
    {"employee_name": "خالد محمد", "hour": 2, "action": "تصدير بيانات", "amount": 0, "records_exported": 520},
    {"employee_name": "عمر صالح", "hour": 3, "action": "تصدير بيانات", "amount": 0, "records_exported": 780},
    {"employee_name": "ياسر ناصر", "hour": 1, "action": "تصدير بيانات", "amount": 0, "records_exported": 410},
    {"employee_name": "أحمد علي", "hour": 15, "action": "تعديل فاتورة", "amount": 1850000, "records_exported": 2},
    {"employee_name": "خالد محمد", "hour": 23, "action": "تعديل فاتورة", "amount": 2400000, "records_exported": 5},
    {"employee_name": "سارة حسن", "hour": 14, "action": "تعديل فاتورة", "amount": 1300000, "records_exported": 0},
]

for _ in range(9):
    case_type = random.choice(["night_export", "huge_amount", "late_login"])
    if case_type == "night_export":
        rows.append({
            "employee_name": random.choice(employees),
            "hour": random.choice([0, 1, 2, 3, 4, 23]),
            "action": "تصدير بيانات",
            "amount": 0,
            "records_exported": random.randint(300, 900)
        })
    elif case_type == "huge_amount":
        rows.append({
            "employee_name": random.choice(employees),
            "hour": random.randint(8, 22),
            "action": "تعديل فاتورة",
            "amount": random.randint(900000, 2500000),
            "records_exported": random.randint(0, 10)
        })
    else:
        rows.append({
            "employee_name": random.choice(employees),
            "hour": random.choice([0, 1, 2, 3, 4]),
            "action": "تسجيل دخول",
            "amount": 0,
            "records_exported": random.randint(100, 300)
        })

rows.extend(suspicious_cases)
random.shuffle(rows)

df = pd.DataFrame(rows)
df.to_csv("data/sample_logs.csv", index=False, encoding="utf-8-sig")
print(f"تم إنشاء ملف البيانات بنجاح! إجمالي العمليات: {len(df)}")
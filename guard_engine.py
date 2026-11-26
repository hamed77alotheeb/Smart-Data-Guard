import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

os.makedirs("data", exist_ok=True)

def _build_arabic_alert(row):
    reasons = []
    if row["hour"] < 7 or row["hour"] > 18:
        reasons.append(f"دخول خارج أوقات الدوام (الساعة {int(row['hour'])}:00)")
    if row["records_exported"] > 100:
        reasons.append(f"سحب كمية كبيرة من السجلات ({int(row['records_exported'])} سجل)")
    if row["amount"] > 500000:
        reasons.append(f"مبلغ مالي ضخم ({int(row['amount']):,})")
    
    if not reasons:
        reasons.append("نمط حركة غير معتاد مقارنة بسجل الموظف")
        
    reason_text = " + ".join(reasons)
    return f"تنبيه: الموظف ({row['employee_name']}) قام بـ ({row['action']}) — السبب: {reason_text}."

def analyze_logs(file_path):
    if str(file_path).endswith(".xlsx") or str(file_path).endswith(".xls"):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    features = df[["hour", "amount", "records_exported"]].fillna(0)
    model = IsolationForest(contamination=0.06, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    suspicious_df = df[df["anomaly"] == -1].copy()
    if not suspicious_df.empty:
        suspicious_df["رسالة_التنبيه_للمدير"] = suspicious_df.apply(_build_arabic_alert, axis=1)

    display_cols = ["employee_name", "hour", "action", "amount", "records_exported", "رسالة_التنبيه_للمدير"]
    alerts_df = suspicious_df[display_cols] if not suspicious_df.empty else pd.DataFrame(columns=display_cols)

    report_path = "data/suspicious_report.csv"
    alerts_df.to_csv(report_path, index=False, encoding="utf-8-sig")

    chart_path = "data/analysis_chart.png"
    normal_count = len(df) - len(alerts_df)
    suspicious_count = len(alerts_df)

    plt.figure(figsize=(6, 4))
    bars = plt.bar(["Normal Operations", "Suspicious Alerts"], [normal_count, suspicious_count], color=["#2ecc71", "#e74c3c"])
    plt.title("Smart Data Guard - Activity Overview")
    plt.ylabel("Number of Operations")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, int(yval), ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    risk_percent = (suspicious_count / len(df) * 100) if len(df) > 0 else 0
    summary = (
        f"إجمالي العمليات المفحوصة: {len(df)} عملية\n"
        f"عدد العمليات المشبوهة المرصودة: {suspicious_count} عملية\n"
        f"نسبة الخطر في السجل: {risk_percent:.1f}%"
    )

    return summary, alerts_df, chart_path, report_path

if __name__ == "__main__":
    summary, alerts, chart, report = analyze_logs("data/sample_logs.csv")
    print(summary)
    print("\nأول 3 تنبيهات:")
    for msg in alerts["رسالة_التنبيه_للمدير"].head(3):
        print("-", msg)
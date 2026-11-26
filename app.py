# -*- coding: utf-8 -*-
import gradio as gr
from guard_engine import analyze_logs

def run_sample():
    return analyze_logs("data/sample_logs.csv")

def run_uploaded(file):
    if file is None:
        return "يرجى رفع ملف CSV أو Excel أولاً.", None, None, None
    return analyze_logs(file.name)

with gr.Blocks(title="Smart Data Guard - الحارس الذكي") as demo:
    gr.Markdown("# 🛡️ نظام الحارس الذكي لحماية البيانات (Smart Data Guard)")
    gr.Markdown("نظام ذكاء اصطناعي لمراقبة سجلات الشركات واكتشاف العمليات المشبوهة والتلاعب بالبيانات تلقائياً.")
    
    with gr.Row():
        sample_btn = gr.Button("🚀 تجربة فورية بالبيانات التجريبية للشركة", variant="primary")
    
    with gr.Row():
        file_input = gr.File(label="أو ارفع ملف سجل الشركة (CSV أو Excel)", file_types=[".csv", ".xlsx", ".xls"])
        analyze_btn = gr.Button("🔍 فحص الملف المرفوع")
        
    summary_out = gr.Textbox(label="ملخص الفحص ونسبة الخطر", lines=3)
    
    with gr.Row():
        chart_out = gr.Image(label="الرسم البياني للعمليات")
        report_out = gr.File(label="تحميل تقرير المخالفات (CSV)")
        
    alerts_table = gr.Dataframe(label="جدول العمليات المشبوهة والتنبيهات الفورية للمدير")
    
    sample_btn.click(fn=run_sample, outputs=[summary_out, alerts_table, chart_out, report_out])
    analyze_btn.click(fn=run_uploaded, inputs=[file_input], outputs=[summary_out, alerts_table, chart_out, report_out])

if __name__ == "__main__":
    demo.launch()
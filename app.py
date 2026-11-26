import gradio as gr
import gradio as gr
from guard_engine import analyze_logs

def run_sample():
    return analyze_logs("data/sample_logs.csv")

def run_uploaded(file):
    if file is None:
        return "ο©¤ξ ©εγ κιε CSV ν Excel νιρ.", None, None, None
    file_path = file if isinstance(file, str) else file.name
    return analyze_logs(file_path)

with gr.Blocks(title="Smart Data Guard - ι¥©« ι¨θο") as demo:
    gr.Markdown("# ??? λβκ ι¥©« ι¨θο ι¥κο΅ ι ολΆ (Smart Data Guard)")
    gr.Markdown("λβκ ¨θ ­αλγο ικ©η ΅ «¤ιΆ ι¬©θΆ νθΆ¬ε ιγκιοΆ ικ¬ νμ΅ νιΆιγ   ι ολΆ Άιηορ.")

    with gr.Row():
        sample_btn = gr.Button("?? Ά¤© ΅ εν©ο΅  ι ολΆ ιΆ¤©ο ο΅ ιι¬©θ΅", variant="primary")

    with gr.Row():
        file_input = gr.File(label="ν ©εγ κιε «¤ι ι¬©θ΅ (CSV ν Excel)", file_types=[".csv", ".xlsx", ".xls"])
        analyze_btn = gr.Button("?? ε¥­ ικιε ικ©ενγ")

    summary_out = gr.Textbox(label="κι¦­ ιε¥­ νλ« ΅ ι¦α©", lines=3)

    with gr.Row():
        chart_out = gr.Image(label="ι©«κ ι ολο ιιγκιοΆ")
        report_out = gr.File(label="Ά¥κοι Άη©ο© ικ¦ιεΆ (CSV)")

    alerts_table = gr.Dataframe(label="¤§νι ιγκιοΆ ικ¬ νμ΅ νιΆλ ομΆ ιεν©ο΅ ιικ§ο©")

    sample_btn.click(fn=run_sample, outputs=[summary_out, alerts_table, chart_out, report_out])
    analyze_btn.click(fn=run_uploaded, inputs=[file_input], outputs=[summary_out, alerts_table, chart_out, report_out])

if __name__ == "__main__":
    demo.launch()

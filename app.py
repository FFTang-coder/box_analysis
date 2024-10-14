from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


def load_data():
    csv_file = 'pred_analysis.csv'  # 请确保文件路径正确
    df = pd.read_csv(csv_file)
    df = df.sort_values(by=['预测日期', 'todaybox'], ascending=[False, False])
    return df


# 路由：主界面，显示筛选表格
@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_data()

    # 获取所有的预测日期作为筛选项
    unique_dates = df['预测日期'].unique()

    # 如果用户选择了日期，通过POST方法获取
    selected_date = request.form.get('date_filter')

    # 根据选择的日期筛选数据
    if selected_date:
        df_filtered = df[df['预测日期'] == int(selected_date)]
    else:
        df_filtered = df  # 默认显示所有数据

    # 为r10列大于0.1的值添加标红样式
    def highlight_r10(val):
        if val >= 0.2:
            color = 'red'
        elif val < 0.1:
            color = 'black'
        else:
            color = 'blue'
        return f'color: {color}'

    cols = [col for col in df_filtered.select_dtypes(include='number').columns if col not in ['预测日期', 'movie_id']]
    round_map = {col: '{:.2f}'.format for col in cols}
    column_names = df_filtered.columns.tolist()
    column_names = ['index'] + column_names
    # 转换为HTML，应用Bootstrap样式，并高亮r10列
    data_html = df_filtered.style.format(round_map) \
        .applymap(highlight_r10, subset=['预测误差', '专业版误差']) \
        .set_table_attributes('class="table table-striped table-hover"').to_html()

    return render_template('display.html', data=data_html, dates=unique_dates, column_names=column_names)

if __name__ == '__main__':
    app.run(debug=True)
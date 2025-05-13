import kivy
kivy.require('2.1.0')  # 替换为您的Kivy版本

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.core.window import Window
from kivy.metrics import dp
import os

# 设置窗口大小为标准手机尺寸
Window.size = (dp(360), dp(640))  # 使用标准手机尺寸

# 注册中文字体
resource_add_path(os.path.join(os.environ.get('WINDIR'), 'Fonts'))  # Windows字体目录
try:
    # 注册微软雅黑字体，用于显示中文
    LabelBase.register('Microsoft YaHei', 
                      fn_regular='msyh.ttc',
                      fn_bold='msyhbd.ttc')
except:
    print("无法加载微软雅黑字体，将尝试使用系统默认字体")

# 使用try-except块处理matplotlib backend导入
try:
    from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
except ImportError:
    print("未找到matplotlib backend，请安装kivy_garden.matplotlib")
    print("安装命令: pip install kivy_garden.matplotlib")
    raise

# 配置matplotlib使用Agg后端，提高在移动设备上的性能
import matplotlib
matplotlib.use('Agg')  # 这必须在导入pyplot之前设置

# 设置matplotlib的字体和样式，防止中文显示问题
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'KaiTi', 'FangSong', 'SimSun', 'NSimSun', 'STXihei', 'WenQuanYi Micro Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 10  # 减小字体大小
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.titlesize'] = 12  # 减小标题字体大小
matplotlib.rcParams['axes.labelsize'] = 10
matplotlib.rcParams['xtick.labelsize'] = 8  # 减小刻度标签字体大小
matplotlib.rcParams['ytick.labelsize'] = 8
matplotlib.rcParams['legend.fontsize'] = 8
matplotlib.rcParams['figure.titlesize'] = 12

import matplotlib.pyplot as plt
import numpy as np

class ScrollableMatplotlibApp(App):
    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(5))
        
        # 创建标题标签
        title_label = Label(
            text='Matplotlib 数据可视化展示',
            size_hint=(1, 0.08),  # 减小标题高度
            font_size=dp(20),  # 使用dp单位
            bold=True,
            color=(0.2, 0.6, 1, 1),
            font_name='Microsoft YaHei'
        )
        main_layout.add_widget(title_label)
        
        # 创建滚动视图
        scroll_view = ScrollView(
            size_hint=(1, 0.92),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(5),  # 减小滚动条宽度
            bar_color=[0.2, 0.7, 0.9, 1],
            effect_cls="ScrollEffect"
        )
        main_layout.add_widget(scroll_view)
        
        # 创建网格布局来容纳多个图表
        grid_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(5)
        )
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        
        # 添加四个不同的Matplotlib图表
        self.add_sin_chart(grid_layout)
        self.add_cos_chart(grid_layout)
        self.add_bar_chart(grid_layout)
        self.add_scatter_chart(grid_layout)
        
        scroll_view.add_widget(grid_layout)
        
        return main_layout
    
    def add_sin_chart(self, parent_layout):
        # 创建一个包含标题的布局
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(280),  # 减小图表高度
            spacing=dp(5)
        )
        chart_label = Label(
            text='正弦波图表',
            size_hint_y=0.15,
            color=(0, 0.7, 1, 1),
            font_size=dp(14),
            bold=True,
            font_name='Microsoft YaHei'
        )
        chart_layout.add_widget(chart_label)
        
        # 创建正弦波图表
        fig, ax = plt.subplots(figsize=(4, 2.5), dpi=100)  # 调整图表尺寸
        fig.tight_layout(pad=1.2)
        
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, 'b-', linewidth=1.5)  # 减小线宽
        ax.set_title('正弦波函数图', fontsize=12, pad=8)
        ax.set_xlabel('X 轴', fontsize=10)
        ax.set_ylabel('sin(x) 值', fontsize=10)
        ax.grid(True, alpha=0.2)
        
        # 添加图表到布局
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        # 添加到父布局
        parent_layout.add_widget(chart_layout)
    
    def add_cos_chart(self, parent_layout):
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(280),
            spacing=dp(5)
        )
        chart_label = Label(
            text='余弦波图表',
            size_hint_y=0.15,
            color=(1, 0.4, 0.4, 1),
            font_size=dp(14),
            bold=True,
            font_name='Microsoft YaHei'
        )
        chart_layout.add_widget(chart_label)
        
        fig, ax = plt.subplots(figsize=(4, 2.5), dpi=100)
        fig.tight_layout(pad=1.2)
        
        x = np.linspace(0, 10, 100)
        y = np.cos(x)
        ax.plot(x, y, 'r-', linewidth=1.5)
        ax.set_title('余弦波函数图', fontsize=12, pad=8)
        ax.set_xlabel('X 轴', fontsize=10)
        ax.set_ylabel('cos(x) 值', fontsize=10)
        ax.grid(True, alpha=0.2)
        
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        parent_layout.add_widget(chart_layout)
    
    def add_bar_chart(self, parent_layout):
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(280),
            spacing=dp(5)
        )
        chart_label = Label(
            text='月度数据统计',
            size_hint_y=0.15,
            color=(0.2, 0.8, 0.2, 1),
            font_size=dp(14),
            bold=True,
            font_name='Microsoft YaHei'
        )
        chart_layout.add_widget(chart_label)
        
        fig, ax = plt.subplots(figsize=(4, 2.5), dpi=100)
        fig.tight_layout(pad=1.2)
        
        categories = ['一月', '二月', '三月', '四月', '五月']
        values = [23, 45, 56, 78, 32]
        bars = ax.bar(categories, values, color='green', alpha=0.7)
        
        # 在柱状图上添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    '%d' % int(height), ha='center', va='bottom', fontsize=8)
        
        ax.set_title('月度销售数据', fontsize=12, pad=8)
        ax.set_xlabel('月份', fontsize=10)
        ax.set_ylabel('销售额（万元）', fontsize=10)
        ax.set_ylim(0, max(values) * 1.2)
        plt.xticks(rotation=45)  # 旋转x轴标签以防重叠
        
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        parent_layout.add_widget(chart_layout)
    
    def add_scatter_chart(self, parent_layout):
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(280),
            spacing=dp(5)
        )
        chart_label = Label(
            text='散点分布图',
            size_hint_y=0.15,
            color=(0.8, 0.4, 1, 1),
            font_size=dp(14),
            bold=True,
            font_name='Microsoft YaHei'
        )
        chart_layout.add_widget(chart_label)
        
        fig, ax = plt.subplots(figsize=(4, 2.5), dpi=100)
        fig.tight_layout(pad=1.2)
        
        np.random.seed(42)
        x = np.random.rand(50)
        y = np.random.rand(50)
        colors = np.random.rand(50)
        size = (20 * np.random.rand(50))**2  # 减小点的大小
        
        scatter = ax.scatter(x, y, c=colors, s=size, alpha=0.6, cmap='viridis')
        ax.set_title('数据分布散点图', fontsize=12, pad=8)
        ax.set_xlabel('X 坐标', fontsize=10)
        ax.set_ylabel('Y 坐标', fontsize=10)
        ax.grid(True, alpha=0.2)
        
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        parent_layout.add_widget(chart_layout)

def main():
    try:
        ScrollableMatplotlibApp().run()
    except Exception as e:
        print(f"错误: {e}")
        print("请确保已安装所有必要的依赖：")
        print("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple kivy matplotlib numpy kivy_garden")
        print("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple https://github.com/kivy-garden/matplotlib/archive/master.zip")

if __name__ == '__main__':
    main() 
import kivy
kivy.require('2.1.0')  # 替换为您的Kivy版本

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

# 使用try-except块处理matplotlib backend导入
try:
    from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
except ImportError:
    try:
        from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    except ImportError:
        print("未找到matplotlib backend，请安装kivy_garden.matplotlib")
        print("安装命令: pip install kivy_garden.matplotlib")
        raise

# 配置matplotlib使用Agg后端，提高在移动设备上的性能
import matplotlib
matplotlib.use('Agg')  # 这必须在导入pyplot之前设置

# 设置matplotlib的字体和样式，防止中文显示问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号
matplotlib.rcParams['font.size'] = 10  # 字体大小适合移动设备

import matplotlib.pyplot as plt
import numpy as np

class ScrollableMatplotlibApp(App):
    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical')
        
        # 创建标题标签
        title_label = Label(
            text='Matplotlib 图表展示',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True
        )
        main_layout.add_widget(title_label)
        
        # 创建滚动视图
        scroll_view = ScrollView(
            size_hint=(1, 0.9),
            do_scroll_x=False,  # 禁用水平滚动
            do_scroll_y=True,   # 启用垂直滚动
            bar_width=10,
            bar_color=[0.2, 0.7, 0.9, 1],  # 滚动条颜色
            effect_cls="ScrollEffect"  # 提高在移动设备上的滚动体验
        )
        main_layout.add_widget(scroll_view)
        
        # 创建网格布局来容纳多个图表
        grid_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=10
        )
        # 这一步很重要：确保网格布局的高度能够适应其内容
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        
        # 添加四个不同的Matplotlib图表
        self.add_sin_chart(grid_layout)
        self.add_cos_chart(grid_layout)
        self.add_bar_chart(grid_layout)
        self.add_scatter_chart(grid_layout)
        
        # 将网格布局添加到滚动视图
        scroll_view.add_widget(grid_layout)
        
        return main_layout
    
    def add_sin_chart(self, parent_layout):
        # 创建一个包含标题的布局
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=350
        )
        chart_label = Label(
            text='正弦波图表',
            size_hint_y=0.1,
            color=(0, 0.7, 1, 1)
        )
        chart_layout.add_widget(chart_label)
        
        # 创建正弦波图表
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        fig.tight_layout(pad=1.2)  # 确保在小屏幕上也有足够的边距
        
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, 'b-', linewidth=2)
        ax.set_title('正弦波')
        ax.set_xlabel('x')
        ax.set_ylabel('sin(x)')
        ax.grid(True, alpha=0.3)
        
        # 添加图表到布局
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        # 添加到父布局
        parent_layout.add_widget(chart_layout)
    
    def add_cos_chart(self, parent_layout):
        # 创建一个包含标题的布局
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=350
        )
        chart_label = Label(
            text='余弦波图表',
            size_hint_y=0.1,
            color=(1, 0.4, 0.4, 1)
        )
        chart_layout.add_widget(chart_label)
        
        # 创建余弦波图表
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        fig.tight_layout(pad=1.2)
        
        x = np.linspace(0, 10, 100)
        y = np.cos(x)
        ax.plot(x, y, 'r-', linewidth=2)
        ax.set_title('余弦波')
        ax.set_xlabel('x')
        ax.set_ylabel('cos(x)')
        ax.grid(True, alpha=0.3)
        
        # 添加图表到布局
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        # 添加到父布局
        parent_layout.add_widget(chart_layout)
    
    def add_bar_chart(self, parent_layout):
        # 创建一个包含标题的布局
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=350
        )
        chart_label = Label(
            text='柱状图',
            size_hint_y=0.1,
            color=(0.2, 0.8, 0.2, 1)
        )
        chart_layout.add_widget(chart_label)
        
        # 创建柱状图
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        fig.tight_layout(pad=1.2)
        
        categories = ['一月', '二月', '三月', '四月', '五月']
        values = [23, 45, 56, 78, 32]
        bars = ax.bar(categories, values, color='green', alpha=0.7)
        
        # 在柱状图上添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    '%d' % int(height), ha='center', va='bottom', fontsize=9)
        
        ax.set_title('月度数据')
        ax.set_xlabel('月份')
        ax.set_ylabel('数值')
        ax.set_ylim(0, max(values) * 1.2)  # 给标签留出空间
        
        # 添加图表到布局
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        # 添加到父布局
        parent_layout.add_widget(chart_layout)
    
    def add_scatter_chart(self, parent_layout):
        # 创建一个包含标题的布局
        chart_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=350
        )
        chart_label = Label(
            text='散点图',
            size_hint_y=0.1,
            color=(0.8, 0.4, 1, 1)
        )
        chart_layout.add_widget(chart_label)
        
        # 创建散点图
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        fig.tight_layout(pad=1.2)
        
        # 生成随机数据
        np.random.seed(42)  # 设置随机种子以便结果可重复
        x = np.random.rand(50)
        y = np.random.rand(50)
        colors = np.random.rand(50)
        size = (30 * np.random.rand(50))**2  # 不同大小的点
        
        scatter = ax.scatter(x, y, c=colors, s=size, alpha=0.6, cmap='viridis')
        ax.set_title('随机散点图')
        ax.set_xlabel('X 轴')
        ax.set_ylabel('Y 轴')
        ax.grid(True, alpha=0.3)
        
        # 添加图表到布局
        chart_widget = FigureCanvasKivyAgg(fig)
        chart_layout.add_widget(chart_widget)
        
        # 添加到父布局
        parent_layout.add_widget(chart_layout)

# 添加一个主函数，包含简单的异常处理以提供更好的用户体验
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
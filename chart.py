try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

def draw_history_chart(*args, **kwargs):
    if plt is None:
        print("matplotlib 未安装，无法生成图表。")
        return None
    # 在这里写你的绘图代码
    # 例如：
    # plt.plot(...)
    # plt.savefig(...)
    # return 图片路径或图片数据

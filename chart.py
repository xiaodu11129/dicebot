import matplotlib.pyplot as plt
from io import BytesIO

def draw_history_chart(lotteries):
    sums = [l.sum for l in lotteries]
    periods = [l.period for l in lotteries]
    plt.figure(figsize=(6,3))
    plt.plot(periods, sums, marker='o', label='和值')
    plt.xlabel('期数')
    plt.ylabel('和值')
    plt.title('最近开奖和值走势图')
    plt.grid(True)
    plt.legend()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

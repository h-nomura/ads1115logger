# _*_ coding:utf-8 _*_
# SIMPLE CURVE GRAPH PY
# VERSION 1.0.0
# ENV VERSION PYTHON 3.6.5,matplotlib 2.2.2
# CREATED BY @pomta_trd

# モジュールインポート
import matplotlib.pyplot as plt

# 初期化
i = 0
j = 0
x = []
y = []
plt.ion()

# MATPLOTLIB コンフィグ
plt.title('Simple Curve Graph') ## グラフタイトル（必須ではない）
plt.xlabel('x') ## x軸ラベル（必須ではない）
plt.ylabel('y') ## y軸ラベル（必須ではない）
plt.xlim(0,100) ## x軸範囲固定（必須ではない）
plt.grid() ## グリッド線オン（必須ではない）

# MAIN
while True:
    ## 描画データ生成
    i = i + 1
    j = i ** 0.1
    x.append(i) ### x軸データ
    y.append(j) ### y軸データ
    plt.plot(x,y,color='blue')

    ## グラフ描画
    plt.draw()

    ## iが100ならWhileを抜ける
    if i == 100:
        break
    
    ## 更新待機（秒）
    plt.pause(0.1)

# グラフを閉じる
plt.close()
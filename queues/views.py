from django.shortcuts import render
import numpy
import pandas

# Create your views here.

# 格式化函数
def pretty(numpy_3d):

    # 将放置方法的数量放入结果数组
    result = [0]
    result[0] = numpy_3d[0]

    # 定义lambda函数
    func = lambda x: x.idxmax()

    # 循环每一个二维棋盘,记得去掉numpy_3d[0]
    for numpy_2d in numpy_3d[1:]:

        # 转化为DF
        DF_2d = pandas.DataFrame(numpy_2d)
        result.append(DF_2d.apply(func, 1).tolist())

    # 返回结果
    return result

# 解决 num数量的皇后如何放置 的函数
def how_to_place(num):

    # 生成 n×n 的棋盘
    chess_board = numpy.zeros([num,num])

    # 结果列表，第一个位置存 总放置方法数
    res = [0]

    # 判断(i,j)位置是否可以放置
    def check(i, j):
        # 左上角
        for n in range(min(i,j)):
            if chess_board[i-n-1][j-n-1] : return False
        # 左下角
        # for n in range(min(num-1-i,j)):
        #     if chess_board[i+n+1][j-n-1] : return False
        # 右上角
        for n in range(min(i,num-1-j)):
            if chess_board[i-n-1][j+n+1] : return False
        # 右下角
        # for n in range(min(num-1-i,num-1-j)):
        #     if chess_board[i+n+1][j+n+1] : return False

        if chess_board[i,:].sum() : return False
        if chess_board[:,j].sum() : return False
        return True

    # 在第i行放置皇后
    def put_queue(i):
        if i > num-1:
            res[0] += 1
            # 如果大于10,则不予显示
            if res[0] <= 10:
                res.append(chess_board.copy())
            return 

        # 遍历第i行的所有位置
        for j in range(num):
            # 如果(i,j)位置可以放置
            if check(i,j):
                # 该位置标记为 1
                chess_board[i][j] = 1
                # 递归：再到下一行放置皇后
                put_queue(i+1)
                chess_board[i][j] = 0

    # 开始在第一行放置皇后
    put_queue(0)
    return res

# 结果呈现函数
def show(request):
    
    num = 0
    result = None
    range_num = None

    # 获取参数num  num的可迭代对象
    if request.GET.get("num"):
        num = int(request.GET.get("num"))
        range_num = range(num)

        # 放置皇后,取得结果，为一个三维数组
        result = how_to_place(num)
        
        # 美化结果
        result = pretty(result)
        template = 'show.html'

    else:
        template = 'qindex.html'
    
    return render(request, template,
                  {'result':result,
                   'num':num,
                   'range_num':range_num})

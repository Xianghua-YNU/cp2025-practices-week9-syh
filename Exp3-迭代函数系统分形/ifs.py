import numpy as np
import matplotlib.pyplot as plt


def get_fern_params():
    """
    返回巴恩斯利蕨的IFS参数
    每个变换包含6个参数(a,b,c,d,e,f)和概率p
    """
    return [
        [0.00, 0.00, 0.00, 0.16, 0.00, 0.00, 0.01],
        [0.85, 0.04, -0.04, 0.85, 0.00, 1.60, 0.85],
        [0.20, -0.26, 0.23, 0.22, 0.00, 1.60, 0.07],
        [-0.15, 0.28, 0.26, 0.24, 0.00, 0.44, 0.07]
    ]


def get_tree_params():
    """
    返回概率树的IFS参数
    每个变换包含6个参数(a,b,c,d,e,f)和概率p
    """
    return [
        [0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.1],
        [0.42, -0.42, 0.42, 0.42, 0.0, 0.2, 0.45],
        [0.42, 0.42, -0.42, 0.42, 0.0, 0.2, 0.45]
    ]


def apply_transform(point, params):
    """
    应用单个变换到点
    :param point: 当前点坐标(x,y)
    :param params: 变换参数[a,b,c,d,e,f,p]
    :return: 变换后的新坐标(x',y')
    """
    x, y = point
    a, b, c, d, e, f, _ = params
    new_x = a * x + b * y + e
    new_y = c * x + d * y + f
    return new_x, new_y


def run_ifs(ifs_params, num_points=100000, num_skip=100):
    """
    运行IFS迭代生成点集
    :param ifs_params: IFS参数列表
    :param num_points: 总点数
    :param num_skip: 跳过前n个点
    :return: 生成的点坐标数组
    """
    probabilities = [param[-1] for param in ifs_params]
    transform_indices = np.arange(len(ifs_params))
    current_point = (0.5, 0)
    result_points = []

    for _ in range(num_points + num_skip):
        selected_index = np.random.choice(transform_indices, p=probabilities)
        selected_transform = ifs_params[selected_index]
        current_point = apply_transform(current_point, selected_transform)
        if _ >= num_skip:
            result_points.append(current_point)

    return np.array(result_points)


def plot_ifs(points, title="IFS Fractal", save_path=None):
    """
    绘制IFS分形并保存为PNG
    :param points: 点坐标数组
    :param title: 图像标题
    :param save_path: 保存路径
    """
    plt.figure(figsize=(8, 8))
    plt.scatter(points[:, 0], points[:, 1], s=1, color='green', alpha=0.75)
    plt.title(title)
    plt.axis('equal')
    plt.axis('off')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()


if __name__ == "__main__":
    # 生成并绘制巴恩斯利蕨
    fern_params = get_fern_params()
    fern_points = run_ifs(fern_params)
    plot_ifs(fern_points, "Barnsley Fern", "barnsley_fern.png")

    # 生成并绘制概率树
    tree_params = get_tree_params()
    tree_points = run_ifs(tree_params)
    plot_ifs(tree_points, "Probability Tree", "probability_tree.png")

import numpy as np
import matplotlib.pyplot as plt


def koch_generator(u, level):
    # 初始竖直线段
    u = np.array([0, 1j])
    if level <= 0:
        return u
    # 旋转角度
    rotate_angle = np.pi / 3
    for _ in range(level):
        new_points = []
        for j in range(len(u) - 1):
            start_point = u[j]
            end_point = u[j + 1]
            segment = end_point - start_point
            # 生成科赫曲线的四个新线段
            point_1 = start_point
            point_2 = start_point + segment / 3
            point_3 = point_2 + segment / 3 * np.exp(1j * rotate_angle)
            point_4 = start_point + 2 * segment / 3
            point_5 = end_point
            new_points.extend([point_1, point_2, point_3, point_4, point_5])
        u = np.array(new_points)
    return u


def minkowski_generator(u, level):
    # 初始水平线段
    u = np.array([0, 1])
    # 旋转角度
    rotate_angle = np.pi / 2
    for _ in range(level):
        new_points = []
        for j in range(len(u) - 1):
            start_point = u[j]
            end_point = u[j + 1]
            segment = end_point - start_point
            # 生成Minkowski曲线的八个新线段
            point_1 = start_point
            point_2 = start_point + segment / 4
            point_3 = point_2 + segment / 4 * np.exp(1j * rotate_angle)
            point_4 = point_2 + segment / 4 * (1 + 1j)
            point_5 = start_point + segment / 2 + segment / 4 * 1j
            point_6 = start_point + segment / 2
            point_7 = start_point + segment / 2 - segment / 4 * 1j
            point_8 = start_point + 3 * segment / 4 - segment / 4 * 1j
            point_9 = start_point + 3 * segment / 4
            point_10 = end_point
            new_points.extend([point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9, point_10])
        u = np.array(new_points)
    return u


if __name__ == "__main__":
    # 初始线段
    init_u = np.array([0, 1])
    # 创建2x2子图布局
    fig_koch, axes_koch = plt.subplots(2, 2, figsize=(10, 10))
    # 生成不同层级的科赫曲线
    for idx in range(4):
        koch_points = koch_generator(init_u, idx + 1)
        axes_koch[idx // 2, idx % 2].plot(koch_points.real, koch_points.imag, 'k-', lw=1)
        axes_koch[idx // 2, idx % 2].set_title(f"Koch Curve Level {idx + 1}")
        axes_koch[idx // 2, idx % 2].axis('equal')
        axes_koch[idx // 2, idx % 2].axis('off')
    plt.tight_layout()
    plt.show()

    # 生成不同层级的Minkowski香肠
    fig_minkowski, axes_minkowski = plt.subplots(2, 2, figsize=(10, 10))
    for idx in range(4):
        minkowski_points = minkowski_generator(init_u, idx + 1)
        axes_minkowski[idx // 2, idx % 2].plot(minkowski_points.real, minkowski_points.imag, 'k-', lw=1)
        axes_minkowski[idx // 2, idx % 2].set_title(f"Minkowski Sausage Level {idx + 1}")
        axes_minkowski[idx // 2, idx % 2].axis('equal')
        axes_minkowski[idx // 2, idx % 2].axis('off')
    plt.tight_layout()
    plt.show()

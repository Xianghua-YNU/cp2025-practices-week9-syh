"""
项目5: 盒计数法估算分形维数
实现盒计数算法计算分形图像的盒维数
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def load_and_convert_to_binary(image_path, threshold=128):
    """
    加载图像并转换为二值数组
    :param image_path: 图像文件路径
    :param threshold: 二值化阈值 (0-255)
    :return: 二值化的NumPy数组 (0和1)
    """
    image = Image.open(image_path).convert('L')
    image_as_array = np.asarray(image)
    binary_img = (image_as_array > threshold).astype(int)
    return binary_img


def perform_box_counting(binary_img, box_sizes_list):
    """
    盒计数算法实现
    :param binary_img: 二值图像数组
    :param box_sizes_list: 盒子尺寸列表
    :return: 字典 {box_size: count}
    """
    img_height, img_width = binary_img.shape
    box_count_dict = {}

    for box_size in box_sizes_list:
        num_rows = img_height // box_size
        num_cols = img_width // box_size
        box_counter = 0

        for row_index in range(num_rows):
            for col_index in range(num_cols):
                box_area = binary_img[row_index * box_size:(row_index + 1) * box_size,
                           col_index * box_size:(col_index + 1) * box_size]
                if np.any(box_area):
                    box_counter += 1

        box_count_dict[box_size] = box_counter

    return box_count_dict


def compute_fractal_dimension(binary_img, min_size=1, max_size=None, num_of_sizes=10):
    """
    计算分形维数
    :param binary_img: 二值图像数组
    :param min_size: 最小盒子尺寸
    :param max_size: 最大盒子尺寸
    :param num_of_sizes: 盒子尺寸数量
    :return: 盒维数, 拟合结果
    """
    if max_size is None:
        max_size = min(binary_img.shape) // 2

    box_sizes = np.geomspace(min_size, max_size, num=num_of_sizes, dtype=int)
    box_sizes = np.unique(box_sizes)

    box_counts = perform_box_counting(binary_img, box_sizes)

    epsilon_values = np.array(list(box_counts.keys()))
    N_epsilon_values = np.array(list(box_counts.values()))

    log_epsilon = np.log(epsilon_values)
    log_N_epsilon = np.log(N_epsilon_values)

    slope, intercept = np.polyfit(log_epsilon, log_N_epsilon, 1)
    fractal_dimension = -slope

    return fractal_dimension, (epsilon_values, N_epsilon_values, slope, intercept)


def draw_log_log_plot(epsilon_values, N_epsilon_values, slope, intercept, save_location=None):
    """
    绘制log-log图
    """
    log_epsilon = np.log(epsilon_values)
    log_N_epsilon = np.log(N_epsilon_values)

    plt.figure(figsize=(9, 7))
    plt.scatter(log_epsilon, log_N_epsilon, label='Data points')

    fitted_line = slope * log_epsilon + intercept
    plt.plot(log_epsilon, fitted_line, 'g-', label=f'Fitted line (slope={-slope:.3f})')

    plt.xlabel('log(ε)')
    plt.ylabel('log(N(ε))')
    plt.title('Box Counting Method - log-log plot')
    plt.legend()
    plt.grid(True)

    if save_location:
        plt.savefig(save_location)
    plt.show()


if __name__ == "__main__":
    # 示例用法
    IMAGE_PATH = "/Users/lixh/Library/CloudStorage/OneDrive-个人/Code/cp2025-practice-week9/images/barnsley_fern.png"

    # 1. 加载并二值化图像
    binary_image = load_and_convert_to_binary(IMAGE_PATH)

    # 2. 计算分形维数
    fractal_dim, (epsilons, N_epsilons, fit_slope, fit_intercept) = compute_fractal_dimension(binary_image)

    # 3. 输出结果
    print("盒计数结果:")
    for epsilon, N_epsilon in zip(epsilons, N_epsilons):
        print(f"ε = {epsilon:4d}, N(ε) = {N_epsilon:6d}, log(ε) = {np.log(epsilon):.3f}, log(N) = {np.log(N_epsilon):.3f}")

    print(f"\n拟合斜率: {fit_slope:.5f}")
    print(f"估算的盒维数 D = {fractal_dim:.5f}")

    # 4. 绘制log-log图
    draw_log_log_plot(epsilons, N_epsilons, fit_slope, fit_intercept, "log_log_plot.png")

import numpy as np
import matplotlib.pyplot as plt


def generate_mandelbrot(width=800, height=800, max_iter=100):
    """
    生成Mandelbrot集数据
    :param width: 图像宽度(像素)
    :param height: 图像高度(像素) 
    :param max_iter: 最大迭代次数
    :return: 2D numpy数组，包含每个点的逃逸时间
    """
    real_part = np.linspace(-2.0, 1.0, width)
    imag_part = np.linspace(-1.5, 1.5, height)
    real_grid, imag_grid = np.meshgrid(real_part, imag_part)
    complex_grid = real_grid + 1j * imag_grid

    iteration_count = np.zeros(complex_grid.shape, dtype=int)
    complex_values = np.zeros(complex_grid.shape, dtype=complex)

    for _ in range(max_iter):
        in_set = np.abs(complex_values) <= 2
        iteration_count[in_set] += 1
        complex_values[in_set] = complex_values[in_set] ** 2 + complex_grid[in_set]

    return iteration_count.T


def generate_julia(c, width=800, height=800, max_iter=100):
    """
    生成Julia集数据
    :param c: Julia集参数(复数)
    :param width: 图像宽度(像素)
    :param height: 图像高度(像素)
    :param max_iter: 最大迭代次数
    :return: 2D numpy数组，包含每个点的逃逸时间
    """
    real_part = np.linspace(-2.0, 2.0, width)
    imag_part = np.linspace(-2.0, 2.0, height)
    real_grid, imag_grid = np.meshgrid(real_part, imag_part)
    initial_complex_values = real_grid + 1j * imag_grid

    iteration_count = np.zeros(initial_complex_values.shape, dtype=int)
    complex_values = initial_complex_values.copy()

    for _ in range(max_iter):
        in_set = np.abs(complex_values) <= 2
        iteration_count[in_set] += 1
        complex_values[in_set] = complex_values[in_set] ** 2 + c

    return iteration_count.T


def plot_fractal(data, title, filename=None, cmap='magma'):
    """
    绘制分形图像
    :param data: 分形数据(2D数组)
    :param title: 图像标题
    :param filename: 保存文件名(可选)
    :param cmap: 颜色映射
    """
    plt.figure(figsize=(10, 10))
    plt.imshow(data.T, cmap=cmap, origin='lower')
    plt.title(title)
    plt.axis('off')

    if filename:
        plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.show()


if __name__ == "__main__":
    width = 800
    height = 800
    max_iter = 100

    mandelbrot_data = generate_mandelbrot(width, height, max_iter)
    plot_fractal(mandelbrot_data, "Mandelbrot Set", "mandelbrot.png")

    julia_c_values = [
        -0.8 + 0.156j,
        -0.4 + 0.6j,
        0.285 + 0.01j
    ]

    for idx, c in enumerate(julia_c_values):
        julia_data = generate_julia(c, width, height, max_iter)
        plot_fractal(julia_data, f"Julia Set (c = {c:.3f})", f"julia_{idx + 1}.png")

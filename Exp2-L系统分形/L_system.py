import matplotlib.pyplot as plt
import math


def apply_rules(axiom, rules, iterations):
    """
    生成L-System字符串
    :param axiom: 初始字符串（如"F"或"0"）
    :param rules: 规则字典，如{"F": "F+F--F+F"} 或 {"1": "11", "0": "1[0]0"}
    :param iterations: 迭代次数
    :return: 经过多轮迭代后的最终字符串
    """
    if not isinstance(axiom, str):
        raise ValueError("公理必须是字符串类型")
    if not isinstance(rules, dict):
        raise ValueError("规则必须是字典类型")
    if not isinstance(iterations, int) or iterations < 0:
        raise ValueError("迭代次数必须是非负整数")

    current_string = axiom
    for _ in range(iterations):
        new_string = ""
        for char in current_string:
            new_string += rules.get(char, char)
        current_string = new_string
    return current_string


def draw_l_system(instructions, angle, step, start_pos=(0, 0), start_angle=0, savefile=None):
    """
    根据L-System指令绘图
    :param instructions: 指令字符串（如"F+F--F+F"）
    :param angle: 每次转向的角度（度）
    :param step: 每步前进的长度
    :param start_pos: 起始坐标 (x, y)
    :param start_angle: 起始角度（0表示向右，90表示向上）
    :param savefile: 若指定则保存为图片文件，否则直接显示
    """
    if not isinstance(instructions, str):
        raise ValueError("指令必须是字符串类型")
    if not isinstance(angle, (int, float)):
        raise ValueError("角度必须是数字类型")
    if not isinstance(step, (int, float)) or step <= 0:
        raise ValueError("步长必须是正的数字类型")
    if not isinstance(start_pos, tuple) or len(start_pos) != 2:
        raise ValueError("起始位置必须是二元组")
    if not isinstance(start_angle, (int, float)):
        raise ValueError("起始角度必须是数字类型")

    x, y = start_pos
    current_angle = start_angle
    stack = []
    ax = plt.gca()

    for char in instructions:
        if char in ('F', '0', '1'):
            rad_angle = math.radians(current_angle)
            nx = x + step * math.cos(rad_angle)
            ny = y + step * math.sin(rad_angle)
            ax.plot([x, nx], [y, ny], color='black')
            x, y = nx, ny
        elif char == '+':
            current_angle += angle
        elif char == '-':
            current_angle -= angle
        elif char == '[':
            stack.append((x, y, current_angle))
            current_angle += angle
        elif char == ']':
            if not stack:
                raise IndexError("栈为空，无法弹出状态")
            x, y, current_angle = stack.pop()
            current_angle -= angle

    plt.axis('equal')
    plt.axis('off')

    if savefile:
        try:
            plt.savefig(savefile)
        except Exception as e:
            print(f"保存图片时出错: {e}")
    else:
        plt.show()


if __name__ == "__main__":
    """
    主程序示例：分别生成并绘制科赫曲线和分形二叉树
    学生可根据下方示例，调整参数体验不同分形效果
    """
    # 1. 生成并绘制科赫曲线
    koch_axiom = "F"  # 公理
    koch_rules = {"F": "F+F--F+F"}  # 规则
    koch_iterations = 3  # 迭代次数
    koch_angle = 60  # 每次转角
    koch_step = 10  # 步长
    koch_instr = apply_rules(koch_axiom, koch_rules, koch_iterations)  # 生成指令字符串
    draw_l_system(koch_instr, koch_angle, koch_step, savefile="l_system_koch.png")  # 绘图并保存

    # 2. 生成并绘制分形二叉树
    tree_axiom = "0"
    tree_rules = {"1": "11", "0": "1[0]0"}
    tree_iterations = 5
    tree_angle = 45
    tree_step = 10
    tree_instr = apply_rules(tree_axiom, tree_rules, tree_iterations)
    draw_l_system(tree_instr, tree_angle, tree_step, savefile="fractal_tree.png")

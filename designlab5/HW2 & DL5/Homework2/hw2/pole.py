import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 输入极点实数表达式
r=15/16
c = sp.sqrt(40*k - 25) / 80
expression_str = "r + c*j"  # 直接在程序中定义极点实数表达式
k = sp.symbols('k')
expression = sp.sympify(expression_str)

# 将实数表达式转换为复数表达式
# sympy 提供了 re() 和 im() 函数来分别获取实部和虚部
real_part = sp.re(expression)
imag_part = sp.im(expression)

# 输出复数表达式
complex_expression = real_part + sp.I * imag_part
print("复数表达式:", complex_expression)

# 在复平面中画出极点随 k 变化的轨迹
k_values = np.linspace(-10, 10, 400)  # k 的取值范围和步数可以根据需要调整
real_values = [sp.re(expression.subs(k, val)) for val in k_values]
imag_values = [sp.im(expression.subs(k, val)) for val in k_values]

plt.figure(figsize=(8, 6))
plt.plot(real_values, imag_values, label=f'极点轨迹 ({expression_str})')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.xlabel('实部')
plt.ylabel('虚部')
plt.title('复平面中的极点轨迹')
plt.grid(True)
plt.legend()
plt.show()

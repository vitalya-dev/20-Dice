import numpy as np

def get_icosahedron_data():
    # Вычисляем пропорцию золотого сечения
    t = (1.0 + np.sqrt(5.0)) / 2.0

    # Координаты 12 вершин икосаэдра (формат числа с плавающей точкой, 4 байта)
    vertices = np.array([
        -1.0,  t,  0.0,
         1.0,  t,  0.0,
        -1.0, -t,  0.0,
         1.0, -t,  0.0,
         0.0, -1.0,  t,
         0.0,  1.0,  t,
         0.0, -1.0, -t,
         0.0,  1.0, -t,
         t,  0.0, -1.0,
         t,  0.0,  1.0,
        -t,  0.0, -1.0,
        -t,  0.0,  1.0,
    ], dtype='f4')

    # Индексы вершин, из которых собираются 20 треугольных граней (целые числа, 4 байта)
    indices = np.array([
         0, 11,  5,
         0,  5,  1,
         0,  1,  7,
         0,  7, 10,
         0, 10, 11,
         1,  5,  9,
         5, 11,  4,
        11, 10,  2,
        10,  7,  6,
         7,  1,  8,
         3,  9,  4,
         3,  4,  2,
         3,  2,  6,
         3,  6,  8,
         3,  8,  9,
         4,  9,  5,
         2,  4, 11,
         6,  2, 10,
         8,  6,  7,
         9,  8,  1
    ], dtype='i4')

    return vertices, indices


import moderngl_window as mglw

class IcosahedronApp(mglw.WindowConfig):
    # Настройки нашего окна
    gl_version = (3, 3) # Используем OpenGL 3.3
    title = "D&D 20-sided Die (Icosahedron)"
    window_size = (800, 600)
    aspect_ratio = 800 / 600

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Здесь мы позже загрузим наши шейдеры и геометрию
        pass

    def on_render(self, time: float, frame_time: float):
        # Очищаем экран темно-серым цветом на каждом кадре
        self.ctx.clear(0.15, 0.15, 0.15, 1.0)
        
        # Здесь позже будет код для отрисовки самого кубика
        pass

# Этот блок запускает наше приложение, если мы запускаем файл напрямую
if __name__ == '__main__':
    mglw.run_window_config(IcosahedronApp)
import numpy as np
from pathlib import Path
from pyrr import Matrix44
import moderngl

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
    resource_dir = Path(".").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Загружаем шейдеры с помощью встроенного менеджера ресурсов
        self.program = self.load_program(
            vertex_shader='vertex_shader.glsl',
            fragment_shader='fragment_shader.glsl'
        )

        # Получаем массивы вершин и индексов
        vertices, indices = get_icosahedron_data()

        # Создаем буферы на видеокарте и загружаем в них данные
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.ibo = self.ctx.buffer(indices.tobytes())

        # Создаем VAO: связываем VBO с переменной 'in_position' в вершинном шейдере
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f', 'in_position')],
            index_buffer=self.ibo
        )

    def on_render(self, time: float, frame_time: float):
        # Включаем тест глубины
        self.ctx.enable(moderngl.DEPTH_TEST)
        
        # Очищаем экран темно-серым цветом
        self.ctx.clear(0.15, 0.15, 0.15, 1.0)
        
        # 1. Матрица проекции: перспектива остается прежней
        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0)
        
        # 2. Матрица трансформации (сдвиг): отодвигаем кубик на 5 единиц назад (вглубь экрана)
        translation = Matrix44.from_translation((0.0, 0.0, -5.0))
        
        # 3. Матрица вращения: плавно крутим по осям X и Y
        rotation = Matrix44.from_eulers((time * 0.5, time * 0.8, 0.0))
        
        # Комбинируем матрицы: получаем чистую матрицу МОДЕЛИ
        model = translation * rotation
        
        # Передаем готовые матрицы в шейдерную программу
        self.program['m_proj'].write(proj.astype('f4'))
        self.program['m_model'].write(model.astype('f4'))
        
        # Рисуем наш икосаэдр
        self.vao.render(moderngl.TRIANGLES)
# Этот блок запускает наше приложение, если мы запускаем файл напрямую
if __name__ == '__main__':
    mglw.run_window_config(IcosahedronApp)
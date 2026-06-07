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
        
        # 1. Загружаем шейдеры для самого кубика
        self.program = self.load_program(
            vertex_shader='vertex_shader.glsl',
            geometry_shader='geometry_shader.glsl',
            fragment_shader='fragment_shader.glsl'
        )
        
        # 2. Загружаем шейдеры для пост-эффекта (пикселизация)
        self.post_program = self.load_program(
            vertex_shader='post_vertex.glsl',
            fragment_shader='post_fragment.glsl'
        )

        # 3. Геометрия кубика
        vertices, indices = get_icosahedron_data()
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.ibo = self.ctx.buffer(indices.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f', 'in_position')],
            index_buffer=self.ibo
        )
        
        # --- 4. НАСТРОЙКА FBO (НЕВИДИМЫЙ ХОЛСТ) ---
        # Создаем пустую текстуру размером с наше окно
        self.render_texture = self.ctx.texture(self.window_size, 4)
        # Создаем буфер глубины (чтобы кубик был объемным в текстуре)
        self.depth_attachment = self.ctx.depth_renderbuffer(self.window_size)
        # Объединяем их в FBO
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.render_texture],
            depth_attachment=self.depth_attachment
        )
        
        # --- 5. ГЕОМЕТРИЯ ЭКРАНА ---
        # Создаем плоский прямоугольник на весь экран
        from moderngl_window import geometry
        self.quad_vao = geometry.quad_fs()
        
        # Говорим шейдеру пост-обработки брать картинку из 0-го слота текстур
        self.post_program['screen_texture'].value = 0

    def on_render(self, time: float, frame_time: float):
        # --- ЭТАП 1: РИСУЕМ КУБИК В НЕВИДИМУЮ ТЕКСТУРУ ---
        # Переключаем "кисть" на наш FBO
        self.fbo.use()
        
        # Включаем 3D-тест глубины и очищаем текстуру
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(0.15, 0.15, 0.15, 1.0)
        
        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0)
        translation = Matrix44.from_translation((0.0, 0.0, -5.0))
        rotation = Matrix44.from_eulers((time * 0.5, time * 0.8, 0.0))
        model = translation * rotation
        
        self.program['m_proj'].write(proj.astype('f4'))
        self.program['m_model'].write(model.astype('f4'))
        
        # Рисуем икосаэдр в текстуру
        self.vao.render(moderngl.TRIANGLES)
        
        # --- ЭТАП 2: РИСУЕМ ТЕКСТУРУ НА ГЛАВНЫЙ ЭКРАН ---
        # Возвращаем "кисть" обратно на монитор
        self.ctx.screen.use()
        
        # Отключаем тест глубины (пост-эффект - это просто 2D картинка)
        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        
        # Привязываем нашу отрендеренную текстуру кубика к нулевому слоту
        self.render_texture.use(location=0)
        
        # Рисуем плоский прямоугольник, используя шейдер пост-обработки (там живет наша пикселизация)
        self.quad_vao.render(self.post_program)
        
# Этот блок запускает наше приложение, если мы запускаем файл напрямую
if __name__ == '__main__':
    mglw.run_window_config(IcosahedronApp)
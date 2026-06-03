#version 330

// Входящие данные: координаты вершины
in vec3 in_position;

// Матрицы для управления камерой и перспективой
uniform mat4 m_proj;
uniform mat4 m_modelview;

// Переменная для передачи данных во фрагментный шейдер
out vec3 v_position;

void main() {
    // Вычисляем итоговую позицию вершины на экране
    gl_Position = m_proj * m_modelview * vec4(in_position, 1.0);
    // Передаем исходную позицию дальше для расчета цвета
    v_position = in_position;
}
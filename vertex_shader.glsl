#version 330

// Входящие данные: координаты вершины
in vec3 in_position;

// Матрицы для управления камерой и перспективой
uniform mat4 m_proj;
uniform mat4 m_model;

// Переименовали переменную для передачи в ГЕОМЕТРИЧЕСКИЙ шейдер
out vec3 v_geom_position;

void main() {
    // Вычисляем итоговую позицию вершины на экране
    gl_Position = m_proj * m_model * vec4(in_position, 1.0);
    // Передаем исходную позицию дальше
    v_geom_position = in_position;
}
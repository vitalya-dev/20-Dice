#version 330

// Сообщаем видеокарте, что на вход ждем треугольники (по 3 вершины)
layout (triangles) in;
// На выходе тоже отдаем треугольники
layout (triangle_strip, max_vertices = 3) out;

// Входные данные от вершинного шейдера (теперь это массив из 3 элементов)
in vec3 v_geom_position[];

// Выходные данные для фрагментного шейдера
out vec3 v_position;
out vec3 v_barycentric;

void main() {
    // Обрабатываем первый угол треугольника
    gl_Position = gl_in[0].gl_Position;
    v_position = v_geom_position[0];
    v_barycentric = vec3(1.0, 0.0, 0.0); // 100% первый угол
    EmitVertex();

    // Обрабатываем второй угол треугольника
    gl_Position = gl_in[1].gl_Position;
    v_position = v_geom_position[1];
    v_barycentric = vec3(0.0, 1.0, 0.0); // 100% второй угол
    EmitVertex();

    // Обрабатываем третий угол треугольника
    gl_Position = gl_in[2].gl_Position;
    v_position = v_geom_position[2];
    v_barycentric = vec3(0.0, 0.0, 1.0); // 100% третий угол
    EmitVertex();

    // Завершаем сборку треугольника
    EndPrimitive();
}
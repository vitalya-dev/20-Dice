#version 330

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in vec3 v_geom_position[];

// Теперь мы передаем готовую нормаль вместо позиции
out vec3 v_normal;
out vec3 v_barycentric;

void main() {
    // Вычисляем два вектора (края нашего треугольника)
    vec3 edge1 = v_geom_position[1] - v_geom_position[0];
    vec3 edge2 = v_geom_position[2] - v_geom_position[0];
    
    // Векторное произведение дает перпендикуляр (нормаль) ко всей грани
    vec3 face_normal = normalize(cross(edge1, edge2));

    // Обрабатываем первый угол
    gl_Position = gl_in[0].gl_Position;
    v_normal = face_normal;
    v_barycentric = vec3(1.0, 0.0, 0.0);
    EmitVertex();

    // Обрабатываем второй угол
    gl_Position = gl_in[1].gl_Position;
    v_normal = face_normal;
    v_barycentric = vec3(0.0, 1.0, 0.0);
    EmitVertex();

    // Обрабатываем третий угол
    gl_Position = gl_in[2].gl_Position;
    v_normal = face_normal;
    v_barycentric = vec3(0.0, 0.0, 1.0);
    EmitVertex();

    EndPrimitive();
}
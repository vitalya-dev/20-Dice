#version 330

// Получаем данные от геометрического шейдера
in vec3 v_normal;
in vec3 v_barycentric;

out vec4 f_color;

uniform mat4 m_model;

void main() {
    // Нормаль уже плоская для всей грани, переводим её в model space
    vec3 normal = normalize(mat3(m_model) * v_normal);
    
    // Задаем направление воображаемого источника света
    vec3 light_dir = normalize(vec3(1.0, 1.0, 1.0));
    
    // Рассчитываем освещенность: базовая тень (0.3) + прямой свет (до 0.7)
    float lum = max(dot(normal, light_dir), 0.0) * 0.7 + 0.3; 
    
    // Задаем цвет кубика (красный) и применяем освещенность
    vec3 base_color = vec3(0.8, 0.1, 0.1); 
    vec3 final_color = base_color * lum;

    // --- ЛОГИКА ОБВОДКИ ---
    // Если пиксель находится очень близко к краю, закрашиваем его в черный
    if (v_barycentric.x < 0.02 || v_barycentric.y < 0.02 || v_barycentric.z < 0.02) {
        final_color = vec3(0.0, 0.0, 0.0);
    }
    
    f_color = vec4(final_color, 1.0);
}
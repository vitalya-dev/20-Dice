#version 330

// Получаем данные от вершинного шейдера
in vec3 v_position;

// Итоговый цвет пикселя на экране
out vec4 f_color;

void main() {
    // Вычисляем направление поверхности (нормаль)
    vec3 normal = normalize(v_position);
    
    // Задаем направление воображаемого источника света
    vec3 light_dir = normalize(vec3(1.0, 1.0, 1.0));
    
    // Рассчитываем освещенность: базовая тень (0.3) + прямой свет (до 0.7)
    float lum = max(dot(normal, light_dir), 0.0) * 0.7 + 0.3; 
    
    // Задаем цвет кубика (красный) и применяем освещенность
    vec3 base_color = vec3(0.8, 0.1, 0.1); 
    f_color = vec4(base_color * lum, 1.0);
}
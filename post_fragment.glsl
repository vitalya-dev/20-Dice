#version 330

in vec2 v_uv;
out vec4 f_color;

// Текстура, в которую мы предварительно отрендерим наш кубик
uniform sampler2D screen_texture;

void main() {
    // Твоя логика пикселизации
    float pixels = 75.0;
    vec2 pixel_uv = floor(v_uv * pixels) / pixels;

    // Берем цвет из текстуры по новым "квадратным" координатам
    f_color = texture(screen_texture, pixel_uv);
}
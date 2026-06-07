#version 330

// Геометрия прямоугольника на весь экран передаст нам эти данные
in vec3 in_position;
in vec2 in_texcoord_0;

// Передаем UV-координаты во фрагментный шейдер
out vec2 v_uv;

void main() {
    gl_Position = vec4(in_position, 1.0);
    v_uv = in_texcoord_0;
}
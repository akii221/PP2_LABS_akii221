import pygame  # Импортируем библиотеку pygame, которая используется для создания графических интерфейсов и игр.

def main():
    pygame.init()  # Инициализируем все модули pygame.
    screen = pygame.display.set_mode((640, 480))  # Создаем экран с разрешением 640x480 пикселей.
    clock = pygame.time.Clock()  # Создаем объект для контроля частоты обновления экрана.

    radius = 15  # Радиус кисти и ластика.
    mode = 'blue'  # Начальный цвет рисования — синий.
    tool = 'brush'  # Выбран инструмент кисти (brush).
    points = []  # Список для хранения всех точек, нарисованных с помощью кисти.
    shapes = []  # Список для хранения всех нарисованных фигур.
    drawing = False  # Флаг, указывающий, рисуем ли мы в данный момент.
    start_pos = None  # Начальная позиция для рисования фигур (например, прямоугольников).

    while True:
        pressed = pygame.key.get_pressed()  # Получаем текущие нажатия клавиш.
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]  # Проверяем, нажата ли клавиша ALT.
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]  # Проверяем, нажата ли клавиша CTRL.
        
        for event in pygame.event.get():  # Обрабатываем все события.
            if event.type == pygame.QUIT:  # Если событие — выход из программы.
                return
            if event.type == pygame.KEYDOWN:  # Если нажата клавиша.
                # Закрытие программы с использованием комбинаций клавиш.
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                # Выбор цвета инструмента.
                if event.key == pygame.K_r:
                    mode = 'red'  # Выбираем красный цвет.
                elif event.key == pygame.K_g:
                    mode = 'green'  # Выбираем зеленый цвет.
                elif event.key == pygame.K_b:
                    mode = 'blue'  # Выбираем синий цвет.

                # Выбор инструмента.
                if event.key == pygame.K_t:  # Прямоугольник.
                    tool = 'rectangle'
                elif event.key == pygame.K_c:  # Круг.
                    tool = 'circle'
                elif event.key == pygame.K_e:  # Ластик.
                    tool = 'eraser'
                elif event.key == pygame.K_p:  # Кисть.
                    tool = 'brush'
                elif event.key == pygame.K_s:  # Квадрат.
                    tool = 'square'
                elif event.key == pygame.K_y:  # Прямоугольный треугольник.
                    tool = 'right_triangle'
                elif event.key == pygame.K_u:  # Равносторонний треугольник.
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_h:  # Ромб.
                    tool = 'rhombus'
                
                # Начать рисование при нажатии пробела.
                if event.key == pygame.K_SPACE:
                    drawing = True
                    start_pos = pygame.mouse.get_pos()  # Запоминаем начальную позицию мыши для рисования.

            if event.type == pygame.KEYUP:  # Когда клавиша отпускается.
                if event.key == pygame.K_SPACE:  # Если отпускаем пробел.
                    drawing = False  # Прекращаем рисование.
                    # Если рисуем фигуру (не кисть или ластик), добавляем фигуру в список.
                    if tool in ('rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus') and start_pos:
                        end_pos = pygame.mouse.get_pos()  # Получаем конечную позицию мыши.
                        shapes.append((tool, start_pos, end_pos, mode))  # Добавляем фигуру в список.

            if event.type == pygame.MOUSEMOTION:  # Обработка движения мыши.
                position = event.pos  # Текущая позиция мыши.
                if drawing and tool == 'brush':  # Если рисуем кистью, добавляем точки в список.
                    points.append(position)
                    points = points[-256:]  # Ограничиваем список 256 точками (для производительности).

                if drawing and tool == 'eraser':  # Если рисуем ластиком, стираем точки и фигуры.
                    erase(points, position, radius)  # Удаляем точки, попадающие в радиус ластика.
                    erase_shapes(shapes, position, radius)  # Удаляем фигуры, попадающие в радиус ластика.

        screen.fill((0, 0, 0))  # Заполняем экран черным цветом (фон).

        # Рисуем все фигуры.
        for shape in shapes:
            drawShape(screen, *shape)

        # Рисуем линии кистью.
        for i in range(len(points) - 1):
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
        
        pygame.display.flip()  # Обновляем экран.
        clock.tick(60)  # Ограничиваем частоту обновлений экрана до 60 кадров в секунду.

# Функция для рисования линии между двумя точками с плавной заливкой.
def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))  # Модифицируем значения цветов для плавности.
    c2 = max(0, min(255, 2 * index))

    # Выбираем цвет в зависимости от выбранного режима.
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    dx, dy = start[0] - end[0], start[1] - end[1]  # Разница между начальной и конечной точками.
    iterations = max(abs(dx), abs(dy))  # Определяем количество итераций для рисования линии.

    for i in range(iterations):
        progress = i / iterations  # Рассчитываем прогресс линии.
        aprogress = 1 - progress
        # Рассчитываем координаты промежуточных точек линии.
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)  # Рисуем маленькие окружности для линии.

# Функция для рисования различных фигур.
def drawShape(screen, shape, start, end, color_mode):
    colors = {'blue': (0, 0, 255), 'red': (255, 0, 0), 'green': (0, 255, 0)}  # Словарь для цветов.
    color = colors.get(color_mode, (255, 255, 255))  # Получаем цвет по выбранному режиму, по умолчанию — белый.

    if shape == 'rectangle':  # Если фигура прямоугольник.
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))  # Определяем прямоугольник.
        pygame.draw.rect(screen, color, rect, 2)  # Рисуем прямоугольник.

    elif shape == 'circle':  # Если фигура круг.
        center = start
        radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)  # Вычисляем радиус.
        pygame.draw.circle(screen, color, center, radius, 2)  # Рисуем круг.

    elif shape == 'square':  # Если фигура квадрат.
        x1, y1 = start
        x2, y2 = end
        side_length = min(abs(x2 - x1), abs(y2 - y1))  # Вычисляем сторону квадрата.
        pygame.draw.rect(screen, color, pygame.Rect(x1, y1, side_length, side_length), 2)  # Рисуем квадрат.

    elif shape == 'right_triangle':  # Если фигура прямоугольный треугольник.
        x1, y1 = start
        x2, y2 = end
        pygame.draw.polygon(screen, color, [(x1, y1), (x1, y2), (x2, y2)], 2)  # Рисуем прямоугольный треугольник.

    elif shape == 'equilateral_triangle':  # Если фигура равносторонний треугольник.
        x1, y1 = start
        x2, y2 = end
        side_length = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)  # Вычисляем длину стороны.
        height = int(side_length * (3**0.5) / 2)  # Вычисляем высоту.
        pygame.draw.polygon(screen, color, [(x1, y1), (x1 + side_length, y1), (x1 + side_length / 2, y1 - height)], 2)

    elif shape == 'rhombus':  # Если фигура ромб.
        x1, y1 = start
        x2, y2 = end
        width = abs(x2 - x1)  # Ширина ромба.
        height = abs(y2 - y1)  # Высота ромба.
        pygame.draw.polygon(screen, color, [(x1, y1 + height / 2), (x1 + width / 2, y1), (x2, y1 + height / 2), (x1 + width / 2, y2)], 2)

# Функция для удаления точек с помощью ластика.
def erase(points, position, radius):
    points[:] = [p for p in points if (p[0] - position[0])**2 + (p[1] - position[1])**2 > radius**2]

# Функция для удаления фигур с помощью ластика.
def erase_shapes(shapes, position, radius):
    shapes[:] = [shape for shape in shapes if not is_inside_eraser(shape, position, radius)]

# Функция, которая проверяет, попадает ли фигура в зону стирания.
def is_inside_eraser(shape, position, radius):
    _, start, end, _ = shape
    x, y = position
    if shape[0] == 'rectangle':
        x1, y1 = start
        x2, y2 = end
        return x1 - radius < x < x2 + radius and y1 - radius < y < y2 + radius  # Проверка для прямоугольника.
    elif shape[0] == 'circle':
        cx, cy = start
        r = int(((end[0] - cx) ** 2 + (end[1] - cy) ** 2) ** 0.5)  # Радиус для круга.
        return (cx - x) ** 2 + (cy - y) ** 2 < (r + radius) ** 2  # Проверка для круга.
    elif shape[0] == 'square':
        x1, y1 = start
        x2, y2 = end
        side_length = min(abs(x2 - x1), abs(y2 - y1))  # Сторона квадрата.
        return x1 - radius < x < x1 + side_length + radius and y1 - radius < y < y1 + side_length + radius  # Проверка для квадрата.
    elif shape[0] == 'right_triangle':
        x1, y1 = start
        x2, y2 = end
        return x1 - radius < x < x2 + radius and y1 - radius < y < y2 + radius  # Проверка для треугольника.
    elif shape[0] == 'equilateral_triangle':
        x1, y1 = start
        x2, y2 = end
        side_length = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)  # Длина стороны для треугольника.
        height = int(side_length * (3**0.5) / 2)  # Высота для треугольника.
        return x1 - radius < x < x1 + side_length + radius and y1 - radius < y < y1 + height + radius  # Проверка для треугольника.
    elif shape[0] == 'rhombus':
        x1, y1 = start
        x2, y2 = end
        width = abs(x2 - x1)  # Ширина ромба.
        height = abs(y2 - y1)  # Высота ромба.
        return x1 - radius < x < x2 + radius and y1 - radius < y < y2 + radius  # Проверка для ромба.
    return False  # Возвращаем False, если фигура не попадает в радиус ластика.

main()  # Запуск основной функции.

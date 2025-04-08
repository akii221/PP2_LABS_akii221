import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    tool = 'brush'  # 'brush', 'rectangle', 'circle', 'eraser', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus'
    points = []
    shapes = []  # Список для хранения фигур
    drawing = False
    start_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                # Выбор цвета
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # Выбор инструмента
                if event.key == pygame.K_t:  # Прямоугольник
                    tool = 'rectangle'
                elif event.key == pygame.K_c:  # Круг
                    tool = 'circle'
                elif event.key == pygame.K_e:  # Ластик
                    tool = 'eraser'
                elif event.key == pygame.K_p:  # Кисть
                    tool = 'brush'
                elif event.key == pygame.K_s:  # Квадрат
                    tool = 'square'
                elif event.key == pygame.K_y:  # Прямоугольный треугольник
                    tool = 'right_triangle'
                elif event.key == pygame.K_u:  # Равносторонний треугольник
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_h:  # Ромб
                    tool = 'rhombus'
                
                # Начать рисование
                if event.key == pygame.K_SPACE:
                    drawing = True
                    start_pos = pygame.mouse.get_pos()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    drawing = False
                    if tool in ('rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus') and start_pos:
                        end_pos = pygame.mouse.get_pos()
                        shapes.append((tool, start_pos, end_pos, mode))  # Добавляем фигуру

            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if drawing and tool == 'brush':
                    points.append(position)
                    points = points[-256:]

                if drawing and tool == 'eraser':
                    erase(points, position, radius)
                    erase_shapes(shapes, position, radius)

        screen.fill((0, 0, 0))

        # Рисуем все фигуры
        for shape in shapes:
            drawShape(screen, *shape)

        # Рисуем кисть
        for i in range(len(points) - 1):
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
        
        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    dx, dy = start[0] - end[0], start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def drawShape(screen, shape, start, end, color_mode):
    colors = {'blue': (0, 0, 255), 'red': (255, 0, 0), 'green': (0, 255, 0)}
    color = colors.get(color_mode, (255, 255, 255))

    if shape == 'rectangle':
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, color, rect, 2)
    elif shape == 'circle':
        center = start
        radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
        pygame.draw.circle(screen, color, center, radius, 2)
    elif shape == 'square':
        x1, y1 = start
        x2, y2 = end
        side_length = min(abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, color, pygame.Rect(x1, y1, side_length, side_length), 2)
    elif shape == 'right_triangle':
        x1, y1 = start
        x2, y2 = end
        pygame.draw.polygon(screen, color, [(x1, y1), (x1, y2), (x2, y2)], 2)
    elif shape == 'equilateral_triangle':
        x1, y1 = start
        x2, y2 = end
        side_length = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
        height = int(side_length * (3**0.5) / 2)
        pygame.draw.polygon(screen, color, [(x1, y1), (x1 + side_length, y1), (x1 + side_length / 2, y1 - height)], 2)
    elif shape == 'rhombus':
        x1, y1 = start
        x2, y2 = end
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        pygame.draw.polygon(screen, color, [(x1, y1 + height / 2), (x1 + width / 2, y1), (x2, y1 + height / 2), (x1 + width / 2, y2)], 2)

def erase(points, position, radius):
    """Удаляет точки, находящиеся в зоне ластика."""
    points[:] = [p for p in points if (p[0] - position[0])**2 + (p[1] - position[1])**2 > radius**2]

def erase_shapes(shapes, position, radius):
    """Удаляет фигуры, если центр попадает в зону ластика."""
    shapes[:] = [shape for shape in shapes if not is_inside_eraser(shape, position, radius)]

def is_inside_eraser(shape, position, radius):
    """Проверяет, попадает ли фигура в зону стирания."""
    _, start, end, _ = shape
    x, y = position
    if shape[0] == 'rectangle':
        x1, y1 = start
        x2, y2 = end
        return x1 - radius < x < x2 + radius and y1 - radius < y < y2 + radius
    elif shape[0] == 'circle':
        cx, cy = start
        r = int(((end[0] - cx) ** 2 + (end[1] - cy) ** 2) ** 0.5)
        return (cx - x) ** 2 + (cy - y) ** 2 < (r + radius) ** 2
    elif shape[0] == 'square':
        x1, y1 = start
        x2, y2 = end
        side_length = min(abs(x2 - x1), abs(y2 - y1))
        return x1 - radius < x < x1 + side_length + radius and y1 - radius < y < y1 + side_length + radius
    elif shape[0] == 'right_triangle':
        x1, y1 = start
        x2, y2 = end
        return x1 - radius < x < x2 + radius and y1 - radius < y < y2 + radius
    elif shape[0] == 'equilateral_triangle':
        x1, y1 = start
        x2, y2 = end
        side_length = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
        height = int(side_length * (3**0.5) / 2)
        return x1 - radius < x < x1 + side_length + radius and y1 - radius < y < y1 + height + radius
    elif shape[0] == 'rhombus':
        x1, y1 = start
        x2, y2 = end
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        return x1 - radius < x < x2 + radius and y1 - radius < y < y2 + radius
    return False

main()

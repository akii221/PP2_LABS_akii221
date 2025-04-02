import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    points = []
    drawing_mode = 'free_draw'
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
                    screen.fill((0, 0, 0))  # Clear screen with black

                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                if event.key == pygame.K_f:
                    drawing_mode = 'free_draw'
                elif event.key == pygame.K_e:
                    drawing_mode = 'eraser'
                elif event.key == pygame.K_c:
                    drawing_mode = 'circle'
                elif event.key == pygame.K_v:
                    drawing_mode = 'rectangle'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if drawing_mode == 'circle':
                        pygame.draw.circle(screen, get_color(mode), start_pos, radius)
                    elif drawing_mode == 'rectangle' and start_pos:
                        end_pos = event.pos
                        pygame.draw.rect(screen, get_color(mode), (*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), 2)
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if drawing_mode == 'free_draw' and start_pos:
                    points.append(position)
                    points = points[-256:]
                elif drawing_mode == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0), position, radius)

        if drawing_mode == 'free_draw':
            for i in range(len(points) - 1):
                draw_line_between(screen, i, points[i], points[i + 1], radius, mode)

        pygame.display.flip()
        clock.tick(60)

def draw_line_between(screen, index, start, end, width, color_mode):
    color = get_color(color_mode)
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations
        x = int((1 - progress) * start[0] + progress * end[0])
        y = int((1 - progress) * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

def get_color(color_mode):
    colors = {'blue': (0, 0, 255), 'red': (255, 0, 0), 'green': (0, 255, 0)}
    return colors.get(color_mode, (255, 255, 255))

main()

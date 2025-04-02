import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    points = []
    drawing_mode = 'free_draw'  # Possible values: 'free_draw', 'rectangle', 'circle', 'eraser'
    start_pos = None
    end_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    screen.fill((0, 0, 0))  # Clear screen with Escape key

                # Choose color
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # Choose drawing mode
                if event.key == pygame.K_f:
                    drawing_mode = 'free_draw'
                elif event.key == pygame.K_e:
                    drawing_mode = 'eraser'
                elif event.key == pygame.K_c:
                    drawing_mode = 'circle'
                elif event.key == pygame.K_v:
                    drawing_mode = 'rectangle'

                # Control start position for shapes
                if event.key == pygame.K_UP:
                    if start_pos:
                        start_pos = (start_pos[0], max(0, start_pos[1] - 5))
                elif event.key == pygame.K_DOWN:
                    if start_pos:
                        start_pos = (start_pos[0], min(screen.get_height(), start_pos[1] + 5))
                elif event.key == pygame.K_LEFT:
                    if start_pos:
                        start_pos = (max(0, start_pos[0] - 5), start_pos[1])
                elif event.key == pygame.K_RIGHT:
                    if start_pos:
                        start_pos = (min(screen.get_width(), start_pos[0] + 5), start_pos[1])

                # Adjust radius
                if event.key == pygame.K_MINUS:
                    radius = max(1, radius - 1)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    radius += 1

            if event.type == pygame.KEYUP:
                # Complete drawing for circle or rectangle
                if event.key == pygame.K_RETURN:
                    if drawing_mode == 'circle' and start_pos:
                        pygame.draw.circle(screen, get_color(mode), start_pos, radius)
                    elif drawing_mode == 'rectangle' and start_pos and end_pos:
                        pygame.draw.rect(screen, get_color(mode), (*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), 2)
                    start_pos = None
                    end_pos = None

            # Mouse button events for drawing
            if event.type == pygame.MOUSEBUTTONDOWN:
                if drawing_mode == 'free_draw':
                    points = [event.pos]  # Start new line
                elif drawing_mode in ['circle', 'rectangle']:
                    start_pos = event.pos
                elif drawing_mode == 'eraser':
                    start_pos = event.pos

            elif event.type == pygame.MOUSEMOTION:
                if drawing_mode == 'free_draw' and event.buttons[0]:
                    points.append(event.pos)  # Add point to line
                elif drawing_mode == 'eraser' and event.buttons[0]:
                    start_pos = event.pos  # Eraser follows the mouse

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing_mode == 'circle' and start_pos:
                    end_pos = event.pos  # End point for circle
                    pygame.draw.circle(screen, get_color(mode), start_pos, radius)
                elif drawing_mode == 'rectangle' and start_pos:
                    end_pos = event.pos  # End point for rectangle
                    pygame.draw.rect(screen, get_color(mode), (*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), 2)

        # Logic for free drawing
        if drawing_mode == 'free_draw' and pressed[pygame.K_SPACE] and len(points) > 1:
            pygame.draw.lines(screen, get_color(mode), False, points, radius)

        # Eraser logic
        if drawing_mode == 'eraser' and pressed[pygame.K_SPACE] and start_pos:
            pygame.draw.circle(screen, (0, 0, 0), start_pos, radius)

        pygame.display.flip()
        clock.tick(60)

def get_color(color_mode):
    colors = {'blue': (0, 0, 255), 'red': (255, 0, 0), 'green': (0, 255, 0)}
    return colors.get(color_mode, (255, 255, 255))

main()

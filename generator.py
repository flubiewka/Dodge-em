import sys

import numpy as np
import pygame

pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

points = []
TRACK_WIDTH = 300
selected_point_index = None
CLICK_RADIUS = 15


def catmull_rom_spline(P0, P1, P2, P3, num_points=100, alpha=0.5):
    P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])

    def tj(pi, pj):
        return np.linalg.norm(pj - pi) ** alpha + 1e-6

    t0 = 0.0
    t1 = t0 + tj(P0, P1)
    t2 = t1 + tj(P1, P2)
    t3 = t2 + tj(P2, P3)

    t = np.linspace(t1, t2, num_points)
    t = t[:, np.newaxis]

    A1 = (t1 - t) / (t1 - t0) * P0 + (t - t0) / (t1 - t0) * P1
    A2 = (t2 - t) / (t2 - t1) * P1 + (t - t1) / (t2 - t1) * P2
    A3 = (t3 - t) / (t3 - t2) * P2 + (t - t2) / (t3 - t2) * P3

    B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
    B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3

    C = (t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2
    return C.tolist()


def generate_smooth_track(pts):
    if len(pts) < 3:
        return pts

    smooth_pts = []
    extended_pts = [pts[-1]] + pts + [pts[0], pts[1]]

    for i in range(1, len(extended_pts) - 2):
        segment = catmull_rom_spline(
            extended_pts[i - 1],
            extended_pts[i],
            extended_pts[i + 1],
            extended_pts[i + 2],
        )
        smooth_pts.extend(segment[:-1])

    smooth_pts.append(extended_pts[-2])
    return [(int(p[0]), int(p[1])) for p in smooth_pts]


def draw_track_solid(surface, pts, width, track_color, border_color):
    # Рисуем круги на всех стыках для закругленных углов
    if border_color:
        for p in pts:
            pygame.draw.circle(surface, border_color, p, (width + 4) // 2)
        if len(pts) >= 2:
            pygame.draw.lines(surface, border_color, True, pts, width + 4)

    for p in pts:
        pygame.draw.circle(surface, track_color, p, width // 2)
    if len(pts) >= 2:
        pygame.draw.lines(surface, track_color, True, pts, width)


running = True
pan_offset = [0, 0]
zoom = 1.0
is_panning = False
last_mouse_pos = (0, 0)

while running:
    screen.fill((40, 40, 40))

    scaled_track_width = int(TRACK_WIDTH * zoom)
    smooth_points = generate_smooth_track(points) if len(points) >= 3 else points
    rendered_smooth = [
        (int(p[0] * zoom + pan_offset[0]), int(p[1] * zoom + pan_offset[1]))
        for p in smooth_points
    ]

    if len(rendered_smooth) >= 3:
        draw_track_solid(
            screen, rendered_smooth, scaled_track_width, (80, 80, 80), (200, 200, 200)
        )
    elif len(rendered_smooth) > 1:
        pygame.draw.lines(
            screen, (80, 80, 80), False, rendered_smooth, max(1, scaled_track_width)
        )

    for i, p in enumerate(points):
        color = (255, 193, 7) if i == selected_point_index else (255, 87, 34)
        rendered_p = (
            int(p[0] * zoom + pan_offset[0]),
            int(p[1] * zoom + pan_offset[1]),
        )
        pygame.draw.circle(screen, color, rendered_p, max(1, int(6 * zoom)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            world_x = (mx - pan_offset[0]) / zoom
            world_y = (my - pan_offset[1]) / zoom

            zoom += event.y * 0.1
            zoom = max(0.1, min(zoom, 10.0))

            pan_offset[0] = mx - world_x * zoom
            pan_offset[1] = my - world_y * zoom

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = (
                    (event.pos[0] - pan_offset[0]) / zoom,
                    (event.pos[1] - pan_offset[1]) / zoom,
                )
                clicked_on_point = False

                for i, p in enumerate(points):
                    if (
                        pygame.math.Vector2(p).distance_to(mouse_pos) * zoom
                        < CLICK_RADIUS
                    ):
                        selected_point_index = i
                        clicked_on_point = True
                        break

                if not clicked_on_point:
                    points.append(mouse_pos)
                    selected_point_index = len(points) - 1

            elif event.button == 2 and points:
                # Удаление точки теперь на среднюю кнопку мыши (колесико)
                points.pop()
                selected_point_index = None

            elif event.button == 3:
                is_panning = True
                last_mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected_point_index = None
            elif event.button == 3:
                is_panning = False

        elif event.type == pygame.MOUSEMOTION:
            if is_panning:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                pan_offset[0] += dx
                pan_offset[1] += dy
                last_mouse_pos = event.pos

            if selected_point_index is not None:
                points[selected_point_index] = (
                    (event.pos[0] - pan_offset[0]) / zoom,
                    (event.pos[1] - pan_offset[1]) / zoom,
                )

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(smooth_points) >= 3:
                # Находим минимальные координаты среди всех точек
                min_x = min(p[0] for p in smooth_points)
                min_y = min(p[1] for p in smooth_points)

                # Добавляем небольшой запас (половина толщины трассы), чтобы трасса не касалась края (0)
                padding = (TRACK_WIDTH + 40) // 2

                # Смещаем все точки вправо и вниз
                norm_points = [
                    (p[0] - min_x + padding, p[1] - min_y + padding)
                    for p in smooth_points
                ]

                print("\ndef draw_smooth_track(surface, camera_pos):")
                print(f"    track_points = {norm_points}")
                print(
                    "    offset_points = [(p[0] - camera_pos.x, p[1] - camera_pos.y) for p in track_points]"
                )
                print(f"    width = {TRACK_WIDTH}")
                print("    if len(offset_points) >= 2:")
                print("        for p in offset_points:")
                print(
                    "            pygame.draw.circle(surface, (200, 200, 200), p, (width + 40) // 2)"
                )
                print(
                    "        pygame.draw.lines(surface, (200, 200, 200), True, offset_points, width + 40)"
                )
                print("        for p in offset_points:")
                print(
                    "            pygame.draw.circle(surface, (80, 80, 80), p, width // 2)"
                )
                print(
                    "        pygame.draw.lines(surface, (80, 80, 80), True, offset_points, width)"
                )
                running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

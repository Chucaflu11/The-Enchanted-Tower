import pygame

from setup import WHITE, BLACK, RUSSIAN_VIOLET, RUSSIAN_VIOLET_LIGHT, PERSIAN_INDIGO, TEKHELET, FRENCH_VIOLET, AMETHYST, HELIOTROPE, MAUVE

def create_bar_chart_image(data, width, height):
    chart_image = pygame.Surface((width, height))
    chart_image.fill(TEKHELET)  #Background color

    font = pygame.font.Font(None, 12)

    num_values = len(data)
    num_groups = num_values // 2  # Two bars per group
    total_gap = width - 120  # Total space available for all bars and gaps
    bar_width = total_gap // (6 * num_groups + 1) 
    gap = bar_width // 2  # Space between bars
    group_space = 3 * gap + 2 * bar_width

    x = gap + 60  # x-coordinate of first bar
    y = height - 50

    max_data = max(data)
    y_scale = 10 * ((max_data // 10) + 1) # Round up to nearest multiple of 10

    # Draw axes
    pygame.draw.line(chart_image, BLACK, (60, y), (width - 60, y), 2)  # X
    pygame.draw.line(chart_image, BLACK, (60, 50), (60, y), 2)  # Y

    for i in range(num_groups):
        x += i * group_space

        for j in range(2):
            bar_height = (data[2*i + j] / y_scale) * (y - 50) 
            pygame.draw.rect(chart_image, MAUVE, (x, y - bar_height, bar_width, bar_height))

            # Draw bar value
            text = font.render(str(data[2*i + j]), True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (x + bar_width / 2, y + 10)
            chart_image.blit(text, text_rect)

            x += bar_width + gap

    y_scale = max(data)

    if all(value == 0 for value in data):
        y_scale = 1  # Avoid division by zero

    y_labels = []
    num_labels = min(y_scale // 20 + 1, 11)  # Maximum of 10 labels
    for i in range(num_labels):
        if (num_labels > 1):
            label = y_scale * i // (num_labels - 1)
        else:
            label = y_scale * i // (num_labels)
        y_labels.append(label)

    # Draw y-axis labels
    for label in y_labels:
        text = font.render(str(label), True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (30, height - 50 - (label / y_scale) * (height - 100))
        chart_image.blit(text, text_rect)

    return chart_image
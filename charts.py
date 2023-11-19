import pygame

#Funcion para crear imagenes de graficos de barras
def create_bar_chart_image(data, width, height):
    chart_image = pygame.Surface((width, height))
    chart_image.fill((60, 9, 108))  # Rellenar el fondo con un color

    font = pygame.font.Font(None, 12)  # Tamaño de fuente 12

    num_values = len(data)
    num_groups = num_values // 2  # Calcula la cantidad de grupos de barras
    total_gap = width - 120  # Espacio total disponible para los grupos de barras
    bar_width = total_gap // (6 * num_groups + 1)  # Calcula el ancho de cada barra
    gap = bar_width // 2  # Espacio entre barras dentro de un grupo
    group_space = 3 * gap + 2 * bar_width  # Espacio total ocupado por un grupo de barras

    x = gap + 60  # Desplazado a la derecha
    y = height - 50

    max_data = max(data)
    y_scale = 10 * ((max_data // 10) + 1)  # Escala el eje Y para que el número máximo calce

    # Dibujar ejes X e Y
    pygame.draw.line(chart_image, (0, 0, 0), (60, y), (width - 60, y), 2)  # Eje X
    pygame.draw.line(chart_image, (0, 0, 0), (60, 50), (60, y), 2)  # Eje Y

    for i in range(num_groups):
        x += i * group_space  # Ajusta el desplazamiento para cada grupo

        for j in range(2):  # Dos barras por grupo
            bar_height = (data[2*i + j] / y_scale) * (y - 50)  # Ajustar la altura de la barra
            pygame.draw.rect(chart_image, (224, 170, 255), (x, y - bar_height, bar_width, bar_height))

            # Agregar etiqueta de datos en la parte inferior de la barra
            text = font.render(str(data[2*i + j]), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (x + bar_width / 2, y + 10)
            chart_image.blit(text, text_rect)

            x += bar_width + gap  # Ajuste de posición para la siguiente barra dentro del grupo

    y_scale = max(data)

    if all(value == 0 for value in data):
        y_scale = 1  # Establecer y_scale en 1 si todos son cero

    y_labels = []
    num_labels = min(y_scale // 20 + 1, 11)  # Máximo de 10 etiquetas + 0
    for i in range(num_labels):
        if (num_labels > 1):
            label = y_scale * i // (num_labels - 1)
        else:
            label = y_scale * i // (num_labels)
        y_labels.append(label)

    for label in y_labels:
        text = font.render(str(label), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (30, height - 50 - (label / y_scale) * (height - 100))
        chart_image.blit(text, text_rect)

    return chart_image
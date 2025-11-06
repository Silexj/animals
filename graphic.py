import pygame
import json
import sys
import os
import subprocess
import random

# --- КОНФИГУРАЦИЯ ---
# Общие
CELL_SIZE = 60
SIDEBAR_WIDTH = 350
INFO_PANEL_HEIGHT = 50
SCROLL_SPEED = 30

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

ASSETS_PATH = os.path.join(SCRIPT_DIR, "assets")
CPP_EXECUTABLE = os.path.join(SCRIPT_DIR, "bin", "program.exe") # Примерный путь, измените если нужно
INPUT_CONFIG_PATH = os.path.join(SCRIPT_DIR, "input.txt")
OUTPUT_DATA_PATH = os.path.join(SCRIPT_DIR, "simulation_output.json")
FOX_IMAGE_PATH = os.path.join(ASSETS_PATH, "animals", "fox.png")
RABBIT_IMAGE_PATH = os.path.join(ASSETS_PATH, "animals", "rabbit.png")

# Цвета
COLOR_BACKGROUND = (25, 25, 25)
COLOR_GRID = (50, 50, 50)
COLOR_SIDEBAR_BG = (40, 40, 40)
COLOR_HIGHLIGHT = (255, 255, 0)
COLOR_TEXT_HEADER = (255, 255, 255)
COLOR_TEXT_BODY = (200, 200, 200)
COLOR_INPUT_ACTIVE = (200, 200, 255)
COLOR_INPUT_INACTIVE = (150, 150, 150)
COLOR_BUTTON = (80, 80, 80)
COLOR_BUTTON_HOVER = (110, 110, 110)

# --- КЛАССЫ UI ЭЛЕМЕНТОВ ---
class InputBox:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INPUT_INACTIVE
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_INPUT_ACTIVE if self.active else COLOR_INPUT_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = COLOR_INPUT_INACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Разрешаем вводить только цифры
                    if event.unicode.isdigit():
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class Button:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(screen, color, self.rect)
        
        text_surf = self.font.render(self.text, True, COLOR_TEXT_HEADER)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def generate_input_file(config):
    """Генерирует input.txt на основе данных из меню."""
    try:
        with open(INPUT_CONFIG_PATH, 'w') as f:
            f.write(f"{config['width']} {config['height']} {config['steps']}\n")
            f.write(f"{config['rabbits']} {config['foxes']}\n")
            # Генерация кроликов
            for _ in range(config['rabbits']):
                x = random.randint(0, config['width'] - 1)
                y = random.randint(0, config['height'] - 1)
                d = random.randint(0, 3) # Направление
                s = random.randint(2, 5) # Стабильность
                f.write(f"{x} {y} {d} {s}\n")
            # Генерация лис
            for _ in range(config['foxes']):
                x = random.randint(0, config['width'] - 1)
                y = random.randint(0, config['height'] - 1)
                d = random.randint(0, 3)
                s = random.randint(2, 5)
                f.write(f"{x} {y} {d} {s}\n")
        return True
    except IOError as e:
        print(f"Ошибка записи в input.txt: {e}")
        return False

def run_simulation_cpp():
    """Запускает C++ исполняемый файл."""
    print("Запуск C++ симуляции...")
    try:
        subprocess.run([CPP_EXECUTABLE], check=True, capture_output=True, text=True)
        print("Симуляция завершена.")
        return True
    except FileNotFoundError:
        print(f"ОШИБКА: Исполняемый файл не найден по пути '{CPP_EXECUTABLE}'")
        return False
    except subprocess.CalledProcessError as e:
        print(f"ОШИБКА во время выполнения симуляции: {e}")
        print(f"Вывод C++ программы (stderr):\n{e.stderr}")
        return False

def load_simulation_data():
    """Загружает данные симуляции из JSON-файла."""
    try:
        with open(OUTPUT_DATA_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки данных симуляции: {e}")
        return None

def load_images():
    """Загружает и масштабирует изображения животных."""
    try:
        fox_img = pygame.image.load(FOX_IMAGE_PATH).convert_alpha()
        rabbit_img = pygame.image.load(RABBIT_IMAGE_PATH).convert_alpha()
        scaled_size = (int(CELL_SIZE * 0.9), int(CELL_SIZE * 0.9))
        return {
            "fox": pygame.transform.scale(fox_img, scaled_size),
            "rabbit": pygame.transform.scale(rabbit_img, scaled_size)
        }
    except pygame.error as e:
        print(f"Ошибка загрузки изображений: {e}")
        return None

def draw_text(screen, text, pos, font, color=COLOR_TEXT_BODY):
    """Упрощенная функция для отрисовки текста."""
    screen.blit(font.render(text, True, color), pos)

def draw_sidebar(screen, fonts, selected_cell, animals_in_cell, grid_height, scroll_y, step_data):
    """Отрисовывает боковую панель с поддержкой скроллинга и общей статистики."""
    sidebar_x = pygame.display.get_surface().get_width() - SIDEBAR_WIDTH
    sidebar_height = grid_height * CELL_SIZE
    sidebar_rect = pygame.Rect(sidebar_x, 0, SIDEBAR_WIDTH, sidebar_height)
    pygame.draw.rect(screen, COLOR_SIDEBAR_BG, sidebar_rect)
    
    content_surface_height = max(sidebar_height, len(animals_in_cell) * 150 + 150)
    content_surface = pygame.Surface((SIDEBAR_WIDTH, content_surface_height), pygame.SRCALPHA)
    
    current_y = 70

    if not selected_cell:
        # ИЗМЕНЕНИЕ: Отображаем общую статистику, если клетка не выбрана
        draw_text(content_surface, "Общая статистика", (20, 20), fonts["header"], COLOR_TEXT_HEADER)
        
        num_foxes = len(step_data["foxes"])
        num_rabbits = len(step_data["rabbits"])
        total_animals = num_foxes + num_rabbits

        draw_text(content_surface, f"Количество лис:", (20, current_y), fonts["body_bold"])
        draw_text(content_surface, str(num_foxes), (250, current_y), fonts["body"])
        current_y += 35

        draw_text(content_surface, f"Количество кроликов:", (20, current_y), fonts["body_bold"])
        draw_text(content_surface, str(num_rabbits), (250, current_y), fonts["body"])
        current_y += 45

        pygame.draw.line(content_surface, COLOR_GRID, (10, current_y), (SIDEBAR_WIDTH - 10, current_y))
        current_y += 15

        draw_text(content_surface, f"Всего животных:", (20, current_y), fonts["body_bold"])
        draw_text(content_surface, str(total_animals), (250, current_y), fonts["body"])

    else:
        # Этот блок остается как был
        draw_text(content_surface, "Информация", (20, 20), fonts["header"], COLOR_TEXT_HEADER)
        
        coord_text = f"Клетка: ({selected_cell[0] + 1}, {selected_cell[1] + 1})"
        draw_text(content_surface, coord_text, (20, current_y), fonts["body"])
        current_y += 40
        
        if not animals_in_cell:
            draw_text(content_surface, "Клетка пуста", (20, current_y), fonts["body"])
        else:
            for animal in animals_in_cell:
                type_text = f"Тип: {animal['type']}"
                draw_text(content_surface, type_text, (20, current_y), fonts["body_bold"])
                current_y += 25
                draw_text(content_surface, f"ID: {animal['id']}", (35, current_y), fonts["body"])
                current_y += 25
                draw_text(content_surface, f"Возраст: {animal['age']}", (35, current_y), fonts["body"])
                current_y += 25
                if animal['type'] == 'Лиса':
                    draw_text(content_surface, f"Голод: {animal['hunger']}", (35, current_y), fonts["body"])
                    current_y += 25
                current_y += 20
                pygame.draw.line(content_surface, COLOR_GRID, (10, current_y - 15), (SIDEBAR_WIDTH - 10, current_y - 15))

    screen.blit(content_surface, (sidebar_x, 0), (0, scroll_y, SIDEBAR_WIDTH, sidebar_height))
    return current_y


# --- ОСНОВНАЯ ФУНКЦИЯ ---
def main():
    pygame.init()
    
    game_state = "MENU"
    simulation_data = None
    
    fonts = {
        "header": pygame.font.SysFont("sans", 32, bold=True),
        "body_bold": pygame.font.SysFont("sans", 24, bold=True),
        "body": pygame.font.SysFont("sans", 22),
        "info": pygame.font.SysFont("sans", 28),
        "cell_count": pygame.font.SysFont("sans", 18, bold=True),
    }
    clock = pygame.time.Clock()

    # (Код для меню остается без изменений)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Настройка симуляции")
    input_boxes = {
        "width": InputBox(350, 150, 140, 32, fonts["body"], "20"),
        "height": InputBox(350, 200, 140, 32, fonts["body"], "15"),
        "steps": InputBox(350, 250, 140, 32, fonts["body"], "10"),
        "rabbits": InputBox(350, 300, 140, 32, fonts["body"], "15"),
        "foxes": InputBox(350, 350, 140, 32, fonts["body"], "5"),
    }
    start_button = Button(300, 450, 200, 50, fonts["header"], "СТАРТ")
    error_message = ""

    # (Переменные симуляции остаются без изменений)
    images = None
    grid_dims = {}
    current_step = 0
    selected_cell = None
    animals_in_selected_cell = []
    scroll_y = 0
    total_content_height = 0

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(COLOR_BACKGROUND)

        if game_state == "MENU":
            # (Код для меню остается без изменений)
            for event in events:
                for box in input_boxes.values():
                    box.handle_event(event)
                if start_button.is_clicked(event):
                    config = {name: int(box.text) for name, box in input_boxes.items() if box.text and box.text.isdigit()}
                    if len(config) != 5:
                        error_message = "Ошибка: все поля должны быть заполнены целыми числами."
                    else:
                        error_message = ""
                        if generate_input_file(config) and run_simulation_cpp():
                            simulation_data = load_simulation_data()
                            if simulation_data:
                                game_state = "SIMULATION"
                                grid_dims = simulation_data["grid_dimensions"]
                                screen_width = grid_dims["width"] * CELL_SIZE + SIDEBAR_WIDTH
                                screen_height = grid_dims["height"] * CELL_SIZE
                                screen = pygame.display.set_mode((screen_width, screen_height + INFO_PANEL_HEIGHT))
                                pygame.display.set_caption("Симуляция 'Лисы и Кролики'")
                                images = load_images()
                                if not images: running = False
                        else:
                            error_message = "Не удалось запустить симуляцию. См. консоль."
            
            draw_text(screen, "Настройка симуляции", (250, 50), fonts["header"], COLOR_TEXT_HEADER)
            draw_text(screen, "Ширина поля:", (150, 155), fonts["body"])
            draw_text(screen, "Высота поля:", (150, 205), fonts["body"])
            draw_text(screen, "Кол-во шагов:", (150, 255), fonts["body"])
            draw_text(screen, "Кол-во кроликов:", (150, 305), fonts["body"])
            draw_text(screen, "Кол-во лис:", (150, 355), fonts["body"])
            for box in input_boxes.values():
                box.draw(screen)
            start_button.draw(screen)
            if error_message:
                draw_text(screen, error_message, (150, 520), fonts["body"], (255, 50, 50))

        elif game_state == "SIMULATION":
            # (Код обработки событий симуляции остается без изменений)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        current_step = min(current_step + 1, len(simulation_data["simulation_data"]) - 1)
                        selected_cell = None
                        scroll_y = 0
                    elif event.key == pygame.K_LEFT:
                        current_step = max(current_step - 1, 0)
                        selected_cell = None
                        scroll_y = 0
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < grid_dims["width"] * CELL_SIZE and pos[1] < grid_dims["height"] * CELL_SIZE:
                        selected_cell = (pos[0] // CELL_SIZE, pos[1] // CELL_SIZE)
                        scroll_y = 0
                        animals_in_selected_cell = [
                            {**f, 'type': 'Лиса'} for f in simulation_data["simulation_data"][current_step]["foxes"]
                            if f['x'] == selected_cell[0] and f['y'] == selected_cell[1]
                        ] + [
                            {**r, 'type': 'Кролик'} for r in simulation_data["simulation_data"][current_step]["rabbits"]
                            if r['x'] == selected_cell[0] and r['y'] == selected_cell[1]
                        ]
                if event.type == pygame.MOUSEWHEEL:
                    scroll_y -= event.y * SCROLL_SPEED
                    max_scroll_y = max(0, total_content_height - grid_dims["height"] * CELL_SIZE)
                    scroll_y = max(0, min(scroll_y, max_scroll_y))
            
            grid_height_px = grid_dims["height"] * CELL_SIZE
            grid_width_px = grid_dims["width"] * CELL_SIZE
            for x in range(0, grid_width_px, CELL_SIZE):
                pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, grid_height_px))
            for y in range(0, grid_height_px, CELL_SIZE):
                pygame.draw.line(screen, COLOR_GRID, (0, y), (grid_width_px, y))
            
            step_data = simulation_data["simulation_data"][current_step]
            animal_counts = {}
            all_animals = step_data["foxes"] + step_data["rabbits"]
            for animal in all_animals:
                pos = (animal['x'], animal['y'])
                animal_counts[pos] = animal_counts.get(pos, 0) + 1

            for animal_type, img in [("foxes", images["fox"]), ("rabbits", images["rabbit"])]:
                for animal in step_data[animal_type]:
                    rect = img.get_rect(center=(animal['x'] * CELL_SIZE + CELL_SIZE / 2, animal['y'] * CELL_SIZE + CELL_SIZE / 2))
                    screen.blit(img, rect)

            for (x, y), count in animal_counts.items():
                if count > 1:
                    count_text = str(count)
                    text_surf = fonts["cell_count"].render(count_text, True, COLOR_HIGHLIGHT)
                    text_rect = text_surf.get_rect(topright=(x * CELL_SIZE + CELL_SIZE - 5, y * CELL_SIZE + 5))
                    bg_rect = text_rect.inflate(4, 4)
                    pygame.draw.rect(screen, (0, 0, 0), bg_rect, border_radius=3)
                    screen.blit(text_surf, text_rect)
            
            if selected_cell:
                rect = pygame.Rect(selected_cell[0] * CELL_SIZE, selected_cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_HIGHLIGHT, rect, 3)

            # ИЗМЕНЕНИЕ: Передаем 'step_data' в функцию отрисовки сайдбара
            total_content_height = draw_sidebar(screen, fonts, selected_cell, animals_in_selected_cell, grid_dims["height"], scroll_y, step_data)
            
            info_panel_rect = pygame.Rect(0, grid_height_px, screen.get_width(), INFO_PANEL_HEIGHT)
            pygame.draw.rect(screen, (30, 30, 30), info_panel_rect)
            draw_text(screen, f"Шаг: {step_data['step_number']} / {len(simulation_data['simulation_data']) - 1}", (15, grid_height_px + 10), fonts["info"])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

    
if __name__ == '__main__':
    main()
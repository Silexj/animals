import pygame
import json
import sys
import os
import subprocess
import random

# --- Глобальные константы и настройки ---
CELL_SIZE = 60
SIDEBAR_WIDTH = 350
INFO_PANEL_HEIGHT = 50
SCROLL_SPEED = 30

# Динамическое определение путей относительно расположения скрипта
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

ASSETS_PATH = os.path.join(SCRIPT_DIR, "assets")
CPP_EXECUTABLE = os.path.join(SCRIPT_DIR, "bin", "program.exe")
INPUT_CONFIG_PATH = os.path.join(SCRIPT_DIR, "input.txt")
OUTPUT_DATA_PATH = os.path.join(SCRIPT_DIR, "simulation_output.json")
FOX_IMAGE_PATH = os.path.join(ASSETS_PATH, "animals", "fox.png")
RABBIT_IMAGE_PATH = os.path.join(ASSETS_PATH, "animals", "rabbit.png")

# --- Цветовая палитра и словари ---
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

DIRECTION_MAP = {0: "Север (↑)", 1: "Восток (→)", 2: "Запад (←)", 3: "Юг (↓)"}

# --- Классы UI элементов ---
class InputBox:
    """Элемент для ввода текста, обрабатывающий клики и нажатия клавиш."""
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INPUT_INACTIVE
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, COLOR_TEXT_HEADER)
        self.active = False

    def handle_event(self, event, offset_y=0):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Корректируем позицию клика с учетом скролла для правильного определения фокуса
            adjusted_mouse_pos = (event.pos[0], event.pos[1] + offset_y)
            self.active = self.rect.collidepoint(adjusted_mouse_pos)
            self.color = COLOR_INPUT_ACTIVE if self.active else COLOR_INPUT_INACTIVE
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = COLOR_INPUT_INACTIVE
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, COLOR_TEXT_HEADER)

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

    def is_clicked(self, event, offset_y=0):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Корректируем позицию клика для поддержки скролла
            adjusted_mouse_pos = (event.pos[0], event.pos[1] + offset_y)
            if self.rect.collidepoint(adjusted_mouse_pos):
                return True
        return False

# --- Вспомогательные функции ---
def generate_input_file_random(config):
    """Создает input.txt со случайными параметрами животных."""
    try:
        with open(INPUT_CONFIG_PATH, 'w') as f:
            f.write(f"{config['width']} {config['height']} {config['steps']}\n")
            f.write(f"{config['rabbits']} {config['foxes']}\n")
            for _ in range(config['rabbits']):
                f.write(f"{random.randint(0, config['width'] - 1)} {random.randint(0, config['height'] - 1)} {random.randint(0, 3)} {random.randint(2, 5)}\n")
            for _ in range(config['foxes']):
                f.write(f"{random.randint(0, config['width'] - 1)} {random.randint(0, config['height'] - 1)} {random.randint(0, 3)} {random.randint(2, 5)}\n")
        return True
    except IOError:
        return False

def generate_input_file_manual(config, manual_data):
    """Создает input.txt на основе данных из формы ручного ввода."""
    try:
        with open(INPUT_CONFIG_PATH, 'w') as f:
            f.write(f"{config['width']} {config['height']} {config['steps']}\n")
            f.write(f"{config['rabbits']} {config['foxes']}\n")
            for animal_data in manual_data:
                f.write(f"{animal_data['x'].text} {animal_data['y'].text} {animal_data['d'].text} {animal_data['s'].text}\n")
        return True
    except IOError:
        return False

def run_simulation_cpp():
    print("Запуск C++ симуляции...")
    try:
        subprocess.run([CPP_EXECUTABLE], check=True, capture_output=True, text=True)
        print("Симуляция завершена.")
        return True
    except FileNotFoundError:
        print(f"ОШИБКА: Исполняемый файл не найден '{CPP_EXECUTABLE}'")
        return False
    except subprocess.CalledProcessError as e:
        print(f"ОШИБКА C++: {e.stderr}")
        return False

def load_simulation_data():
    try:
        with open(OUTPUT_DATA_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки JSON: {e}")
        return None

def load_images():
    try:
        fox_img = pygame.image.load(FOX_IMAGE_PATH).convert_alpha()
        rabbit_img = pygame.image.load(RABBIT_IMAGE_PATH).convert_alpha()
        scaled_size = (int(CELL_SIZE * 0.9), int(CELL_SIZE * 0.9))
        return {"fox": pygame.transform.scale(fox_img, scaled_size), "rabbit": pygame.transform.scale(rabbit_img, scaled_size)}
    except pygame.error as e:
        print(f"Ошибка загрузки изображений: {e}")
        return None

def draw_text(screen, text, pos, font, color=COLOR_TEXT_BODY):
    screen.blit(font.render(text, True, color), pos)

def draw_sidebar(screen, fonts, selected_cell, animals_in_cell, grid_height, scroll_y, step_data):
    sidebar_x = pygame.display.get_surface().get_width() - SIDEBAR_WIDTH
    sidebar_height = grid_height * CELL_SIZE
    sidebar_rect = pygame.Rect(sidebar_x, 0, SIDEBAR_WIDTH, sidebar_height)
    pygame.draw.rect(screen, COLOR_SIDEBAR_BG, sidebar_rect)

    # Используем временную поверхность для реализации прокрутки контента
    content_surface = pygame.Surface((SIDEBAR_WIDTH, max(sidebar_height, len(animals_in_cell) * 180 + 150)), pygame.SRCALPHA)
    current_y = 70

    if not selected_cell:
        # Режим общей статистики
        draw_text(content_surface, "Общая статистика", (20, 20), fonts["header"], COLOR_TEXT_HEADER)
        num_foxes, num_rabbits = len(step_data["foxes"]), len(step_data["rabbits"])
        draw_text(content_surface, "Количество лис:", (20, current_y), fonts["body_bold"]); draw_text(content_surface, str(num_foxes), (250, current_y), fonts["body"]); current_y += 35
        draw_text(content_surface, "Количество кроликов:", (20, current_y), fonts["body_bold"]); draw_text(content_surface, str(num_rabbits), (250, current_y), fonts["body"]); current_y += 45
        pygame.draw.line(content_surface, COLOR_GRID, (10, current_y), (SIDEBAR_WIDTH - 10, current_y)); current_y += 15
        draw_text(content_surface, "Всего животных:", (20, current_y), fonts["body_bold"]); draw_text(content_surface, str(num_foxes + num_rabbits), (250, current_y), fonts["body"])
    else:
        # Режим детальной информации по клетке
        draw_text(content_surface, "Информация", (20, 20), fonts["header"], COLOR_TEXT_HEADER)
        draw_text(content_surface, f"Клетка: ({selected_cell[0] + 1}, {selected_cell[1] + 1})", (20, current_y), fonts["body"]); current_y += 40
        if not animals_in_cell:
            draw_text(content_surface, "Клетка пуста", (20, current_y), fonts["body"])
        else:
            for animal in animals_in_cell:
                draw_text(content_surface, f"Тип: {animal['type']}", (20, current_y), fonts["body_bold"]); current_y += 25
                draw_text(content_surface, f"ID: {animal['id']}", (35, current_y), fonts["body"]); current_y += 25
                draw_text(content_surface, f"Возраст: {animal['age']}", (35, current_y), fonts["body"]); current_y += 25
                draw_text(content_surface, f"Направление: {DIRECTION_MAP.get(animal.get('direction', -1), '?')}", (35, current_y), fonts["body"]); current_y += 25
                if animal['type'] == 'Лиса':
                    draw_text(content_surface, f"Голод: {animal['hunger']}", (35, current_y), fonts["body"]); current_y += 25
                current_y += 20
                pygame.draw.line(content_surface, COLOR_GRID, (10, current_y - 15), (SIDEBAR_WIDTH - 10, current_y - 15))
    
    # Отрисовываем видимую часть контента на основной экран
    screen.blit(content_surface, (sidebar_x, 0), (0, scroll_y, SIDEBAR_WIDTH, sidebar_height))
    return current_y

def main():
    pygame.init()

    # Управляет тем, какой экран отображать: MENU, MANUAL_INPUT или SIMULATION
    game_state = "MENU"
    simulation_data = None
    
    fonts = { "header": pygame.font.SysFont("sans", 32, bold=True), "body_bold": pygame.font.SysFont("sans", 24, bold=True),
              "body": pygame.font.SysFont("sans", 22), "info": pygame.font.SysFont("sans", 28), "cell_count": pygame.font.SysFont("sans", 18, bold=True), }
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600)); pygame.display.set_caption("Настройка симуляции")

    # Переменные для состояния MENU
    input_boxes = {"width": InputBox(350, 150, 140, 32, fonts["body"], "10"), "height": InputBox(350, 200, 140, 32, fonts["body"], "10"),
                   "steps": InputBox(350, 250, 140, 32, fonts["body"], "25"), "rabbits": InputBox(350, 300, 140, 32, fonts["body"], "10"),
                   "foxes": InputBox(350, 350, 140, 32, fonts["body"], "5"),}
    menu_buttons = {"random": Button(250, 420, 300, 40, fonts["body"], "Запуск с Random"),
                    "manual": Button(250, 470, 300, 40, fonts["body"], "Ручной ввод параметров"),
                    "existing": Button(250, 520, 300, 40, fonts["body"], "Запуск с текущим input.txt")}
    error_message = ""

    # Переменные для состояния MANUAL_INPUT
    manual_config = {}; manual_input_boxes = []; manual_scroll_y = 0; manual_content_height = 0
    
    # Переменные для состояния SIMULATION
    images = None; grid_dims = {}; current_step = 0; selected_cell = None; animals_in_selected_cell = []; scroll_y = 0; total_content_height = 0

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.fill(COLOR_BACKGROUND)

        # --- Состояние: Главное меню ---
        if game_state == "MENU":
            for event in events:
                for box in input_boxes.values():
                    box.handle_event(event)

                # Вложенная функция для избежания дублирования кода при переходе в симуляцию
                def start_simulation(success):
                    nonlocal simulation_data, game_state, grid_dims, images, error_message, running
                    if success:
                        simulation_data = load_simulation_data()
                        if simulation_data:
                            game_state = "SIMULATION"
                            grid_dims = simulation_data["grid_dimensions"]
                            screen_width = grid_dims["width"] * CELL_SIZE + SIDEBAR_WIDTH
                            screen_height = grid_dims["height"] * CELL_SIZE
                            screen = pygame.display.set_mode((screen_width, screen_height + INFO_PANEL_HEIGHT))
                            images = load_images()
                            if not images:
                                running = False
                        else: error_message = "Ошибка загрузки JSON. См. консоль."
                    else: error_message = "Ошибка запуска C++. См. консоль."

                if menu_buttons["random"].is_clicked(event):
                    config = {name: int(box.text) for name, box in input_boxes.items() if box.text.isdigit()}
                    if len(config) != 5: error_message = "Ошибка: все поля должны быть заполнены."
                    else: start_simulation(generate_input_file_random(config) and run_simulation_cpp())
                
                if menu_buttons["manual"].is_clicked(event):
                    config = {name: int(box.text) for name, box in input_boxes.items() if box.text.isdigit()}
                    if len(config) != 5: error_message = "Ошибка: все поля должны быть заполнены."
                    else:
                        # Подготовка данных для экрана ручного ввода
                        manual_config = config; manual_input_boxes = []; manual_scroll_y = 0; y_pos = 150
                        for i in range(config["rabbits"]):
                            manual_input_boxes.append({"type": "Кролик", "num": i + 1, 'x': InputBox(200, y_pos, 50, 32, fonts["body"]), 'y': InputBox(300, y_pos, 50, 32, fonts["body"]), 'd': InputBox(400, y_pos, 50, 32, fonts["body"]), 's': InputBox(500, y_pos, 50, 32, fonts["body"])}); y_pos += 40
                        y_pos += 20
                        for i in range(config["foxes"]):
                            manual_input_boxes.append({"type": "Лиса", "num": i + 1, 'x': InputBox(200, y_pos, 50, 32, fonts["body"]), 'y': InputBox(300, y_pos, 50, 32, fonts["body"]), 'd': InputBox(400, y_pos, 50, 32, fonts["body"]), 's': InputBox(500, y_pos, 50, 32, fonts["body"])}); y_pos += 40
                        manual_content_height = y_pos + 80
                        game_state = "MANUAL_INPUT"

                if menu_buttons["existing"].is_clicked(event):
                    if not os.path.exists(INPUT_CONFIG_PATH): error_message = "Ошибка: input.txt не найден."
                    else: start_simulation(run_simulation_cpp())

            # Отрисовка элементов меню
            draw_text(screen, "Настройка симуляции", (250, 50), fonts["header"], COLOR_TEXT_HEADER)
            draw_text(screen, "Ширина поля:", (150, 155), fonts["body"]); draw_text(screen, "Высота поля:", (150, 205), fonts["body"]); draw_text(screen, "Кол-во шагов:", (150, 255), fonts["body"]); draw_text(screen, "Кол-во кроликов:", (150, 305), fonts["body"]); draw_text(screen, "Кол-во лис:", (150, 355), fonts["body"])
            for box in input_boxes.values(): box.draw(screen)
            for button in menu_buttons.values(): button.draw(screen)
            if error_message: draw_text(screen, error_message, (150, 580), fonts["body"], (255, 50, 50))
        
        # --- Состояние: Ручной ввод ---
        elif game_state == "MANUAL_INPUT":
            content_surface = pygame.Surface((800, manual_content_height)); content_surface.fill(COLOR_BACKGROUND)
            start_manual_button = Button(300, manual_content_height - 60, 200, 50, fonts["header"], "СТАРТ")
            
            for event in events:
                if event.type == pygame.MOUSEWHEEL:
                    manual_scroll_y = max(0, min(manual_scroll_y - event.y * SCROLL_SPEED, manual_content_height - 600))
                for group in manual_input_boxes:
                    for box in [group['x'], group['y'], group['d'], group['s']]:
                        box.handle_event(event, manual_scroll_y)
                
                if start_manual_button.is_clicked(event, manual_scroll_y):
                    all_filled = all(box.text.isdigit() for group in manual_input_boxes for box in [group['x'], group['y'], group['d'], group['s']])
                    if not all_filled:
                        error_message = "Ошибка: все поля животных должны быть заполнены."
                    else: 
                        manual_data_to_write = ([{'x':g['x'], 'y':g['y'], 'd':g['d'], 's':g['s']} for g in manual_input_boxes if g['type']=='Кролик'] + 
                                                [{'x':g['x'], 'y':g['y'], 'd':g['d'], 's':g['s']} for g in manual_input_boxes if g['type']=='Лиса'])
                        start_simulation(generate_input_file_manual(manual_config, manual_data_to_write) and run_simulation_cpp())
            
            # Отрисовка прокручиваемого контента
            draw_text(content_surface, "Ручной ввод параметров", (250, 20), fonts["header"], COLOR_TEXT_HEADER)
            draw_text(content_surface, "X", (220, 110), fonts["body_bold"]); draw_text(content_surface, "Y", (320, 110), fonts["body_bold"]); draw_text(content_surface, "D", (420, 110), fonts["body_bold"]); draw_text(content_surface, "S", (520, 110), fonts["body_bold"])
            for group in manual_input_boxes:
                draw_text(content_surface, f"{group['type']} #{group['num']}", (20, group['x'].rect.y + 5), fonts["body"])
                for box in [group['x'], group['y'], group['d'], group['s']]:
                    box.draw(content_surface)
            start_manual_button.draw(content_surface)
            if error_message:
                draw_text(content_surface, error_message, (150, manual_content_height - 80), fonts["body"], (255, 50, 50))
            
            screen.blit(content_surface, (0, 0), (0, manual_scroll_y, 800, 600))

        # --- Состояние: Симуляция ---
        elif game_state == "SIMULATION":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        current_step = min(current_step + 1, len(simulation_data["simulation_data"]) - 1); selected_cell = None; scroll_y = 0
                    elif event.key == pygame.K_LEFT:
                        current_step = max(current_step - 1, 0); selected_cell = None; scroll_y = 0
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < grid_dims["width"] * CELL_SIZE and pos[1] < grid_dims["height"] * CELL_SIZE:
                        selected_cell = (pos[0] // CELL_SIZE, pos[1] // CELL_SIZE); scroll_y = 0
                        step_data = simulation_data["simulation_data"][current_step]
                        animals_in_selected_cell = ([{**f, 'type': 'Лиса'} for f in step_data["foxes"] if f['x'] == selected_cell[0] and f['y'] == selected_cell[1]] + 
                                                   [{**r, 'type': 'Кролик'} for r in step_data["rabbits"] if r['x'] == selected_cell[0] and r['y'] == selected_cell[1]])
                if event.type == pygame.MOUSEWHEEL:
                    scroll_y = max(0, min(scroll_y - event.y * SCROLL_SPEED, total_content_height - grid_dims["height"] * CELL_SIZE))
            
            # Отрисовка игрового поля
            grid_height_px, grid_width_px = grid_dims["height"] * CELL_SIZE, grid_dims["width"] * CELL_SIZE
            for x in range(0, grid_width_px, CELL_SIZE):
                pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, grid_height_px))
            for y in range(0, grid_height_px, CELL_SIZE):
                pygame.draw.line(screen, COLOR_GRID, (0, y), (grid_width_px, y))
            
            step_data = simulation_data["simulation_data"][current_step]
            
            # Подсчет животных в каждой клетке
            animal_counts = {}
            for animal in step_data["foxes"] + step_data["rabbits"]:
                pos = (animal['x'], animal['y'])
                animal_counts[pos] = animal_counts.get(pos, 0) + 1
            
            # Отрисовка животных и счетчиков
            for animal_type, img in [("foxes", images["fox"]), ("rabbits", images["rabbit"])]:
                for animal in step_data[animal_type]:
                    screen.blit(img, img.get_rect(center=(animal['x'] * CELL_SIZE + CELL_SIZE / 2, animal['y'] * CELL_SIZE + CELL_SIZE / 2)))
            for (x, y), count in animal_counts.items():
                if count > 1:
                    text_surf = fonts["cell_count"].render(str(count), True, COLOR_HIGHLIGHT)
                    text_rect = text_surf.get_rect(topright=(x * CELL_SIZE + CELL_SIZE - 5, y * CELL_SIZE + 5))
                    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4), border_radius=3)
                    screen.blit(text_surf, text_rect)
            
            if selected_cell:
                pygame.draw.rect(screen, COLOR_HIGHLIGHT, pygame.Rect(selected_cell[0] * CELL_SIZE, selected_cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
            
            # Отрисовка UI
            total_content_height = draw_sidebar(screen, fonts, selected_cell, animals_in_selected_cell, grid_dims["height"], scroll_y, step_data)
            pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, grid_height_px, screen.get_width(), INFO_PANEL_HEIGHT))
            draw_text(screen, f"Шаг: {step_data['step_number']} / {len(simulation_data['simulation_data']) - 1}", (15, grid_height_px + 10), fonts["info"])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
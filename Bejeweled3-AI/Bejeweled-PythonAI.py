import random
from enum import Enum
from PIL import ImageGrab, Image, ImageColor
import pygetwindow as gw
from collections import Counter


class ArrowDirection(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

class BejeweledTile:
    def __init__(self, tile_code):
        self.tile_code = tile_code
        self.normalised_tile_code = None

class BejeweledBoard:
    def __init__(self, squares=None, tile_count=None):
        if squares is not None:
            self.tile_count = len(squares)
            self.squares = [row[:] for row in squares]
        else:
            self.tile_count = tile_count
            self.squares = [[None for _ in range(tile_count)] for _ in range(tile_count)]

    for x in range(bejeweled_board.tile_count):
        for y in range(bejeweled_board.tile_count):
            tile_image = extract_tile_image(image, x, y)  # Implement this method
            tile_code = analyze_tile(tile_image)  # Implement this method
            bejeweled_board.set_tile(x, y, tile_code)

    return bejeweled_board

    def set_tile(self, x, y, tile_code):
        self.squares[x][y] = BejeweledTile(tile_code)

    def swap_tiles(self, x1, y1, x2, y2):
        self.squares[x1][y1], self.squares[x2][y2] = self.squares[x2][y2], self.squares[x1][y1]

    def try_swap_tiles(self, x1, y1, x2, y2):
        for index in [x1, y1, x2, y2]:
            if index < 0 or index >= self.tile_count:
                return False
        self.swap_tiles(x1, y1, x2, y2)
        return True


class BejeweledMove:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.tiles_to_remove_as_result = set()

    def score(self):
        return len(self.tiles_to_remove_as_result)

    def __str__(self):
        return f"{self.x},{self.y},{self.direction.name} = {self.score()}"

    def __hash__(self):
        return 31 * self.x + 17 * self.y

class BejeweledScreenReader:
    def get_bejeweled_window_rect(self):
        # Logic to find and return the Bejeweled game window rectangle
        pass


class BejeweledScreenReader:
    def __init__(self, tile_count, tile_size):
        self.latest_bitmap = Image.new('RGB', (1, 1))
        self.tile_count = tile_count
        self.tile_size = tile_size

    def draw_and_get_bejeweled_board_from_screen(self, m=0.25, use_mode=False):
        window = self.get_bejeweled_window_rect()
        image = ImageGrab.grab(bbox=(window.left, window.top, window.right, window.bottom))
        image = image.convert('L')  # Convert to 8bpp indexed
        image = image.convert('RGB')  # Convert to 16bpp RGB555
        self.latest_bitmap = image

        bejeweled_board = BejeweledBoard(self.tile_count)
        for x in range(self.tile_count):
            for y in range(self.tile_count):
                sample_rectangle = (self.tile_size * m + x * self.tile_size,
                                    self.tile_size * m + y * self.tile_size,
                                    self.tile_size * (1 - m * 2),
                                    self.tile_size * (1 - m * 2))
                color_bucket = ColorBucket()
                for i in range(sample_rectangle[0], sample_rectangle[2]):
                    for j in range(sample_rectangle[1], sample_rectangle[3]):
                        color_bucket.colors.add(image.getpixel((i, j)))
                tile_code = color_bucket.get_color_code_mode() if use_mode else color_bucket.get_color_code()
                bejeweled_board.set_tile(x, y, tile_code)
        bejeweled_board.normalize()
        return bejeweled_board
    
class BejeweledTile:
    def __init__(self, tile_code):
        self.tile_code = tile_code
        self.normalised_tile_code = None

class ColorBucket:
    def __init__(self):
        self.colors = []
        self.white = (255, 255, 255)
        self.dirt_brown = (255, 255, 255)  # Update this color as needed

        self.known_colors = set([
            (255, 0, 49),
            (255, 0, 255),
            (0, 156, 255),
            (255, 255, 49),
            (255, 99, 0),
            (49, 255, 99),
            self.dirt_brown,
            self.white
        ])

    def get_color_code_mode(self):
        most_common_color, _ = Counter(self.colors).most_common(1)[0]
        return ImageColor.getcolor(f'#{most_common_color[0]:02x}{most_common_color[1]:02x}{most_common_color[2]:02x}', "RGB")

    def get_color_code(self):
        colors_by_frequency = [color for color, count in Counter(self.colors).most_common() if color in self.known_colors]

        if colors_by_frequency:
            if colors_by_frequency[0] == self.white:
                if len(colors_by_frequency) == 1:
                    return ImageColor.getcolor(f'#{self.white[0]:02x}{self.white[1]:02x}{self.white[2]:02x}', "RGB")
                else:
                    return ImageColor.getcolor(f'#{colors_by_frequency[1][0]:02x}{colors_by_frequency[1][1]:02x}{colors_by_frequency[1][2]:02x}', "RGB")
            else:
                return ImageColor.getcolor(f'#{colors_by_frequency[0][0]:02x}{colors_by_frequency[0][1]:02x}{colors_by_frequency[0][2]:02x}', "RGB")
        else:
            return ImageColor.getcolor("#000000", "RGB")  # Black

    @staticmethod
    def is_known_color(tile_code):
        return ImageColor.getrgb(tile_code) in ColorBucket.known_colors
    
class OscillationDetector:
    def __init__(self):
        self.move_list_hashcodes = [0] * 10
        self.next_insertion_index = 0

    def log_moves_and_return_true_if_oscillation_detected(self, moves):
        hashcode = sum(move.__hash__() for move in moves)
        try:
            return hashcode != 0 and self.move_list_hashcodes.count(hashcode) > 2
        finally:
            self.move_list_hashcodes[self.next_insertion_index] = hashcode
            self.next_insertion_index = (self.next_insertion_index + 1) % len(self.move_list_hashcodes)

    @staticmethod
    def get_difference_in_boards(bejeweled_board1, bejeweled_board2):
        differences = 0
        if bejeweled_board1 is not None and bejeweled_board2 is not None:
            for x in range(len(bejeweled_board1.squares)):
                for y in range(len(bejeweled_board1.squares)):
                    if bejeweled_board1.squares[x][y].tile_code != bejeweled_board2.squares[x][y].tile_code:
                        differences += 1
        return differences
    
class PlayBejeweled:
    def __init__(self, tile_count=8, tile_size=...):  # Provide a default or required tile size
        self.screen_reader = BejeweledScreenReader(tile_count, tile_size)

    def capture_and_analyze_game(self):
        return self.screen_reader.draw_and_get_bejeweled_board_from_screen()


def get_bejeweled_window():
    # Logic to find and return the Bejeweled game window
    pass

def extract_tile_image(image, x, y):
    # Extract and return the image for the tile at position (x, y)
    pass

def analyze_tile(tile_image):
    # Analyze the tile image and return the corresponding tile code
    pass


game = PlayBejeweled()
bejeweled_board = game.capture_and_analyze_game()

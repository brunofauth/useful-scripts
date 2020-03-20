import pygame
import random


pygame.init()


def score(score):
    text = small_font.render("Score: " + str(score), True, WHITE)
    display.blit(text, [0, 0])


def get_apple():
    x, y = random.randrange(9) * tile_size, random.randrange(9) * tile_size
    return pygame.Rect(x, y, tile_size, tile_size)


def text_objects(text, color, size):
    sizes = {"small": small_font, "medium": medium_font, "large": large_font}
    text = sizes[size].render(text, True, color)
    return text, text.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2), (display_height / 2) + y_displace
    display.blit(text_surf, text_rect)


def game_over_loop():
    message_to_screen("Game Over", RED, y_displace=-50, size="large")
    message_to_screen("Press C to play again or Q to quit", WHITE,
                      y_displace=50, size="medium")
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_c:
                    return True
        clock.tick(FPS)


def snake_loop():
    head = pygame.Rect(9 // 2 * tile_size, 9 // 2 * tile_size, tile_size, tile_size)
    speed = 0, 0
    snake_length = 1

    # Note: the last item in list is the head)
    snake = [head]
    apple = get_apple()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key in XMOVEKEYS and speed[0] == 0:
                    speed = XMOVEKEYS[event.key][0] * tile_size, XMOVEKEYS[event.key][1] * tile_size
                elif event.key in YMOVEKEYS and speed[1] == 0:
                    speed = YMOVEKEYS[event.key][0] * tile_size, YMOVEKEYS[event.key][1] * tile_size

        head = pygame.Rect(head.x + speed[0], head.y + speed[1], tile_size, tile_size)
        
        if not 0 <= head.x < display_width or not 0 <= head.y < display_height:
            break

        display.fill((0, 0, 0))
        display.fill(RED, apple)

        snake.append(head)

        if len(snake) > snake_length:
            del snake[0]

        if head.collidelist(snake[:-1]) != -1: break
        if snake_length >= 9 * 9: break
        
        for segment in snake:
            display.fill((0, 255, 0), segment)

        score(snake_length - 1)
        pygame.display.flip()

        if pygame.Rect(head.x, head.y, tile_size, tile_size).colliderect(apple):
            apple = get_apple()
            snake_length += 1

        clock.tick(FPS)


def main():
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    tile_size = 64
    
    XMOVEKEYS = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
    YMOVEKEYS = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}
    
    display_width = tile_size * 9
    display_height = tile_size * 9
    
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Minhoca")
    
    clock = pygame.time.Clock()
    FPS = 8
    
    small_font = pygame.font.SysFont("comicsansms", 15)
    medium_font = pygame.font.SysFont("comicsansms", 30)
    large_font = pygame.font.SysFont("comicsansms", 50)
    
    globals().update(locals())
    
    while True:
        snake_loop()
        if not game_over_loop(): break
    pygame.quit()

    
if __name__ == "__main__":
    main()


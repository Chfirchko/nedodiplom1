import pygame

pygame.init()

window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Pygame Window")

# Define button properties
button_color = (255, 255, 255)
button_hover_color = (200, 200, 200)
button_rect = pygame.Rect(300, 250, 200, 100)
button_font = pygame.font.SysFont(None, 36)
button_text = button_font.render("Click me!", True, (0, 0, 0))
button_text_rect = button_text.get_rect(center=button_rect.center)

# Initialize Pygame clock
clock = pygame.time.Clock()

running = True
while running:
    # Limit the frame rate to 60 FPS
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                print("Button clicked!")

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                button_color = button_hover_color
            else:
                button_color = (255, 255, 255)

    # Draw button and clock
    window.fill((128, 128, 128))
    pygame.draw.rect(window, button_color, button_rect)
    window.blit(button_text, button_text_rect)
    current_time = pygame.time.get_ticks()
    clock_text = button_font.render(f"Time: {current_time / 1000:.2f} s", True, (255, 255, 255))
    clock_text_rect = clock_text.get_rect(topright=(780, 10))
    window.blit(clock_text, clock_text_rect)

    pygame.display.flip()
pygame.quit()
import pygame,time

# 初始化 Pygame
pygame.init()

# 设置窗口大小
window_width = 320
window_height = 320
window_size = (window_width, window_height)

# 创建窗口
window = pygame.display.set_mode(window_size,pygame.RESIZABLE)

# 加载图像
BlkPth="resource/img/Block/"
image = pygame.image.load(BlkPth+"Grass_Side.png").convert_alpha()

# 缩放图像


# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #if window_height <= 720:
    #    scaled_image = pygame.transform.scale(image, (window_width, window_height))
    #    window.blit(scaled_image, (0, 0))
    #    window_height += 1
    #    window_width += 1
    #    window_size = (window_width, window_height)
    # 绘制图像
    scaled_image = pygame.transform.scale(image, (window_width, window_height))
    flip_img = pygame.transform.flip(scaled_image, 1, 0) #图，转x轴，转y轴
    window.blit(flip_img, (0, 0))
    plback = pygame.display.get_desktop_sizes()
    # 更新窗口
    pygame.display.update()

# 退出 Pygame
pygame.quit()

if n != 0:
            font = pygame.font.SysFont(None, int(self.KT_O * 0.6))
            text = font.render(str(n), True, (0, 0, 0))
            rect = text.get_rect(center=(
                DEM + c * self.KT_O + self.KT_O // 2,
                DEM + r * self.KT_O + self.KT_O // 2
            ))
            self.screen.blit(text, rect)

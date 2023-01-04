# Курсовой проект по PyGame

Заготовка файла readme.md

## Игра Тортики
### Standalone-запуск
Запустить скрипт cake.py

### Запуск в составе другого приложения Pygame
1. Импортировать модуль:
```buildoutcfg
from cake import CakeGame
```
2. Вставить в приложение следующий код:
```buildoutcfg
game = CakeGame()
game.run()
```
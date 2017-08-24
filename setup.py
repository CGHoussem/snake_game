import cx_Freeze

cx_Freeze.setup(
    name="Snake Game",
    version="0.1",
    options={"build_exe": {"include_files": ["Sprites/grass_tile.png",
                                             "Sprites/wall_tile.png",
                                             "Sprites/apple_sprite.png",
                                             "Sprites/snake_head_sprite.png",
                                             "Sprites/snake_body_tile.png",
                                             "Sounds/apple_eaten.wav",
                                             "Sounds/gameover.wav",
                                             "Sounds/playing.wav",
                                             "Sounds/menu.wav"]}},
    executables=[cx_Freeze.Executable("__main__.py")]
)

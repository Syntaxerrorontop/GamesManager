from . import QWidget, QVBoxLayout, QLabel, QScrollArea, QStackedWidget, QHBoxLayout, QPushButton, QLineEdit
from . import Qt

from . import commen, rungame, downloader
from . import threading, logging, os 

#w
class LibaryTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout (horizontal: left = buttons, right = content)
        main_layout = QHBoxLayout(self)

        # Scroll area for buttons
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Ensure content resizes properly
        self.scroll_area.setStyleSheet(commen.GAMES_BROWSER_SCROLLABLE_LIBARY)
        
        # Container for buttons inside the scroll area
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)  # Set layout for buttons
        self.scroll_area.setWidget(self.button_container)  # Attach container to scroll area
        self.scroll_area.setFixedWidth(200)  # Set a fixed width for sidebar

        # Stacked widget for tab contents
        self.stacked_widget = QStackedWidget()

        # Add widgets to main layout
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.stacked_widget, 1)  # Make stack expand

        # Create tabs (buttons + corresponding pages)
        self.update_list()

    def update_list(self):
        """Creates buttons inside the scrollable area and corresponding pages."""
        logging.debug("Updating list...")  # Debugging print

        # Clear existing buttons
        while self.button_layout.count():
            item = self.button_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new buttons and corresponding pages
        
        json_game_data = commen.load_json(os.path.join(os.getcwd(), commen.CONFIG_DIR, commen.GAMES_JSON_DATA))
        
        for i, game_name in enumerate(os.listdir(os.path.join(os.getcwd(), commen.GAME_DIR))):  # Iterate over games

            try:
                name = game_name
                playtime = json_game_data["Games"][name]["playtime"]
                raw_exe = json_game_data["Games"][name]["exe"]
                raw_args = json_game_data["Games"][name]["args"]
                raw_name = name
            except KeyError:
                logging.warning(f"Game {game_name} is not in the games.json file")
                logging.info("Generating default values")
                
                if commen.ask_yes_no(f"Unknown Game: {game_name}\nDo you want to add it to the libary?"):
                    
                    if os.path.isdir(os.path.join(os.getcwd(), commen.GAME_DIR, game_name)):
                        
                        logging.info("Game is a folder -> adding to Libary")
                        full_path_game_execution, folder_name = downloader._game_naming(use_folder_name = game_name)
                        downloader._add_game_info(full_path_game_execution, folder_name, default=True)
                        
                        logging.info("Reading Games.json file")
                        json_game_data = commen.load_json(os.path.join(os.getcwd(), commen.CONFIG_DIR, commen.GAMES_JSON_DATA))
                        
                        name = game_name
                        playtime = json_game_data["Games"][name]["playtime"]
                        raw_exe = json_game_data["Games"][name]["exe"]
                        raw_args = json_game_data["Games"][name]["args"]
                        raw_name = name
                    
                    else:
                        if game_name.endswith(".rar"):
                            logging.info("Game is a rar file -> extracting")
                            pass
                
                else:
                    continue

            # Create button
            button = QPushButton(game_name)
            button.setStyleSheet(commen.STACKED_WIDGET_BUTTON_LIBARY)
            button.setFixedHeight(40)  
            button.clicked.connect(lambda _, index=i: self.switch_tab(index))  # Link button to tab switching
            self.button_layout.addWidget(button)  # Add button to layout

            # Create corresponding page
            page = QWidget()
            layout = QVBoxLayout(page)
            
            layout.setSpacing(10)
            
            label = QLabel(name)
            label.setStyleSheet(commen.GAME_NAME_STYLESHEET_LIBARY)
            label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # Align label to top-left
            layout.addWidget(label)
            
            playtime_lable = QLabel(f"Playtime: {str(round(playtime / 3600, 2))}h")
            playtime_lable.setStyleSheet(commen.GAME_PLAYTIME_STYLESHEET_LIBARY)
            #playtime_lable.setAlignment(Qt.AlignmentFlag.Align | Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(playtime_lable)
            
            line_edit = QLineEdit(page)
            line_edit.setPlaceholderText("Enter Args here...")
            line_edit.setStyleSheet(commen.QLINE_EDIT_ARGS_LIBARY)
            if raw_args:
                build_string = ""
                for arg in raw_args:
                    build_string += f"{arg} "
                line_edit.setText(build_string)
            
            save_button = QPushButton(page)
            save_button.setText("Save Args")
            save_button.setStyleSheet(commen.ARGS_SAVE_BUTTON_LIBARY)
            save_button.move(1300, 250)
            save_button.clicked.connect(lambda _, qline = line_edit, name = raw_name: self._save_args(name, qline.text()))
            
            play_button = QPushButton(page)
            play_button.setText("Play")
            play_button.setStyleSheet(commen.PLAY_BUTTON_STYLESHEET_LIBARY)
            play_button.move(5, 175)
            play_button.clicked.connect(lambda _, instance = rungame.GameInstance(raw_name, raw_exe, raw_args, play_button): self._rungame_handling(instance))
            
            uninstall_button = QPushButton(page)
            uninstall_button.setText("Uninstall")
            uninstall_button.move(5, 200)
            uninstall_button.clicked.connect(lambda _, name=raw_name: (rungame.uninstall(name), self.update_list()))
            line_edit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

            # Add page to stacked widget
            self.stacked_widget.addWidget(page)  # Add page to stack

        # Push buttons to the top (prevents excessive spacing)
        self.button_layout.addStretch()

        # Set the first page as the default
        self.stacked_widget.setCurrentIndex(0)
    
    def _save_args(self, name, args):
        logging.debug(f"Saving args: {args} game: {name}")
        data = commen.load_json(os.path.join(os.getcwd(), commen.CONFIG_DIR, commen.GAMES_JSON_DATA))
        args = args.split(" ")
        args = [arg for arg in args if arg.strip()]
        data["Games"][name]["args"] = args
        commen.save_json(os.path.join(os.getcwd(), commen.CONFIG_DIR, commen.GAMES_JSON_DATA), data)
    
    def _rungame_handling(self, run_instance: rungame.GameInstance):
        run_instance.start()
        _game_thread = threading.Thread(target=run_instance.wait)
        _game_thread.start()

    def switch_tab(self, index):
        """Switch to the correct tab in QStackedWidget."""
        self.stacked_widget.setCurrentIndex(index)
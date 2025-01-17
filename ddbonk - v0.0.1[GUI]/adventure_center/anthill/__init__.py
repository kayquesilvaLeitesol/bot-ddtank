import pyautogui
import time
import cv2
import logging
import keyboard
import numpy as np
import ctypes
import sys
from PIL import Image

from pandora import (
    turn_on_boss,
    set_count_try_angle,
    set_adjusted_angle,
    ADJUSTED_ANGLE,
    COUNT_GET_TRY_ANGLE,
)

from ants import (
    set_default_parameters_ants,
    fly,
    walking,
    turn_on_stage_ants,
)

logging.basicConfig(filename="../log/error_log.txt", level=logging.ERROR)


def find_image(image_path, confidence=0.7):
    result = {"found": False, "position_x": 0, "position_y": 0}
    try:
        template = cv2.imread(image_path)
        position = pyautogui.locateOnScreen(template, confidence=confidence)

        if position is not None:
            x, y, _, _ = position
            result["found"] = True
            result["position_x"] = x
            result["position_y"] = y

    except Exception as e:
        error_message = f"An error occurred: {e}"
        logging.error(error_message)
        with open("../log/log.txt", "a") as log_file:
            log_file.write(error_message + "\n")

    return result


def step_click(key, x, y):
    print(f"step: '{key}' x: {x} y: {y}")
    pyautogui.click(x, y)


def setting_instance():
    global IMAGES_CHECK, IMAGES_CENTRAL, IMAGES_PLAY, IMAGES_READY, IMAGES_START, IMAGES_AVAILABLE, IMAGES_SELECTED, IMAGES_SELECT, IMAGES_OK, IMAGES_LEVEL
    global PASS_OK, ENABLE_START, LEVEL, AVAILABLE, LEVEL_SELECTED, ANTHILL_SELECTED, STAGE_FINAL

    if not STAGE_FINAL:
        for img_central in IMAGES_CENTRAL:
            central = find_image(img_central["path"])
            if central["found"]:
                step_click(
                    img_central["key"], central["position_x"], central["position_y"]
                )
                break

    for img_play in IMAGES_PLAY:
        play = find_image(img_play["path"])
        if play["found"]:
            step_click(img_play["key"], play["position_x"], play["position_y"])
            break

    if not AVAILABLE:
        for img_ready in IMAGES_READY:
            ready = find_image(img_ready["path"])
            if ready["found"]:
                step_click(img_ready["key"], ready["position_x"], ready["position_y"])
                break

    if LEVEL_SELECTED or not PASS_OK:
        for img_ok in IMAGES_OK:
            ok = find_image(img_ok["path"])
            if ok["found"]:
                step_click(img_ok["key"], ok["position_x"], ok["position_y"])
                PASS_OK = True
                time.sleep(1)
                break

    for img_available in IMAGES_AVAILABLE:
        available = find_image(img_available["path"])
        if available["found"]:
            AVAILABLE = True
            step_click(
                img_available["key"],
                available["position_x"],
                available["position_y"],
            )
            break
        else:
            AVAILABLE = False

    if not AVAILABLE:
        for img_select in IMAGES_SELECT:
            select = find_image(img_select["path"])
            if select["found"]:
                step_click(
                    img_select["key"], select["position_x"], select["position_y"]
                )
                break

    for img_selected in IMAGES_SELECTED:
        selected = find_image(img_selected["path"])
        if selected["found"]:
            step_click(
                img_selected["key"], selected["position_x"], selected["position_y"]
            )
            ANTHILL_SELECTED = True
            STAGE_FINAL = False
            break

    if ANTHILL_SELECTED:
        level = find_image(IMAGES_LEVEL[LEVEL - 1]["path"])
        if level["found"]:
            step_click(
                IMAGES_LEVEL[LEVEL - 1]["key"],
                level["position_x"],
                level["position_y"],
            )
            LEVEL_SELECTED = True

    if not AVAILABLE and ENABLE_START:
        for img_start in IMAGES_START:
            start = find_image(img_start["path"])
            if start["found"]:
                set_default_parameters_ants()
                step_click(img_start["key"], start["position_x"], start["position_y"])
                break

    check = find_image(IMAGES_CHECK[0]["path"])
    if check["found"]:
        print(f"step: checked instance")
        if PASS_OK:
            PASS_OK = False
        else:
            ENABLE_START = True
        AVAILABLE = False
        STAGE_FINAL = False
        ADJUSTED_ANGLE = False
        set_adjusted_angle(False)


IMAGES_CENTRAL = [{"key": "room", "path": "img/central.png"}]
IMAGES_PLAY = [{"key": "enter_room", "path": "img/play.png"}]
IMAGES_READY = [{"key": "ready", "path": "img/ready.png"}]
IMAGES_OK = [{"key": "ok", "path": "img/ok.png"}]
IMAGES_CLOSE = [{"key": "close", "path": "img/close.png"}]
IMAGES_START = [{"key": "start", "path": "img/start.png"}]
IMAGES_AVAILABLE = [{"key": "available", "path": "img/available.png"}]
IMAGES_CHECK = [{"key": "check", "path": "img/check.png"}]
IMAGES_SELECTED = [{"key": "selected_ant", "path": "img/selected_ant.png"}]
IMAGES_SELECT = [{"key": "select", "path": "img/select.png"}]
IMAGES_LEVEL = [
    {"key": "easy", "path": "img/easy.png"},
    {"key": "normal", "path": "img/normal.png"},
]
IMAGES_PASS = [
    {"key": "turn_on", "path": "img/pass.png"},
    {"key": "turn_on", "path": "img/pass2.png"},
    {"key": "turn_on", "path": "img/pass1.png"},
    {"key": "turn_on", "path": "img/pass3.png"},
    {"key": "turn_on", "path": "img/pass4.png"},
    {"key": "turn_on", "path": "img/pass5.png"},
    {"key": "turn_on", "path": "img/pass6.png"},
]

# SETTINGS STAGE
# STAGE_FINAL = True
STAGE_FINAL = False

# SETTINGS ROOM
LEVEL = 0
AVAILABLE = True
ENABLE_START = False
ANTHILL_SELECTED = False
LEVEL_SELECTED = False
PASS_OK = False

# SETTINGS TURN
TURN_ON = False
MAX_TURN = 10
COUNT_TURN = 0

print("Selecione o nível...")
print("Tecle: ")
print("1 - Facil ou 2 - Normal")
input_user = input("Digite um 1 ou 2: ")

try:
    LEVEL = int(input_user)
    if LEVEL == 1 or LEVEL == 2:
        level = IMAGES_LEVEL[LEVEL - 1]["key"]
        print(f"level selecionado: {level}")
    else:
        print("Erro: Por favor, digite apenas 1 ou 2.")
        sys.exit()


except ValueError:
    print("Erro: Por favor, digite um valor inteiro válido.")
    sys.exit()


while True:
    if STAGE_FINAL:
        win = find_image("img/win_stage_2.png")
        if win["found"]:
            print(f"step: win")
            STAGE_FINAL = False
            ADJUSTED_ANGLE = False
            set_adjusted_angle(False)
            set_default_parameters_ants()
            COUNT_TURN = 0
            COUNT_GET_TRY_ANGLE = 0
            set_count_try_angle()

        end_game = find_image("img/end_game.png")
        if end_game["found"]:
            print(f"step: end game")
            STAGE_FINAL = False
            ADJUSTED_ANGLE = False
            set_adjusted_angle(False)
            set_default_parameters_ants()
            COUNT_TURN = 0
            COUNT_GET_TRY_ANGLE = 0
            set_count_try_angle()

    if not STAGE_FINAL and not LEVEL_SELECTED:
        pandora = find_image("img/pandora/pandora.png")
        if pandora["found"]:
            STAGE_FINAL = True
            x = pandora["position_x"]
            y = pandora["position_y"]
            print(f"step: 'pandora' x: {x} y: {y}")

    if not STAGE_FINAL:
        stage_2 = find_image("img/pandora/stage_2.png")
        if stage_2["found"]:
            ENABLE_START = True
            STAGE_FINAL = True
            x = stage_2["position_x"]
            y = stage_2["position_y"]
            print(f"step: 'stage 2' x: {x} y: {y}")

    if not TURN_ON:
        setting_instance()

    for img_pass in IMAGES_PASS:
        key = img_pass["key"]
        turn_on = find_image(img_pass["path"])
        if turn_on["found"]:
            AVAILABLE = False
            ENABLE_START = False
            ANTHILL_SELECTED = False
            LEVEL_SELECTED = False
            PASS_OK = False
            TURN_ON = True

            x_aux = turn_on["position_x"] - 40
            y_aux = turn_on["position_y"] - 80
            step_click(key, x_aux, y_aux)
            time.sleep(0.05)

            if not STAGE_FINAL:
                ADJUSTED_ANGLE = False
                set_adjusted_angle(False)
                COUNT_GET_TRY_ANGLE = 0
                set_count_try_angle()
                if COUNT_TURN < MAX_TURN:
                    turn_on_stage_ants()
                    COUNT_TURN += 1
                else:
                    COUNT_TURN = 0
                    walking()
                    fly()
            else:
                print("boss fight")
                turn_on_boss()
                set_default_parameters_ants()
                COUNT_TURN = 0
            break
        else:
            TURN_ON = False

    time.sleep(0.3)

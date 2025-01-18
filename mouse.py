import ctypes
import keyboard
import time
import win32con
import win32gui
import win32api

# システムカーソルIDのリスト
OCR_CURSORS = [
    win32con.OCR_NORMAL,
    win32con.OCR_IBEAM,
    win32con.OCR_WAIT,
    win32con.OCR_CROSS,
    win32con.OCR_UP,
    win32con.OCR_SIZE,
    win32con.OCR_ICON,
    win32con.OCR_SIZENWSE,
    win32con.OCR_SIZENESW,
    win32con.OCR_SIZEWE,
    win32con.OCR_SIZENS,
    win32con.OCR_SIZEALL,
    win32con.OCR_NO,
    win32con.OCR_HAND,
    win32con.OCR_APPSTARTING,
]

# カーソルファイルの設定
def load_cursor(cursor_path):
    cursor = win32gui.LoadImage(
        0,                         
        cursor_path,                
        win32con.IMAGE_CURSOR,      
        0,                          # 幅
        0,                          # 高さ
        win32con.LR_LOADFROMFILE   
    )
    return cursor

# 右クリックが押されているか判定
def is_right_click_pressed():
    return win32api.GetKeyState(win32con.VK_RBUTTON) < 0

# カーソルの変更
def set_system_cursor(cursor, cursor_id):
    ctypes.windll.user32.SetSystemCursor(cursor, cursor_id)

# カーソルを戻す
def restore_default_cursors():
    ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_SETCURSORS,
        0,
        0,
        win32con.SPIF_SENDCHANGE
    )

def main():
    try:
        cursor_path = "Cocoa.cur" 
        cursors = []
        cursor_set = False
        
        print("右クリックを長押しするとカーソルが変わります")
        print("終了するには 'Esc' キーを押してください")
        
        while True:
            if is_right_click_pressed():
                if not cursor_set:
                    custom_cursor = load_cursor(cursor_path)
                    for cursor_id in OCR_CURSORS:
                        set_system_cursor(custom_cursor, cursor_id)
                        cursors.append(custom_cursor)
                    cursor_set = True
            else:
                if cursor_set:
                    restore_default_cursors()
                    cursor_set = False
                    for cursor in cursors:
                        ctypes.windll.user32.DestroyCursor(cursor)
                    cursors.clear()
            
            if keyboard.is_pressed('esc'):
                break
            
            time.sleep(0.1)  # 0.1秒待機
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    finally:
        restore_default_cursors()
        for cursor in cursors:
            ctypes.windll.user32.DestroyCursor(cursor)
        print("プログラムを終了しました")

if __name__ == "__main__":
    main()
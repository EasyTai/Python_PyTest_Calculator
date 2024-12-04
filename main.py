import subprocess
import time
import os

def start_application(exe_path):
    """Запускает приложение и возвращает объект процесса."""
    print(f"Запуск приложения: {exe_path}")
    return subprocess.Popen([exe_path, 'start'])

def run_tests(test_file_path):
    """Запускает тесты и возвращает результат."""
    print(f"Запуск тестов: {test_file_path}")
    return subprocess.run(["pytest", test_file_path])

def main():
    # Путь к exe-файлу
    web_calculator_path = 'C:\\Users\\Desktop\\path\\webcalculator.exe'
    # Полный путь к файлу тестов
    test_file_path = 'C:\\Users\\Desktop\\test_webcalculator.py'

    # Путь к файлу журнала
    local_app_data_path = os.environ.get('LOCALAPPDATA', '')
    log_file_path = os.path.join(local_app_data_path, 'webcalculator', 'webcalculator.log')

    # Проверка пути к файлу журнала
    print(f"Путь к файлу журнала: {log_file_path}")

    # Запуск приложения
    process = start_application(web_calculator_path)

    try:
        # Ожидание запуска приложения
        time.sleep(5)

        # Запуск тестов
        test_process = run_tests(test_file_path)

        # Проверка результатов тестов
        if test_process.returncode != 0:
            raise Exception("Некоторые тесты не прошли")

    finally:
        # Завершение приложения
        process.terminate()
        print("Процесс приложения завершен.")

if __name__ == "__main__":
    main()

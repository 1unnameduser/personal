#include <windows.h>

// Преобразование ANSI->Unicode
void AnsiToUtf16(const char* src, wchar_t* dest, int size) {
    MultiByteToWideChar(CP_ACP, MB_PRECOMPOSED, src, -1, dest, size);
}

int main() {
    // Получаем полное имя исполняемого файла вместе с путем
    char ansiPath[MAX_PATH];
    GetModuleFileNameA(NULL, ansiPath, MAX_PATH);

    // Заменяем расширение ".exe" на ".bat"
    char* ext = strrchr(ansiPath, '.');
    strcpy(ext, ".bat");

    // Конвертируем строку в Unicode
    wchar_t utf16Path[MAX_PATH];
    AnsiToUtf16(ansiPath, utf16Path, MAX_PATH);

    // Выполняем bat файл скрытно
    ShellExecuteW(nullptr, nullptr, utf16Path, nullptr, nullptr, SW_HIDE);

    return 0;
}
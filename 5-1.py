from pathlib import Path
import sys
import os
import time

def scan_dir(path: Path) -> dict:
    """Zwraca słownik {ścieżka: st_time} dla wszystkich plików w katalogu"""
    result = {}
    for item in path.rglob('*'):
        if item.is_file():
            result[item] = os.stat(item).st_mtime
    return result

def check_changes(current: dict, cache: dict) -> None:
    #Porównuje aktualny stan z cache, wypisuje zmiany i aktualizuje cache
    current_paths = set(current)
    cached_paths = set(cache)

    added = current_paths - cached_paths
    removed = cached_paths - current_paths

    #pliki ktore istniały i nadal istnieją, ale zmieniły się
    modified = set()
    for p in current_paths & cached_paths:
        if current[p] != cache[p]:
            modified.add(p)

    #wypisanie zmian
    for p in sorted(added):
        print(f"[NOWY]   {p}")
    for p in sorted(removed):
        print(f"[USUNIĘTY]   {p}")
    for p in sorted(modified):
        print(f"[ZMIENIONY]   {p}")

    #aktualizacja słownika cache    
    cache.update(current) #nadpisanie/dodanie nowych i zmienionych plików
    for p in removed:
        del cache[p] #usunięcie z cache plików których już nie ma
def main():
    #cache = {}
    if len(sys.argv) != 2:
        sys.exit("usage: 1.py <path>")
    path = Path(sys.argv[1])
    if not path.exists():
        sys.exit(f"Ścieżka nie istnieje: {path}")
    if not path.is_dir():
        sys.exit(f"Podana ścieżka nie jest katalogiem: {path}")

    print(f"Obserwuję katalog: {path.resolve()}")
    cache = scan_dir(path)
    print(f"Pierwsze skanowanie: znaleziono {len(cache)} plików.\n")
    try:
        while True:
            time.sleep(1)
            current = scan_dir(path)
            check_changes(current, cache)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
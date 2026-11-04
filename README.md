![CI](https://github.com/mmEmichael/url-normalizer/actions/workflows/ci.yml/badge.svg)

# url-normalizer

Python-библиотека для нормализации URL и определения источника ссылки.

## Возможности

- Нормализация URL для YouTube, Reddit и остальных сайтов.
- Определение источника ссылки (`YOUTUBE`, `REDDIT`, `GENERIC`).
- Извлечение ID видео YouTube и постов Reddit.
- Проверка некорректных URL через `InvalidURLError`.
- Не использует внешние зависимости во время выполнения.
- Не выполняет сетевые запросы.

## Установка

```bash
uv add url-normalizer
```

_Примечание: пока библиотека не опубликована в PyPI, установка производится из Git-репозитория или локального пути._

## Использование

```python
from url_normalizer import normalize, detect_source, extract_id, Source

url = "https://youtu.be/abc123?utm_source=telegram"

print(normalize(url))
# https://www.youtube.com/watch?v=abc123

print(detect_source(url))
# Source.YOUTUBE

print(extract_id(url))
# abc123
```

## Правила нормализации

### Общие правила

- Удаление пробелов по краям.
- Приведение схемы и домена к нижнему регистру.
- Удаление стандартных портов.
- Удаление URL-фрагментов.
- Удаление известных tracking-параметров.
- Сортировка оставшихся query-параметров.
- Удаление завершающего слэша у путей, кроме корневого.

### YouTube

- Поддерживаются `youtube.com`, `www.youtube.com`, `m.youtube.com`, `music.youtube.com`, `youtu.be`.
- Ссылки на видео приводятся к формату `https://www.youtube.com/watch?v=ID`.
- Поддерживаются ссылки `/watch`, `/shorts`, `/embed`, `/live` и короткие ссылки.
- Параметры времени и плейлиста у ссылок на видео удаляются.
- Ссылки на плейлисты сохраняют параметр `list`.

### Reddit

- Поддерживаются `reddit.com`, `www.reddit.com`, `old.reddit.com`, `m.reddit.com`, `redd.it`.
- Ссылки на посты приводятся к каноническому виду `https://www.reddit.com/r/SUBREDDIT/comments/ID/`.
- Slug после ID поста удаляется.
- Короткие ссылки `redd.it` не раскрываются без сетевого запроса.

### Остальные сайты

Применяются только общие правила нормализации.

## Принятые решения

- Библиотека не выполняет сетевые запросы.
- Неизвестные сайты обрабатываются как `GENERIC`.
- Короткие ссылки Reddit не раскрываются автоматически.
- Для определения источника сравнивается домен целиком, а не его часть.
- Нормализация идемпотентна: повторный вызов `normalize()` не меняет результат.

## Разработка и тестирование

Клонировать репозиторий и установить dev-зависимости:

```bash
uv sync
```

Запустить проверки:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest --cov --cov-report=term-missing
```

Минимальное требуемое покрытие тестами: 95%.

## Лицензия

Проект распространяется под лицензией MIT. Подробности — в файле [LICENSE](LICENSE).

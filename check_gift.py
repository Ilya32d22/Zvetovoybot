import httpx
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import os

# Используем твою палитру из 80 цветов (сокращенно для примера, вставь свою полную)
COLOR_PALETTE = {
    "Ivory White": [206, 206, 206], "Platinum": [169, 169, 163], "Roman Silver": [142, 144, 154],
    "Steel Grey": [117, 123, 126], "Battleship Grey": [119, 117, 105], "Feldgrau": [99, 107, 96],
    "Rifle Green": [75, 77, 66], "Black": [36, 36, 36], "Onyx Black": [59, 60, 60],
    "Gunmetal": [61, 72, 74], "Seal Brown": [89, 62, 55], "Burgundy": [145, 78, 83],
    "Rosewood": [169, 107, 100], "Desert Sand": [179, 155, 117], "Cappuccino": [163, 131, 109],
    "Chocolate": [150, 92, 65], "Chestnut": [188, 92, 61], "Carmine": [214, 62, 51],
    "Fire Engine": [232, 70, 63], "Burnt Sienna": [207, 99, 47], "Copper": [181, 112, 60],
    "Tomato": [228, 87, 46], "Mystic Pearl": [207, 106, 98], "Strawberry": [212, 105, 90],
    "Coral Red": [209, 109, 84], "Carrot Juice": [237, 139, 76], "Persimmon": [229, 129, 57],
    "Orange": [225, 142, 36], "Amber": [218, 165, 32], "Caramel": [210, 145, 36],
    "Mustard": [210, 140, 0], "Old Gold": [164, 130, 45], "Satin Gold": [179, 148, 51],
    "Pure Gold": [201, 168, 57], "Light Olive": [178, 159, 77], "Khaki Green": [148, 153, 90],
    "Pistachio": [138, 162, 102], "Camo Green": [115, 129, 63], "Lemongrass": [151, 184, 71],
    "Shamrock Green": [99, 172, 74], "Malachite": [91, 178, 70], "Mint Green": [110, 189, 122],
    "Emerald": [92, 181, 116], "Hunter Green": [107, 138, 83], "Pine Green": [99, 144, 111],
    "Tactical Pine": [66, 120, 99], "Dark Green": [63, 77, 47], "Ranger Green": [91, 100, 58],
    "Gunship Green": [85, 107, 86], "Jade Green": [71, 178, 139], "Pacific Green": [94, 186, 148],
    "Turquoise": [79, 182, 177], "Deep Cyan": [33, 169, 164], "Aquamarine": [77, 187, 181],
    "Pacific Cyan": [69, 169, 192], "Azure Blue": [107, 183, 212], "Sky Blue": [113, 178, 217],
    "Celtic Blue": [72, 158, 230], "Sapphire": [106, 149, 214], "French Blue": [81, 138, 191],
    "Moonstone": [129, 170, 168], "Silver Blue": [131, 153, 169], "Indigo Dye": [82, 110, 128],
    "Midnight Blue": [78, 83, 101], "Marine Blue": [91, 110, 158], "Cobalt Blue": [95, 127, 205],
    "Navy Blue": [111, 143, 223], "Neon Blue": [116, 134, 250], "Electric Indigo": [131, 114, 247],
    "Cyberpunk": [144, 121, 235], "Lavender": [178, 138, 224], "French Violet": [183, 104, 241],
    "Electric Purple": [198, 113, 229], "English Violet": [172, 141, 164], "Grape": [155, 112, 193],
    "Purple": [153, 97, 163], "Dark Lilac": [177, 131, 153], "Fandango": [204, 121, 156],
    "Mexican Pink": [225, 97, 139], "Raspberry": [215, 125, 129]
}


def analyze_single_link(url):
    # 1. Извлекаем имя из ссылки (например, CloverPin)
    gift_name = url.split('/')[-1].split('-')[0]

    # 2. Формируем путь к CDN (обычно ID можно достать через API,
    # но если есть скачанная папка, ищем в ней по имени)
    print(f"🔍 Анализируем подарок: {gift_name}")

    # Для теста: находим локальный файл, в имени которого есть это название
    folder = "telegram_gifts_png"
    target_file = None
    for f in os.listdir(folder):
        if gift_name.lower() in f.lower():
            target_file = os.path.join(folder, f)
            break

    if not target_file:
        return print("❌ Файл не найден в локальной папке. Сначала скачай его.")

    # 3. Анализ цветов (как в твоем основном скрипте)
    img = Image.open(target_file).convert("RGBA")
    img.thumbnail((100, 100))
    data = np.array(img)
    pixels = data[data[:, :, 3] > 100][:, :3]

    kmeans = KMeans(n_clusters=5, n_init=10).fit(pixels)
    dominant_rgb = kmeans.cluster_centers_[np.argmax(np.bincount(kmeans.labels_))]

    # 4. Считаем совместимость со ВСЕМИ фонами
    scores = []
    for name, rgb in COLOR_PALETTE.items():
        # Считаем расстояние (чем меньше, тем лучше)
        dist = np.linalg.norm(dominant_rgb - rgb)
        # Переводим в проценты (условно: dist 0 = 100%, dist 200 = 0%)
        compatibility = max(0, min(100, 100 - (dist / 2)))
        scores.append((name, compatibility))

    # 5. Сортируем и выводим ТОП-10
    scores.sort(key=lambda x: x[1], reverse=True)

    print(f"\n✅ Идеальный фон: {scores[0][0]} ({scores[0][1]:.1f}%)")
    print("\n📊 ТОП-10 Совместимых фонов:")
    for i, (name, pct) in enumerate(scores[:10], 1):
        print(f"{i}. {name}: {pct:.1f}%")

# Пример запуска
# analyze_single_link("https://t.me/nft/CloverPin-169271")
import os
from PIL import Image

ROOT_DIR = "images"
TARGET_SIZE = 3_500_000  # 1MB
VALID_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]


def compress_image(image_path):
    try:
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in VALID_EXTENSIONS:
            return

        original_size = os.path.getsize(image_path)
        if original_size <= TARGET_SIZE:
            print(f"✅ Đã đạt yêu cầu: {image_path} ({original_size // 1024} KB)")
            return

        img = Image.open(image_path)

        # Giữ chế độ gốc
        params = {}

        # Thiết lập chất lượng thấp hơn nếu có thể
        if ext in [".jpg", ".jpeg"]:
            params["quality"] = 85
            params["optimize"] = True
        elif ext == ".png":
            params["optimize"] = True
        elif ext == ".webp":
            params["quality"] = 80

        # Lưu tạm vào file .temp, rồi kiểm tra size
        temp_path = image_path + ".temp"
        img.save(temp_path, format=img.format, **params)

        new_size = os.path.getsize(temp_path)

        if new_size < original_size and new_size <= TARGET_SIZE:
            os.replace(temp_path, image_path)
            print(f"✅ Đã nén: {image_path} -> {new_size // 1024} KB")
        else:
            os.remove(temp_path)
            print(f"⚠️ Không thể giảm đủ: {image_path} (hiện tại {original_size // 1024} KB)")
    except Exception as e:
        print(f"❌ Lỗi với {image_path}: {e}")


def compress_all_images():
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            compress_image(file_path)


if __name__ == "__main__":
    compress_all_images()

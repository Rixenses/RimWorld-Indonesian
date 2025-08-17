# Untuk update/replace file Bahasa Indonesia ke "Path folder game RimWorld"
# Pastikan kamu sudah menginstall Python 3.x
# Running dengan "python syncTranslation.py"

import os
import shutil

# Path sumber hasil terjemahan
src_base = r"C:\Users\User\RimWorld-Indonesian"

# Path folder game RimWorld
dst_base = r"D:\SteamLibrary\steamapps\common\RimWorld\Data"

# Daftar folder Utama dan DLC yang mau disalin
dlc_list = ["Core", "Biotech", "Ideology", "Royalty", "Anomaly", "Odyssey"]

# Nama folder Languages yang akan dibuat di folder game
languages_folder = "Languages"

# ➜ Pakai nama folder bahasa yang kamu gunakan (biar konsisten)
language_name = "Indonesian (Bahasa Indonesia)"

# Folder-folder yang akan disalin ke dalam Languages\<language_name>
folders_to_copy = ["DefInjected", "Keyed", "Strings", "WordInfo"]

# File pendukung di Core folder bahasa
files_to_copy = ["LanguageInfo.xml", "LangIcon.png"]

def copy_tree_clean(src, dst):
    """Hapus dst kalau ada, lalu copy isi src -> dst."""
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

for dlc in dlc_list:
    src_dlc_path = os.path.join(src_base, dlc)
    dst_language_path = os.path.join(dst_base, dlc, languages_folder, language_name)

    if not os.path.exists(src_dlc_path):
        print(f"⚠ Folder sumber DLC tidak ditemukan: {src_dlc_path}")
        continue

    # Buat folder bahasa di dalam Languages jika belum ada
    os.makedirs(dst_language_path, exist_ok=True)

    # 1) Salin folder Utama dan DLC
    for folder_name in folders_to_copy:
        src_folder = os.path.join(src_dlc_path, folder_name)
        dst_folder = os.path.join(dst_language_path, folder_name)

        if os.path.isdir(src_folder):
            try:
                copy_tree_clean(src_folder, dst_folder)
                print(f"✅ {dlc}: Folder '{folder_name}' disalin ke '{language_name}'.")
            except Exception as e:
                print(f"❌ {dlc}: Gagal menyalin folder '{folder_name}': {e}")
        else:
            # Strings sering nggak ada di beberapa DLC—info aja
            if folder_name == "Strings":
                print(f"ℹ️ {dlc}: Folder '{folder_name}' tidak ada, dilewati.")
            else:
                print(f"⚠ {dlc}: Folder '{folder_name}' tidak ditemukan di sumber.")

    # 2) Salin file root (LanguageInfo.xml, LangIcon.png) kalau ada
    for fname in files_to_copy:
        src_file = os.path.join(src_dlc_path, fname)
        dst_file = os.path.join(dst_language_path, fname)

        if os.path.isfile(src_file):
            try:
                shutil.copy2(src_file, dst_file)
                print(f"✅ {dlc}: File '{fname}' disalin ke root '{language_name}'.")
            except Exception as e:
                print(f"❌ {dlc}: Gagal menyalin file '{fname}': {e}")
        else:
            # Untuk skip LanguageInfo.xml di folder DLC
            if fname == "LanguageInfo.xml" and dlc != "Core":
                print(f"ℹ️ {dlc}: '{fname}' tidak ditemukan (Dilewati).")
            else:
                print(f"ℹ️ {dlc}: '{fname}' tidak ditemukan di sumber.")

print("🎉 Semua berkas bahasa sudah diperbarui.")
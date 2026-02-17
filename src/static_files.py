import os
import shutil

def copy_to_public():
    if os.path.exists("public"):
        print("Deleting public directory...")
        shutil.rmtree("public")

    print("Copying static files to public directory...")
    copy_tree("static", "public")

def copy_tree(src: str, dst: str):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        print(f" * {src_path} -> {dst_path}")
        if os.path.isdir(src_path):
            copy_tree(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
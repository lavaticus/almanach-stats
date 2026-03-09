import os
import re

# ── CONFIG ────────────────────────────────────────────────────
# Set this to the folder containing your weapon PNGs.
# Use "." to run in the same folder as this script.
TARGET_DIR = "."

# ── MAIN ──────────────────────────────────────────────────────
def main():
    files = [f for f in os.listdir(TARGET_DIR) if f.lower().endswith('.png')]

    if not files:
        print("No PNG files found.")
        return

    deleted  = []
    renamed  = []
    skipped  = []

    for filename in sorted(files):
        name, ext = os.path.splitext(filename)
        filepath  = os.path.join(TARGET_DIR, filename)

        # Strip leading "T_"
        new_name = re.sub(r'^T_', '', name)

        # Strip trailing "_1" (but not e.g. "_12")
        new_name = re.sub(r'_1$', '', new_name)

        # Delete files ending with "_Square" — checked AFTER stripping _1
        # so it catches originals like T_Weapon_Square_1.png too
        if re.search(r'_[Ss]quare$', new_name):
            os.remove(filepath)
            deleted.append(filename)
            continue

        new_filename = new_name + ext
        new_filepath = os.path.join(TARGET_DIR, new_filename)

        if new_filename == filename:
            skipped.append(filename)
            continue

        # Avoid overwriting an existing file
        if os.path.exists(new_filepath):
            print(f"  [SKIP] {filename} → {new_filename} already exists, skipping.")
            skipped.append(filename)
            continue

        os.rename(filepath, new_filepath)
        renamed.append((filename, new_filename))

    # ── REPORT ────────────────────────────────────────────────
    print(f"\n{'─' * 52}")
    print(f"  WEAPON PNG RENAME — COMPLETE")
    print(f"{'─' * 52}")

    if renamed:
        print(f"\n  RENAMED ({len(renamed)}):")
        for old, new in renamed:
            print(f"    {old}  →  {new}")

    if deleted:
        print(f"\n  DELETED ({len(deleted)}) [_Square files]:")
        for f in deleted:
            print(f"    {f}")

    if skipped:
        print(f"\n  UNCHANGED ({len(skipped)}):")
        for f in skipped:
            print(f"    {f}")

    print(f"\n  Total: {len(renamed)} renamed, {len(deleted)} deleted, {len(skipped)} unchanged")
    print(f"{'─' * 52}\n")


if __name__ == "__main__":
    main()

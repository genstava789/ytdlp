import os
import re
import pysubs2

def convert_and_cleanup_subtitles(output_path="/storage/9C1C-01E7/Anime/", print_all=True):
    episode_pattern = re.compile(r"(EP\d+)", re.IGNORECASE)
    final_pattern = re.compile(r"^EP\d+\.srt$", re.IGNORECASE)

    for file_name in os.listdir(output_path):
        file_path = os.path.join(output_path, file_name)
        if not os.path.isfile(file_path):
            continue

        # Skip .srt files already matching final format
        if file_name.lower().endswith('.srt'):
            if final_pattern.match(file_name):
                if print_all:
                    print(f"Skipping '{file_name}': already renamed.")
                continue
            else:
                if print_all:
                    print(f"Skipping '{file_name}': srt file not matching rename pattern.")
                continue

        # Process only .vtt files
        if file_name.lower().endswith('.vtt'):
            match = episode_pattern.search(file_name)
            if not match:
                if print_all:
                    print(f"Skipping '{file_name}': no episode number found.")
                continue

            ep_number = match.group(1).upper()
            srt_target_name = f"{ep_number}.srt"
            srt_target_path = os.path.join(output_path, srt_target_name)
            vtt_file = file_path
            srt_file = vtt_file[:-4] + '.srt'  # temp srt file

            try:
                if os.path.exists(srt_target_path):
                    if print_all:
                        print(f"Skipping '{file_name}': '{srt_target_name}' already exists.")
                    os.remove(vtt_file)
                    continue

                # Convert .vtt to .srt
                subs = pysubs2.load(vtt_file, encoding="utf-8")
                subs.save(srt_file, encoding="utf-8")
                # Remove the original .vtt file
                os.remove(vtt_file)

                # Rename to standard format if needed
                if os.path.basename(srt_file) != srt_target_name:
                    os.rename(srt_file, srt_target_path)
                # Only print for new conversion/rename
                print(f"Renamed file to '{srt_target_name}'.")
            except Exception as e:
                print(f"Error processing '{file_name}': {e}")

"""
sync_subtitles.py
-----------------
Shift timestamps in .srt subtitle files forward or backward.

Features:
- Adjusts all timestamps by a positive or negative float (seconds)
- Processes all .srt files in a folder
- Prevents negative time rollover
- Creates new files with `_synced` suffix

Usage:
    python SubSync.py
"""
import re
from datetime import datetime, timedelta
from pathlib import Path

def sync_srt(file_path, output_path, shift_seconds):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def adjust_time(match):
        time_str = match.group(0)
        time_obj = datetime.strptime(time_str, '%H:%M:%S,%f')
        
        # Add the shift_seconds (supports both positive and negative floats)
        shifted_time = time_obj + timedelta(seconds=shift_seconds)
        
        # Safety Check: Prevent time from rolling backward into the previous day
        if shifted_time.year < 1900 or (shifted_time.year == 1900 and shifted_time.day < 1):
            shifted_time = datetime(1900, 1, 1, 0, 0, 0, 0)
            
        return shifted_time.strftime('%H:%M:%S,%f')[:-3]

    shifted_content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3}', adjust_time, content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(shifted_content)

def process_all_subtitles(folder_path, shift_seconds):
    folder = Path(folder_path)
    
    # Find all .srt files in the specified folder
    srt_files = list(folder.glob('*.srt'))
    
    if not srt_files:
        print(f"No .srt files found in the folder: {folder.resolve()}")
        return

    print(f"Found {len(srt_files)} subtitle file(s). Starting sync...")

    for file_path in srt_files:
        # Skip files that have already been synced to prevent endless loops
        if file_path.stem.endswith('_synced'):
            continue
            
        # Create a new filename (e.g., 'movie.srt' becomes 'movie_synced.srt')
        output_name = f"{file_path.stem}_synced{file_path.suffix}"
        output_path = folder / output_name
        
        # Process the file
        sync_srt(file_path, output_path, shift_seconds)
        print(f"✅ Processed: {file_path.name} -> {output_name}")

# Run the script on the current folder (".") 
# Use a negative number to shift backwards, or positive to shift forwards
process_all_subtitles(".", -9.2)

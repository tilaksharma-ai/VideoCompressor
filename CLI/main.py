import subprocess
import shutil
import os
import sys

def extreme_compress(input_path, output_path, target_bitrate="1500k", fps=None):
    """
    Compress video aggressively for very small file size.
    - target_bitrate: e.g., "1500k" (1.5 Mbps)
    - fps: e.g., "30" to reduce framerate (None to keep original)
    - Always outputs 720p.
    - Supports MOV without breaking video.
    """
    if not shutil.which("ffmpeg"):
        print("FFmpeg not installed!")
        return
    
    # Detect extension for MOV-specific handling
    ext = os.path.splitext(output_path)[1].lower()

    cmd = [
        "ffmpeg", "-i", input_path,
        "-vcodec", "libx265",           # H.265 codec
        "-crf", "28",                   # Strong compression
        "-preset", "medium",            # Compression speed
        "-b:v", target_bitrate,         # Target bitrate
        "-acodec", "aac",                # Audio codec
        "-b:a", "96k",                   # Audio bitrate
        "-vf", "scale=1280:720",        # Force 720p
        "-movflags", "+faststart"
    ]

    # Add FPS reduction if requested
    if fps:
        cmd.extend(["-r", str(fps)])

    # Special fix for MOV output
    if ext == ".mov":
        cmd.extend(["-pix_fmt", "yuv420p"])  # Ensures compatibility
    
    # Output file must be LAST
    cmd.append(output_path)
    
    subprocess.run(cmd, check=True)
    print(f"Compressed video saved as: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compress.py input.mp4 output.mp4")
    else:
        extreme_compress(
            sys.argv[1],
            sys.argv[2],
            target_bitrate="1000k",  # Try lowering for smaller files
            scale="1280:720",        # Downscale to 720p
            fps=30                   # Lower framerate
        )

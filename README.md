##SMART VIDEO RENAMER


**SmartVideoRenamer** is a Python-based application that automates the tedious task of organizing and renaming videos based on visual similarity to reference images. It uses the **Structural Similarity Index (SSIM)** to find the closest matching image for each video’s first frame and renames the video accordingly.

This tool is perfect for content creators, editors, and anyone working with large video libraries who wants to streamline organization.

---

## Key Features

- **Intelligent Matching**: Uses SSIM to compare video frames to reference images for accurate renaming.
- **Streamlit Interface**: Upload multiple videos and images easily through a web interface.
- **Automatic Resizing**: Normalizes image and video frame sizes for consistent matching.
- **ZIP Download**: Download all renamed videos as a single ZIP file.
- **Safe Cleanup**: Temporary files are automatically deleted after download to save space.
- **Preserves Original Logic**: Maintains your original matching and renaming workflow for reliability.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/SmartVideoRenamer.git
cd SmartVideoRenamer

import streamlit as st
import cv2
import os
from skimage.metrics import structural_similarity as ssim
import tempfile
import shutil

st.title("Video-to-Image Matching and Renaming")

# Upload images
st.header("Upload Reference Images (PNG)")
uploaded_images = st.file_uploader("Choose images", type=["png"], accept_multiple_files=True)

# Upload videos
st.header("Upload Videos (MP4)")
uploaded_videos = st.file_uploader("Choose videos", type=["mp4"], accept_multiple_files=True)

# Track processing state
files_processed = False
temp_dir = None
video_dir = None

if st.button("Process Videos"):

    if not uploaded_images or not uploaded_videos:
        st.warning("Please upload both images and videos!")
    else:
        # Temporary directories
        temp_dir = tempfile.mkdtemp()
        image_dir = os.path.join(temp_dir, "images")
        video_dir = os.path.join(temp_dir, "videos")
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(video_dir, exist_ok=True)

        # Save images
        images = {}
        for file in uploaded_images:
            img_path = os.path.join(image_dir, file.name)
            with open(img_path, "wb") as f:
                f.write(file.read())
            img = cv2.imread(img_path)
            img = cv2.resize(img, (256, 256))  # Keep original resizing logic
            images[file.name] = img

        # Save videos
        for file in uploaded_videos:
            vid_path = os.path.join(video_dir, file.name)
            with open(vid_path, "wb") as f:
                f.write(file.read())

        st.info("Processing videos...")

        renamed_videos = []
        for vfile in os.listdir(video_dir):
            if not vfile.endswith(".mp4"):
                continue

            vpath = os.path.join(video_dir, vfile)
            cap = cv2.VideoCapture(vpath)
            ret, frame = cap.read()
            cap.release()
            if not ret:
                st.warning(f"Cannot read video: {vfile}")
                continue

            frame = cv2.resize(frame, (256, 256))

            best_match = None
            best_score = -1

            # Original logic: match with SSIM
            for img_name, img in images.items():
                grayA = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                grayB = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                score, _ = ssim(grayA, grayB, full=True)
                if score > best_score:
                    best_score = score
                    best_match = img_name

            if best_match:
                new_name = os.path.splitext(best_match)[0] + ".mp4"
                new_path = os.path.join(video_dir, new_name)
                os.rename(vpath, new_path)
                renamed_videos.append((vfile, new_name, best_score))

        # Display results
        if renamed_videos:
            st.success("✅ Videos Renamed Successfully!")
            for old_name, new_name, score in renamed_videos:
                st.write(f"{old_name} → {new_name} (score={score:.2f})")
            files_processed = True
        else:
            st.warning("No videos were renamed.")

# Download ZIP and delete temporary files after download
if files_processed and video_dir:
    zip_path = "renamed_videos.zip"
    shutil.make_archive("renamed_videos", "zip", video_dir)

    with open(zip_path, "rb") as f:
        if st.download_button("Download Renamed Videos as ZIP", f, file_name="renamed_videos.zip"):
            # Delete temporary files and ZIP after download
            shutil.rmtree(temp_dir)
            os.remove(zip_path)
            st.info("✅ All temporary files have been deleted.")

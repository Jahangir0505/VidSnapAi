import os
import json
from generate_process import text_to_audio, create_reel
from pathlib import Path

# Vercel's handler function
def handler(request):
    try:
        # Check if the request is a POST request
        if request.method != "POST":
            return json.dumps({"status": "error", "message": "Method Not Allowed"}), 405

        # Get the folder_id from the JSON body
        body_data = json.loads(request.body.decode('utf-8'))
        folder = body_data.get('folder_id')

        if not folder:
            return json.dumps({"status": "error", "message": "Missing folder_id"}), 400

        print(f"Processing folder: {folder}")
        
        # In a real app, you would fetch user files from persistent storage.
        # Here, we'll create dummy files for demonstration.
        user_uploads_dir = Path("/tmp") / "user_uploads" / folder
        os.makedirs(user_uploads_dir, exist_ok=True)
        
        # Create a dummy desc.txt and input.txt file
        with open(user_uploads_dir / "desc.txt", "w") as f:
            f.write("This is a sample description for the reel.")
        with open(user_uploads_dir / "input.txt", "w") as f:
            f.write("dummy_video_1.mp4\ndummy_video_2.mp4")

        # Call the processing functions
        if text_to_audio(folder):
            if create_reel(folder):
                return json.dumps({"status": "success", "message": f"Reel for {folder} created."}), 200
            else:
                return json.dumps({"status": "error", "message": f"Failed to create reel for {folder}."}), 500
        else:
            return json.dumps({"status": "error", "message": f"Failed to generate audio for {folder}."}), 500

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500
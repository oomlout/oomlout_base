"""Flask web server that renders pages from the web_pages directory."""

import os
import subprocess
import sys
import threading
import hashlib
from importlib import import_module, reload
from pathlib import Path
from typing import Any, Dict
import json
import shutil
import pickle
from datetime import datetime

import yaml
from flask import Flask, abort, render_template, request, jsonify, send_from_directory
from jinja2 import TemplateNotFound


BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "web_pages"
STATIC_DIR = TEMPLATE_DIR / "static"
SITE_TITLE = BASE_DIR.name
LOCK_FILE = Path("C:/gh/oomlout_base/lock/working_all.lock")
CACHE_FILE = BASE_DIR / "words_cache.pkl"

# Global cache for word data
WORDS_CACHE = {}
LAST_PARTS_FINGERPRINT = ""

# Default values for OOMP form fields
OOMP_DEFAULTS = {
    "oomp_classification": "food",
    "oomp_type": "recipe",
    "oomp_size": "planner",
    "oomp_color": "label",
    "oomp_description_main": "",
    "oomp_description_extra": "",
    "oomp_manufacturer": "",
    "oomp_part_number": "",
    "extra": "",
}


def _load_port_config() -> int:
    """Load port configuration from web_port.yaml file."""
    port_file = BASE_DIR / "web_port.yaml"
    default_port = 5000
    
    if not port_file.exists():
        return default_port
    
    try:
        with port_file.open("r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
        
        if isinstance(config, dict) and "port" in config:
            port = config["port"]
            if isinstance(port, int) and 1 <= port <= 65535:
                return port
            else:
                print(f"[config] Invalid port value in {port_file}: {port}; using default {default_port}")
                return default_port
        else:
            print(f"[config] No 'port' key found in {port_file}; using default {default_port}")
            return default_port
    except Exception as exc:
        print(f"[config] Failed to load {port_file}: {exc}; using default {default_port}")
        return default_port

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
)
app.config["SITE_TITLE"] = SITE_TITLE


def load_words_cache():
    """Load words cache from disk if available."""
    global WORDS_CACHE
    
    if CACHE_FILE.exists():
        try:
            print("[cache] Loading words cache from disk...")
            with open(CACHE_FILE, 'rb') as f:
                WORDS_CACHE = pickle.load(f)
            print(f"[cache] Loaded {len(WORDS_CACHE)} words from cache")
        except Exception as e:
            print(f"[cache] Error loading cache: {e}")
            WORDS_CACHE = {}
    else:
        print("[cache] No cache file found, will build fresh cache")
        WORDS_CACHE = {}


def save_words_cache():
    """Save words cache to disk."""
    try:
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(WORDS_CACHE, f)
        print(f"[cache] Saved {len(WORDS_CACHE)} words to cache")
    except Exception as e:
        print(f"[cache] Error saving cache: {e}")


def _calculate_parts_fingerprint() -> str:
    """Create a stable fingerprint of parts and parts_old directory state."""
    hash_obj = hashlib.sha256()

    for base_name in ["parts", "parts_old"]:
        base_dir = BASE_DIR / base_name
        if not base_dir.exists():
            hash_obj.update(f"{base_name}:missing\n".encode("utf-8"))
            continue

        entries = []
        for item in base_dir.iterdir():
            if not item.is_dir():
                continue

            working_yaml = item / "working.yaml"
            if working_yaml.exists():
                mtime = working_yaml.stat().st_mtime
                size = working_yaml.stat().st_size
            else:
                mtime = 0
                size = 0

            entries.append((item.name, mtime, size))

        entries.sort(key=lambda x: x[0])
        hash_obj.update(f"{base_name}:count={len(entries)}\n".encode("utf-8"))
        for name, mtime, size in entries:
            hash_obj.update(f"{name}|{mtime}|{size}\n".encode("utf-8"))

    return hash_obj.hexdigest()


def load_all_word_data():
    """Load all word data from parts directories and cache them."""
    global WORDS_CACHE, LAST_PARTS_FINGERPRINT
    
    parts_dir = BASE_DIR / "parts"
    prefix = ""
    
    if not parts_dir.exists():
        print("[cache] Parts directory not found")
        return
    
    print("[cache] Loading all word data...")
    updated_count = 0
    new_count = 0
    fresh_cache = {}
    
    for item in parts_dir.iterdir():
        if item.is_dir() and item.name.startswith(prefix):
            word = item.name.replace(prefix, "")
            working_yaml_path = item / "working.yaml"
            
            # Check if we need to update this word
            needs_update = True
            if word in WORDS_CACHE:
                cached_mtime = WORDS_CACHE[word].get('_mtime', 0)
                if working_yaml_path.exists():
                    current_mtime = working_yaml_path.stat().st_mtime
                    if current_mtime == cached_mtime:
                        needs_update = False
            else:
                new_count += 1
            
            if needs_update and working_yaml_path.exists():
                try:
                    with open(working_yaml_path, 'r', encoding='utf-8') as f:
                        yaml_data = yaml.safe_load(f)
                    
                    # Store with metadata
                    fresh_cache[word] = {
                        'word': word,
                        'dir_name': item.name,
                        'data': yaml_data or {},
                        '_mtime': working_yaml_path.stat().st_mtime,
                        '_last_updated': datetime.now().isoformat()
                    }
                    updated_count += 1
                except Exception as e:
                    print(f"[cache] Error loading {word}: {e}")
                    fresh_cache[word] = {
                        'word': word,
                        'dir_name': item.name,
                        'data': {},
                        '_error': str(e),
                        '_mtime': 0,
                        '_last_updated': datetime.now().isoformat()
                    }
            elif working_yaml_path.exists() and word in WORDS_CACHE:
                # Keep existing entry when the source file timestamp is unchanged.
                fresh_cache[word] = WORDS_CACHE[word]

    WORDS_CACHE = fresh_cache
    LAST_PARTS_FINGERPRINT = _calculate_parts_fingerprint()
    
    print(f"[cache] Loaded {new_count} new words, updated {updated_count} changed words")
    print(f"[cache] Total words in cache: {len(WORDS_CACHE)}")
    
    # Save the cache
    save_words_cache()


def ensure_cache_current_for_explore():
    """Refresh cache when parts content changed since the last check."""
    global LAST_PARTS_FINGERPRINT

    current_fingerprint = _calculate_parts_fingerprint()
    if current_fingerprint != LAST_PARTS_FINGERPRINT:
        print("[cache] Parts change detected on /explore, rebuilding cache")
        load_all_word_data()


# Load cache on startup
load_words_cache()
load_all_word_data()

# No background monitoring - keep it simple


def run_working_all_with_file_lock():
    """Run working_all with file-based locking to prevent multiple instances."""
    
    # Check if already running
    if LOCK_FILE.exists():
        # Check if process is actually running (stale lock cleanup)
        try:
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
            
            # Try to check if process exists (Windows compatible)
            try:
                os.kill(pid, 0)  # This will raise if process doesn't exist
                # Process exists, refuse to run
                app.logger.info("working_all is already running, refusing to start another instance")
                return False
            except OSError:
                # Process doesn't exist, remove stale lock
                LOCK_FILE.unlink(missing_ok=True)
                
        except (ValueError, FileNotFoundError):
            # Invalid lock file, remove it
                LOCK_FILE.unlink(missing_ok=True)
    
    # Launch directly without threading to avoid Flask socket issues
    try:
        # Create lock file first
        current_pid = os.getpid()
        with open(LOCK_FILE, 'w') as f:
            f.write(str(current_pid))
        app.logger.info(f"Created lock file with PID {current_pid}")
        
        # Create command to run working_all in new CMD window
        # This will show all output and close automatically when done
        cmd = f'''start "Working All Process" cmd /c "echo Starting working_all.py... && python working_all.py && echo First run complete. Checking for new entries... && python working_all.py && echo Second run complete. && del "{LOCK_FILE}" && echo Lock removed. Processing complete!"'''
        
        app.logger.info("Launching working_all in new CMD window...")
        
        # Use subprocess.Popen instead of os.system to avoid Flask socket issues
        subprocess.Popen(cmd, shell=True, cwd=Path(__file__).parent)
        
        app.logger.info("CMD window launched successfully")
        return True
        
    except Exception as e:
        app.logger.error(f"Error launching working_all in CMD window: {e}")
        # Fallback: remove lock file if we couldn't start
        LOCK_FILE.unlink(missing_ok=True)
        return False
def get_working_all_status():
    """Get the current status of working_all execution."""
    is_running = LOCK_FILE.exists()
    
    status = {
        "is_running": is_running,
        "lock_file": str(LOCK_FILE)
    }
    
    if is_running:
        try:
            with open(LOCK_FILE, 'r') as f:
                status["pid"] = int(f.read().strip())
        except (ValueError, FileNotFoundError):
            status["pid"] = None
    
    return status


def _load_page_hooks():
    """Load (and hot-reload) the optional page hook module."""
    module_name = "web_pages.page_hooks"
    try:
        if module_name in globals().get("_hook_cache", {}):
            module = reload(globals()["_hook_cache"][module_name])
        else:
            module = import_module(module_name)
        globals().setdefault("_hook_cache", {})[module_name] = module
        return module
    except ModuleNotFoundError:
        return None


def _derive_page_title(template_name: str) -> str:
    """Return a fallback page title based on the template name."""
    base_name = template_name.rsplit(".", 1)[0]
    return base_name.replace("_", " ").title()


def render_page(template_name: str, **context: Any):
    """Render a template and run optional hooks around the render."""
    hooks = _load_page_hooks()
    context_data: Dict[str, Any] = {
        "site_title": app.config.get("SITE_TITLE", SITE_TITLE),
        "request_method": request.method,
    }
    context_data.update(context)
    context_data.setdefault("page_title", _derive_page_title(template_name))

    hook_meta: Dict[str, Any] = {"template": template_name}
    if hooks and hasattr(hooks, "before_render"):
        extra = hooks.before_render(template_name, context_data)
        if isinstance(extra, dict):
            context_data.update(extra)
        hook_meta["hook_module"] = getattr(hooks, "__name__", "web_pages.page_hooks")
    else:
        hook_meta["hook_module"] = None

    context_keys = sorted(context_data.keys())
    context_data.setdefault("debug_info", {}).update({**hook_meta, "context_keys": context_keys})
    app.logger.debug("Rendering %s with context keys: %s", template_name, context_keys)

    try:
        return render_template(template_name, **context_data)
    except TemplateNotFound:
        abort(404)


@app.route("/")
def index():
    """Serve the index page with spelling cards form."""
    return render_page("index.html", page_title=app.config.get("SITE_TITLE", SITE_TITLE))


@app.route("/make_spelling_cards", methods=["GET", "POST"])
def make_spelling_cards():
    """Make spelling cards form handler."""
    return render_page("make_spelling_cards.html", page_title="Make Spelling Cards")


@app.route("/run_batch_only", methods=["POST"])
def run_batch_only():
    """Run the batch file without adding anything to working.yaml."""
    import os
    from pathlib import Path
    
    try:
        working_dir = str(Path(__file__).parent)
        os.system(f'start "Working All" /D "{working_dir}" cmd /c run_working_all.bat')
        return {"success": True, "message": "Batch file started successfully!"}
    except Exception as e:
        return {"success": False, "message": f"Failed to start batch file: {e}"}


@app.route("/working_all_status")
def working_all_status():
    """Return the status of working_all execution."""
    status = get_working_all_status()
    return status


@app.route("/run_working_all", methods=["POST"])
def trigger_working_all():
    """Manually trigger working_all execution."""
    if LOCK_FILE.exists():
        print("[DEBUG] Lock file exists - entering queue mode")
        # Add run instruction to batch file for queuing
        batch_file = Path("C:/gh/oomlout_base/lock/working_all.bat")
        working_dir = str(BASE_DIR)
        
        # Create the command line
        command_line = f'cd /d "{working_dir}" && python working_all.py\n'
        print(f"[DEBUG] Command to queue: {command_line.strip()}")
        
        # Check if this command is already in the file
        if batch_file.exists():
            print(f"[DEBUG] Batch file exists at: {batch_file}")
            with open(batch_file, 'r') as f:
                existing_content = f.read()
            print(f"[DEBUG] Current batch file content:\n{existing_content}")
            if command_line.strip() in existing_content:
                print("[DEBUG] Command already in queue - skipping")
                return {"message": "working_all is already running - command already in queue"}
        else:
            print(f"[DEBUG] Batch file does not exist yet at: {batch_file}")
        
        # Append the command if not already there
        print("[DEBUG] Appending command to batch file")
        with open(batch_file, 'a') as f:
            f.write(command_line)
        print("[DEBUG] Command successfully added to queue")
        
        return {"message": "working_all is already running - added to queue in working_all.bat"}
    
    print("[DEBUG] No lock file - creating launcher batch file")
    
    # Create a temporary batch file with lock logic
    working_dir = str(BASE_DIR)
    lock_file_str = str(LOCK_FILE).replace('/', '\\')
    
    launcher_bat = BASE_DIR / "run_working_all_launcher.bat"
    
    batch_content = f'''@echo off
echo Starting working_all.py...
echo %TIME% > "{lock_file_str}"
cd /d "{working_dir}"
python working_all.py
python working_all.py
del "{lock_file_str}"
echo Done!
pause
'''
    
    print(f"[DEBUG] Creating launcher batch file at: {launcher_bat}")
    with open(launcher_bat, 'w') as f:
        f.write(batch_content)
    
    # Launch the batch file
    cmd = f'start "Working All" "{launcher_bat}"'
    print(f"[DEBUG] Executing command: {cmd}")
    os.system(cmd)
    os.system(cmd)
    
    return {"message": "Started working_all in new window"}


@app.route("/oomp_create", methods=["GET", "POST"])
def oomp_create():
    """Handle OOMP open hardware source creation."""
    print(f"[DEBUG] oomp_create route hit - method: {request.method}")
    
    if request.method == "GET":
        print("[DEBUG] Rendering oomp_create.html")
        return render_page("oomp_create.html", page_title="Create OOMP Entry", oomp_defaults=OOMP_DEFAULTS)
    
    # POST request - create the OOMP entry
    try:
        import re
        data = request.get_json()
        
        # Build OOMP ID from form data
        id_elements = [
            "oomp_classification",
            "oomp_type",
            "oomp_size",
            "oomp_color",
            "oomp_description_main",
            "oomp_description_extra",
            "oomp_manufacturer",
            "oomp_part_number",
        ]
        
        oomp_id_parts = []
        for element in id_elements:
            ele = data.get(element, "")
            if ele:
                # Clean the element: replace spaces and punctuation with underscore
                cleaned = re.sub(r'[^a-zA-Z0-9]+', '_', ele)
                # Remove leading/trailing underscores
                cleaned = cleaned.strip('_')
                # Replace multiple underscores with single underscore
                cleaned = re.sub(r'_+', '_', cleaned)
                if cleaned:  # Only add non-empty cleaned strings
                    oomp_id_parts.append(cleaned)
        
        # Join all parts with single underscore
        oomp_id = '_'.join(oomp_id_parts)
        
        # Create parts_source directory if it doesn't exist
        parts_dir = BASE_DIR / "parts_source" / oomp_id
        parts_dir.mkdir(parents=True, exist_ok=True)
        
        # Save working.yaml in the parts_source directory
        working_file = parts_dir / "working.yaml"
        with open(working_file, 'w') as f:
            yaml.dump(data, f)
        
        print(f"[DEBUG] Created OOMP entry: {oomp_id}")
        print(f"[DEBUG] Saved to: {working_file}")
        
        return {"message": f"OOMP entry created successfully", "oomp_id": oomp_id, "path": str(parts_dir)}
    except Exception as e:
        import traceback
        print(f"[ERROR] {e}")
        print(traceback.format_exc())
        return {"error": str(e), "traceback": traceback.format_exc()}, 400


@app.route("/<path:page_name>")
def serve_page(page_name: str):
    """Serve any template from the web_pages directory."""
    template_name = page_name if page_name.endswith(".html") else f"{page_name}.html"
    return render_page(template_name)








@app.route("/refresh_cache", methods=['POST'])
def refresh_cache():
    """Manually refresh the cache."""
    load_all_word_data()
    return jsonify({'success': True, 'message': f'Cache refreshed with {len(WORDS_CACHE)} words'})








@app.route("/delete_image/<path:image_path>", methods=['POST'])
def delete_image(image_path):
    """Delete a specific image file."""
    try:
        print(f"[delete_image] Received imagePath: {image_path}")
        # Normalize path separators for Windows
        image_path = image_path.replace('/', os.sep)
        file_path = BASE_DIR / image_path
        print(f"[delete_image] Resolved file_path: {file_path}")
        if file_path.exists() and file_path.is_file():
            # Don't allow deletion of working.yaml
            if file_path.name == 'working.yaml':
                print(f"[delete_image] Attempted to delete working.yaml, aborting.")
                return jsonify({'error': 'Cannot delete working.yaml'}), 400
            file_path.unlink()
            print(f"[delete_image] Deleted file: {file_path}")
            return jsonify({'success': True, 'message': f'Deleted {file_path.name}'})
        else:
            print(f"[delete_image] File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        print(f"[delete_image] Exception: {e}")
        return jsonify({'error': str(e)}), 500


from flask import make_response

# Global error handler for 500 errors to always return JSON
@app.errorhandler(500)
def internal_error(error):
    response = jsonify({'error': 'Internal server error', 'details': str(error)})
    response.status_code = 500
    return response




@app.route("/serve_file/<path:filepath>")
def serve_file(filepath):
    """Serve files from the parts directory."""
    # Normalize path separators for Windows
    filepath = filepath.replace('/', os.sep)
    file_path = BASE_DIR / filepath
    if file_path.exists() and file_path.is_file():
        return send_from_directory(file_path.parent, file_path.name)
    abort(404)


@app.route("/explore")
def explore():
    """Explore page with live client-side filtering."""
    ensure_cache_current_for_explore()

    # Get all words from cache, including archive tag for parts_old
    all_words = []
    for word, word_data in WORDS_CACHE.items():
        # Determine if part is archived
        archive = False
        parts_dir = BASE_DIR / "parts" / word_data['dir_name']
        parts_old_dir = BASE_DIR / "parts_old" / word_data['dir_name']
        if parts_old_dir.exists():
            archive = True
            preview_image = parts_old_dir / "initial_generated_2.png"
            preview_path = f"parts_old/{word_data['dir_name']}/initial_generated_2.png" if preview_image.exists() else None
        else:
            preview_image = parts_dir / "initial_generated_2.png"
            preview_path = f"parts/{word_data['dir_name']}/initial_generated_2.png" if preview_image.exists() else None

        has_preview = preview_image.exists()

        word_entry = {
            'word': word,
            'dir_name': word_data['dir_name'],
            'data': word_data.get('data', {}),
            'has_preview': has_preview,
            'preview_path': preview_path,
            'archive': archive
        }
        all_words.append(word_entry)

    # Sort alphabetically
    all_words.sort(key=lambda x: x['word'])

    return render_page("explore.html",
                      words=all_words,
                      total_items=len(all_words))


@app.route("/explore/<word_dir>")
def explore_detail(word_dir):
    """Explore detail page with image gallery and file management."""
    # Support archive query parameter
    archive = request.args.get('archive', '0') == '1'
    if archive:
        parts_dir = BASE_DIR / "parts_old" / word_dir
    else:
        parts_dir = BASE_DIR / "parts" / word_dir

    if not parts_dir.exists():
        abort(404)

    word = word_dir.replace("helen_school_english_spelling_keystage_two_word_card_", "")

    # Get all images
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
    images = []
    for file in parts_dir.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:
            # Convert path to use forward slashes for URLs
            rel_path = str(file.relative_to(BASE_DIR)).replace('\\', '/')
            images.append({
                'filename': file.name,
                'path': rel_path,
                'size': file.stat().st_size,
                'is_initial_generated_2': file.name.lower() == 'initial_generated_2.png'
            })

    # Sort with initial_generated_2.png first
    images.sort(key=lambda x: (not x['is_initial_generated_2'], x['filename']))

    # Get main display image (initial_generated_2.png or first image or None)
    main_image = None
    if images:
        main_image = next((img for img in images if img['is_initial_generated_2']), images[0])

    # List all files with sizes and types
    files = []
    for file in parts_dir.iterdir():
        if file.is_file():
            # Convert path to use forward slashes for URLs
            rel_path = str(file.relative_to(BASE_DIR)).replace('\\', '/')
            files.append({
                'filename': file.name,
                'path': rel_path,
                'size': file.stat().st_size,
                'ext': file.suffix.lower(),
                'is_yaml': file.name == 'working.yaml'
            })
    files.sort(key=lambda x: x['filename'])

    # Load YAML data
    working_yaml_path = parts_dir / "working.yaml"
    yaml_content = None
    if working_yaml_path.exists():
        try:
            with open(working_yaml_path, 'r', encoding='utf-8') as f:
                yaml_content = yaml.safe_load(f)
        except Exception as e:
            yaml_content = {"error": str(e)}

    # Get explanation files
    explanations = {}
    for exp_file in ['explanation_clip.txt', 'explanation_full.txt']:
        exp_path = parts_dir / exp_file
        if exp_path.exists():
            try:
                with open(exp_path, 'r', encoding='utf-8') as f:
                    explanations[exp_file] = f.read()
            except Exception as e:
                explanations[exp_file] = f"Error reading file: {e}"

    return render_page("explore_detail.html",
                      word=word,
                      word_dir=word_dir,
                      images=images,
                      main_image=main_image,
                      files=files,
                      yaml_content=yaml_content,
                      explanations=explanations)


@app.route("/delete_all_files/<word_dir>", methods=['POST'])
def delete_all_files(word_dir):
    """Delete all files in a word directory except working.yaml."""
    try:
        archive = request.args.get('archive', '0') == '1'
        if archive:
            parts_dir = BASE_DIR / "parts_old" / word_dir
        else:
            parts_dir = BASE_DIR / "parts" / word_dir
        if not parts_dir.exists():
            return jsonify({'success': False, 'error': 'Word directory not found'}), 404
        deleted_count = 0
        for file in parts_dir.iterdir():
            if file.is_file() and file.name != 'working.yaml':
                file.unlink()
                deleted_count += 1
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} files (kept working.yaml)',
            'count': deleted_count
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route("/delete_initial_generated/<word_dir>", methods=['POST'])
def delete_initial_generated(word_dir):
    """Delete only initial_generated*.png files in a word directory."""
    try:
        archive = request.args.get('archive', '0') == '1'
        if archive:
            parts_dir = BASE_DIR / "parts_old" / word_dir
        else:
            parts_dir = BASE_DIR / "parts" / word_dir
        if not parts_dir.exists():
            return jsonify({'success': False, 'error': 'Word directory not found'}), 404
        deleted_count = 0
        for file in parts_dir.iterdir():
            if file.is_file() and file.name.lower().startswith('initial_generated') and file.suffix.lower() == '.png':
                file.unlink()
                deleted_count += 1
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} initial_generated*.png files',
            'count': deleted_count
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == "__main__":
    port = _load_port_config()
    print(f"[config] Starting server on port {port}")
    
    # Print registered routes for debugging
    print("[routes] Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} [{','.join(rule.methods)}]")
    
    app.run(host="0.0.0.0", port=port, debug=False)

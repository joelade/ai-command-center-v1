"""
AI Command Center - Filesystem MCP Server
Author: j.adelubi
Description: FastAPI-based filesystem server for MCP (Model Context Protocol)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

def create_app(root: str = "/app/data"):
    app = FastAPI(title="MCP Filesystem")

    # Ensure data directory exists
    os.makedirs(root, exist_ok=True)

    # Serve files under /static (optional)
    app.mount("/static", StaticFiles(directory=root), name="static")

    @app.get("/")
    def list_files():
        items = []
        for entry in sorted(os.listdir(root)):
            path = os.path.join(root, entry)
            items.append({
                "name": entry,
                "is_dir": os.path.isdir(path),
                "size": os.path.getsize(path) if os.path.isfile(path) else None
            })
        return {"root": root, "files": items}

    @app.get("/files/{path:path}")
    def get_file(path: str):
        file_path = os.path.join(root, path)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Not found")
        if os.path.isdir(file_path):
            raise HTTPException(status_code=400, detail="Requested path is a directory")
        return FileResponse(file_path)

    return app

app = create_app(root="/app/data")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3333)
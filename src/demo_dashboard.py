"""Serve only the public classroom dashboard on localhost; no extra packages."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


DASHBOARD_ROOT = Path(__file__).resolve().parents[1] / "examples" / "dashboard_3d"
PUBLIC_ASSETS = {"index.html", "styles.css", "app.js", "sample_state.json"}


class DashboardHandler(SimpleHTTPRequestHandler):
    def is_public_asset(self) -> bool:
        requested = unquote(urlsplit(self.path).path)
        name = "index.html" if requested == "/" else requested.removeprefix("/")
        if name not in PUBLIC_ASSETS:
            return False
        path = Path(self.translate_path(self.path)).resolve()
        return path.is_relative_to(DASHBOARD_ROOT) and (path == DASHBOARD_ROOT or path.is_file())

    def do_GET(self) -> None:
        if not self.is_public_asset():
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self) -> None:
        if not self.is_public_asset():
            self.send_error(404)
            return
        super().do_HEAD()

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    if not (DASHBOARD_ROOT / "index.html").is_file():
        parser.error("Dashboard files are missing. Download or clone the complete repository.")
    handler = partial(DashboardHandler, directory=str(DASHBOARD_ROOT))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as exc:
        parser.error(f"Cannot start the local server: {exc}. Try --port 8001.")
    with server:
        print(f"Student 3D dashboard: http://127.0.0.1:{server.server_port}/", flush=True)
        print("Synthetic data only. Press Ctrl+C to stop.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()

"""Serve only the public classroom dashboard on localhost; no extra packages."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


DASHBOARD_ROOT = Path(__file__).resolve().parents[1] / "examples" / "dashboard_3d"


class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        path = Path(self.translate_path(self.path)).resolve()
        if not path.is_relative_to(DASHBOARD_ROOT) or path.is_dir() and path != DASHBOARD_ROOT:
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self) -> None:
        path = Path(self.translate_path(self.path)).resolve()
        if not path.is_relative_to(DASHBOARD_ROOT) or path.is_dir() and path != DASHBOARD_ROOT:
            self.send_error(404)
            return
        super().do_HEAD()


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

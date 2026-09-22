#!/usr/bin/env python3
"""
Servidor HTTP local para o AP BIM.
- Adiciona MIME type correto para .wasm (application/wasm)
- Adiciona MIME type correto para .ifc
- Adiciona headers para PWA
"""
import http.server
import socketserver
import os
import sys

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    # MIME types extras
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.wasm': 'application/wasm',
        '.ifc':  'application/x-step',
        '.webmanifest': 'application/manifest+json',
        '.json': 'application/json',
        '.js':   'application/javascript',
        '.mjs':  'application/javascript',
        '.svg':  'image/svg+xml',
    }

    def end_headers(self):
        # Headers úteis para PWA / cache / segurança
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        super().end_headers()

    def log_message(self, fmt, *args):
        # Log mais limpo
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        # Permite reutilizar a porta rapidamente
        socketserver.TCPServer.allow_reuse_address = True
        print(f"")
        print(f"  ██████╗ ██████╗     ██████╗ ██╗███╗   ███╗")
        print(f"  ██╔══██╗██╔══██╗    ██╔══██╗██║████╗ ████║")
        print(f"  ██████╔╝██████╔╝    ██████╔╝██║██╔████╔██║")
        print(f"  ██╔═══╝ ██╔═══╝     ██╔══██╗██║██║╚██╔╝██║")
        print(f"  ██║     ██║         ██████╔╝██║██║ ╚═╝ ██║")
        print(f"  ╚═╝     ╚═╝         ╚═════╝ ╚═╝╚═╝     ╚═╝")
        print(f"")
        print(f"  Servidor AP BIM rodando em:")
        print(f"  → http://localhost:{PORT}")
        print(f"")
        print(f"  Para iPhone, use o IP do PC (veja com 'ipconfig'):")
        print(f"  → http://<SEU-IP>:{PORT}")
        print(f"")
        print(f"  Pressione Ctrl+C para parar.")
        print(f"")
        httpd.serve_forever()
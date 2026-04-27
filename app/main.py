from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from app.services.llm import generate_llm_answer

memory = {}

class Handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        if self.path == "/query":
            data = json.loads(body)

            query = data.get("query", "")
            session_id = data.get("session_id", "default")
            file_text = data.get("file_text", "")

            history = memory.get(session_id, "")

            context = ""
            if file_text:
                context += f"\nDOCUMENT:\n{file_text[:6000]}\n"

            context += f"\nHISTORY:\n{history}"

            answer = generate_llm_answer(query, context)

            memory[session_id] = history + f"\nUser: {query}\nAI: {answer}"

            self._set_headers()
            self.wfile.write(json.dumps({"answer": answer}).encode())

        else:
            self._set_headers()
            self.wfile.write(json.dumps({"error": "Invalid route"}).encode())


def run():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, Handler)
    print("Server running on port 10000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
#!/usr/bin/env python3.8
import http.client, http.server, io, os, re, socket, socketserver, sqlite3, sys, subprocess, traceback, urllib.parse, urllib.request, xml.etree.ElementTree
import json
import requests

LISTEN_ADDRESS, LISTEN_PORT = "0.0.0.0", 65412
HTML_PREFIX, HTML_POSTFIX = "<!DOCTYPE html>\n<html>\n<head>\n", "</body>\n</html>"
USERS_XML = """<?xml version="1.0" encoding="utf-8"?><users><user id="0"><username>admin</username><name>admin</name><surname>admin</surname><password>7en8aiDoh!</password></user><user id="1"><username>dricci</username><name>dian</name><surname>ricci</surname><password>12345</password></user><user id="2"><username>amason</username><name>anthony</name><surname>mason</surname><password>gandalf</password></user><user id="3"><username>svargas</username><name>sandra</name><surname>vargas</surname><password>phest1945</password></user></users>"""


def init():
    global connection
    http.server.HTTPServer.allow_reuse_address = True

    # preparation data for vulnerable SQL Injection
    connection = sqlite3.connect(":memory:", isolation_level=None, check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, name TEXT, surname TEXT, password TEXT)")
    cursor.executemany("INSERT INTO users(id, username, name, surname, password) VALUES(NULL, ?, ?, ?, ?)", ((_.findtext("username"), _.findtext("name"), _.findtext("surname"), _.findtext("password")) for _ in xml.etree.ElementTree.fromstring(USERS_XML).findall("user")))
    cursor.execute("CREATE TABLE comments(id INTEGER PRIMARY KEY AUTOINCREMENT, comment TEXT, time TEXT)")


class ReqHandler(http.server.BaseHTTPRequestHandler):

    def _check_signature(self, data, param_signature):
        self.client_address
        signature = {
            "SQL Injection": ["'", "select", "SELECT"],
            "Remote File Inclusion": ["https", "http", ":", "/"],
            "Path Traversal": ["..", "/", "etc", "passwd", "shadow"]
        }
        for item in signature[param_signature]:
            if item in data:
                r = requests.post('http://beta:5000/attack/', json={"attack_name": "{} had attempt {}".format(self.client_address[0], param_signature)})
                break

    def do_GET(self):

        path, query = self.path.split('?', 1) if '?' in self.path else (self.path, "")
        code, content, params, cursor = http.client.OK, HTML_PREFIX, dict((match.group("parameter"), urllib.parse.unquote(','.join(re.findall(r"(?:\A|[?&])%s=([^&]+)" % match.group("parameter"), query)))) for match in re.finditer(r"((\A|[?&])(?P<parameter>[\w\[\]]+)=)([^&]+)", query)), connection.cursor()
        f = open("log_alpha.txt", "a")
        f.write(path)
        f.write("\n")
        f.write(query)
        f.write("\n")
        f.write(json.dumps(code))
        f.write("\n")
        f.write(content)
        f.write("\n")
        f.write(json.dumps(params))
        f.write("\n")
        f.write(str(cursor))
        f.write("\n")
        f.close()
        try:
            if path == '/':
                if "id" in params:
                    self._check_signature(params["id"], "SQL Injection")
                    cursor.execute("SELECT id, username, name, surname FROM users WHERE id=" + params["id"])
                    content += "<div><span>Result(s):</span></div><table><thead><th>id</th><th>username</th><th>name</th><th>surname</th></thead>%s</table>%s" % ("".join("<tr>%s</tr>" % "".join("<td>%s</td>" % ("-" if _ is None else _) for _ in row) for row in cursor.fetchall()), HTML_POSTFIX)
                elif "v" in params:
                    content += re.sub(r"(v<b>)[^<]+(</b>)", r"\g<1>%s\g<2>" % params["v"], HTML_POSTFIX)
                elif "include" in params:
                    self._check_signature(params["include"], "Remote File Inclusion")
                    backup, sys.stdout, program, envs = sys.stdout, io.StringIO(), (open(params["include"], "rb") if not "://" in params["include"] else urllib.request.urlopen(params["include"])).read(), {"DOCUMENT_ROOT": os.getcwd(), "HTTP_USER_AGENT": self.headers.get("User-Agent"), "REMOTE_ADDR": self.client_address[0], "REMOTE_PORT": self.client_address[1], "PATH": path, "QUERY_STRING": query}
                    exec(program, envs)
                    content += sys.stdout.getvalue()
                    sys.stdout = backup
                elif "path" in params:
                    self._check_signature(params["path"], "Path Traversal")
                    content = (open(os.path.abspath(params["path"]), "rb") if not "://" in params["path"] else urllib.request.urlopen(params["path"])).read().decode()
                if HTML_PREFIX in content and HTML_POSTFIX not in content:
                    content += """
                    <div><span>Vulnerable endpoint:</span></div>
                    <ul>
                    <li><a href="?id=2">SQL Injection</a></li>
                    <li><a href="/?path=">Path Traversal</a></li>
                    <li><a href="/?include=">Remote File Inclusion</a></li>
                    </ul>
                    """
            else:
                code = http.client.NOT_FOUND
        except Exception as ex:
            content = ex.output if isinstance(ex, subprocess.CalledProcessError) else traceback.format_exc()
            code = http.client.INTERNAL_SERVER_ERROR
        finally:
            self.send_response(code)
            self.send_header("Connection", "close")
            self.send_header("X-XSS-Protection", "0")
            self.send_header("Content-Type", "%s%s" % ("text/html" if content.startswith("<!DOCTYPE html>") else "text/plain", "; charset=%s" % params.get("charset", "utf8")))
            self.end_headers()
            self.wfile.write(("%s%s" % (content, HTML_POSTFIX if HTML_PREFIX in content else "")).encode())
            self.wfile.flush()


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        http.server.HTTPServer.server_bind(self)


if __name__ == "__main__":
    init()
    try:
        ThreadingServer((LISTEN_ADDRESS, LISTEN_PORT), ReqHandler).serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print("[x] exception occurred ('%s')" % ex)
    finally:
        os._exit(0)

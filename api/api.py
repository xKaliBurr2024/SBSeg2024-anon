from flask_cors import CORS
from flask import Flask, request
from subprocess import getoutput


app = Flask(__name__)


@app.route('/ip', methods=['GET'])
def get_ip():
    host = request.args.get('host', None)
    if host is None:
        return 'Please provide a host', 400

    ip = getoutput(f'host {host} | grep -m 1 address | awk -F " " "{{print $4}}"')
    return ip, 200


@app.route('/whatweb', methods=['GET'])
def get_whatweb():
    url = request.args.get('url', None)
    if url is None:
        return 'Please provide a url', 400

    whatweb = getoutput(f'whatweb -v -a 3 --colour=NEVER {url}')
    return whatweb, 200


@app.route('/reverse_dns', methods=['GET'])
def get_reverse_dns():
    ip = request.args.get('ip', None)
    if ip is None:
        return 'Please provide an ip', 400

    dns = getoutput(f'dnsrecon -r {ip}/24 -n 8.8.8.8')
    return dns, 200


@app.route('/sub_dns', methods=['GET'])
def get_sub_dns():
    host = request.args.get('host', None)
    if host is None:
        return 'Please provide a host', 400

    try:
        sub_dns = getoutput(f'dnsmap {host}')
        return sub_dns, 200
    except Exception as ex:
        print(ex)
        return 'Error', 500


@app.route('/whois', methods=['GET'])
def get_whois():
    ip = request.args.get('ip', None)
    if ip is None:
        return 'Please provide an ip', 400

    whois = getoutput(f'whois {ip}')
    return whois, 200


@app.route('/banner', methods=['GET'])
def get_banner():
    url = request.args.get('url', None)
    if url is None:
        return 'Please provide a url', 400

    banner = getoutput(f'curl -k -v {url}')
    return banner, 200


@app.route('/directory_scan', methods=['GET'])
def get_directory_scan():
    ip = request.args.get('ip', None)
    if ip is None:
        return 'Please provide a ip', 400

    directory_scan = getoutput(f'gobuster dir -u {ip} -w directory-list-2.3-medium.txt -b 301,302,403,404')
    return directory_scan, 200


@app.route('/ports', methods=['GET'])
def get_port_scan():
    ip = request.args.get('ip', None)
    if ip is None:
        return 'Please provide a ip', 400

    port_scan = getoutput(f'nmap -sS -sV {ip} | grep open')
    return port_scan, 200


if __name__ == '__main__':
    CORS(app, origins='*')
    app.run(debug=True, port=5001, host='0.0.0.0')

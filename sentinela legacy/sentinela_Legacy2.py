import os, sys, time, socket, hashlib, random, string, platform, subprocess

# --- [0] AUTO-INSTALADOR DE ELITE ---
def install_dependencies():
    libs = ["scapy", "psutil", "requests"]
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            print(f"[*] Sentinela detectou falta da biblioteca: {lib}. Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Executa a verificação antes de qualquer coisa
install_dependencies()

# Agora importamos com segurança
import psutil, requests
from scapy.all import ARP, Ether, srp

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.name == 'nt': os.system('color 0a')

def banner():
    print(r"""
    ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      █████╗ 
    ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔══██╗
    ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ███████║
    ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║
    ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗██║  ██║
    ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝
    """)
    print(f"{'='*80}\n  SISTEMA OPERACIONAL SENTINELA V8.2 | POR: @fran.codes | BIBLIOTECA MAHAL\n{'='*80}")

# --- [1] RED TEAM: AUDITORIA COM PLANO DE REMEDIAÇÃO ---
def web_audit():
    limpar(); banner()
    url = input("URL para Auditoria (ex: https://biblioteca.mahal.pro/): ")
    if not url.startswith("http"): url = "https://" + url
    
    print(f"[*] Analisando blindagem e gerando plano de remediação para {url}...\n")
    try:
        res = requests.get(url, timeout=5)
        h = res.headers
        
        solutions = {
            'X-Frame-Options': {
                'desc': 'Clickjacking',
                'solucao': 'add_header X-Frame-Options "SAMEORIGIN";',
                'onde': 'Configuração do Servidor (Nginx/Apache) ou .htaccess'
            },
            'Content-Security-Policy': {
                'desc': 'XSS (Injeção)',
                'solucao': "meta http-equiv='Content-Security-Policy' content=\"default-src 'self'\"",
                'onde': 'Tag <head> do seu HTML ou Header do Servidor'
            },
            'Strict-Transport-Security': {
                'desc': 'MITM / SSL Strip',
                'solucao': 'Strict-Transport-Security "max-age=31536000; includeSubDomains"',
                'onde': 'Configurações de SSL no seu Host ou Cloudflare'
            },
            'X-Content-Type-Options': {
                'desc': 'MIME Sniffing',
                'solucao': 'add_header X-Content-Type-Options "nosniff";',
                'onde': 'Configuração do Servidor'
            }
        }

        print(f"{'STATUS':<12} | {'RISCO':<22} | {'COMO CORRIGIR (COPIE O CÓDIGO)'}")
        print("-" * 110)

        for header, info in solutions.items():
            if header not in h:
                print(f"🔴 VULNERÁVEL | {info['desc']:<22} | {info['solucao']}")
                print(f"{' ':<12} | [ONDE APLICAR]: {info['onde']}")
            else:
                print(f"🟢 PROTEGIDO  | {info['desc']:<22} | Proteção ativa detectada.")
            print("-" * 110)

    except Exception as e:
        print(f"[!] Erro ao alcançar o alvo: {e}")
    input("\n[Pressione ENTER para voltar]")

# --- [2] BLUE TEAM: DEFESA ATIVA ---
def system_defense():
    limpar(); banner()
    print("[!] MONITOR DE CONEXÕES EM TEMPO REAL")
    conns = psutil.net_connections()
    targets = []
    print(f"{'IDX':<5} {'PROCESSO':<15} {'REMOTE ADDR':<20} {'STATUS'}")
    idx = 0
    for c in conns:
        if c.raddr and c.status == 'ESTABLISHED':
            try:
                proc = psutil.Process(c.pid)
                name = proc.name()
                print(f"[{idx:<3}] {name[:15]:<15} {c.raddr.ip}:{c.raddr.port:<14} {c.status}")
                targets.append(c.pid); idx += 1
            except: continue
    
    if not targets:
        print("\n[!] Nenhuma conexão externa ativa detectada.")
    else:
        sel = input("\nIDX para Neutralizar Processo (ou 'c' para cancelar): ")
        if sel.isnumeric() and int(sel) < len(targets):
            psutil.Process(targets[int(sel)]).terminate()
            print("[+] Ameaça Neutralizada!"); time.sleep(1)
    input("\n[ENTER]")

# --- [3] NETWORK: SCANNER DE DISPOSITIVOS ---
def network_recon():
    limpar(); banner()
    print("[!] SCANNER DE REDE LOCAL (ARP RECON)")
    try:
        ip_local = socket.gethostbyname(socket.gethostname())
        rede = ".".join(ip_local.split(".")[:-1]) + ".1/24"
        print(f"[*] Procurando invasores em: {rede}\n")
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=rede), timeout=2, verbose=0)
        for s, r in ans:
            print(f" -> IP: {r.psrc} | MAC: {r.hwsrc}")
    except PermissionError:
        print("[!] ERRO: Você precisa rodar como ADMINISTRADOR para escanear a rede.")
    except Exception as e:
        print(f"[!] Aviso: {e}")
    input("\n[VOLTAR]")

# --- [4] OSINT: INTELIGÊNCIA EXTERNA ---
def osint_search():
    limpar(); banner()
    alvo = input("IP ou Domínio para Investigação: ")
    try:
        info = requests.get(f"http://ip-api.com/json/{alvo}").json()
        print(f"\n[+] LOCALIZAÇÃO: {info.get('city')}, {info.get('country')}")
        print(f"[+] PROVEDOR: {info.get('isp')} | Org: {info.get('org')}")
        print(f"[+] COORDENADAS: {info.get('lat')}, {info.get('lon')}")
    except:
        print("Falha na inteligência externa.")
    input("\n[VOLTAR]")

# --- [5] KIT FERRAMENTAS ---
def tool_kit():
    limpar(); banner()
    print("1. Gerar Hash SHA-256 (Integridade)\n2. Gerador de Senhas Master\n0. Voltar")
    op = input("\nEscolha: ")
    if op == "1":
        path = input("Arraste o ficheiro: ").strip('"')
        with open(path, "rb") as f:
            print(f"\n[+] HASH: {hashlib.sha256(f.read()).hexdigest()}")
    elif op == "2":
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        print(f"\n[+] SENHA SEGURA: {''.join(random.choice(chars) for _ in range(20))}")
    input("\n[ENTER]")

# --- LOOP PRINCIPAL ---
while True:
    limpar(); banner()
    print(" [ 1 ] Auditoria Web (Com Plano de Remediação)")
    print(" [ 2 ] Defesa Ativa (Neutralizar Conexões)")
    print(" [ 3 ] Recon Rede (Ver quem está no seu Wi-Fi)")
    print(" [ 4 ] OSINT (Rastrear IP/Domínio)")
    print(" [ 5 ] Kit de Ferramentas (Hash/Senhas)")
    print(" [ 0 ] SAIR")
    
    escolha = input("\nSentinela > ")
    if escolha == "1": web_audit()
    elif escolha == "2": system_defense()
    elif escolha == "3": network_recon()
    elif escolha == "4": osint_search()
    elif escolha == "5": tool_kit()
    elif escolha == "0": break
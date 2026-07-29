# ADP 平台环境探测脚本
# 在 ADP 平台的脚本工具中粘贴此代码并运行，将输出结果贴回


# 请保存函数名为main,输入输出均为dict；最终结果会以json字符串方式返回，请勿直接返回不支持json.dumps的对象
def main(params: dict) -> dict:
    import os, json, subprocess, socket

    # 1. 环境变量（筛选可能含平台标识的，密钥脱敏）
    env_hits = {}
    for k, v in os.environ.items():
        kl = k.lower()
        if any(w in kl for w in ('adp', 'anydev', 'agent', 'entrypoint', 'cfbundle', 'claw',
                                   'codebuddy', 'workbuddy', 'platform', 'tenant', 'env',
                                   'container', 'pod', 'namespace', 'host', 'qclaw')):
            if any(s in kl for s in ('token', 'key', 'secret', 'password', 'auth')):
                env_hits[k] = '<present, len={}>'.format(len(v))
            else:
                env_hits[k] = v

    # 2. 进程树
    proc_chain = []
    try:
        pid = os.getpid()
        for _ in range(15):
            out = subprocess.run(
                ['ps', '-o', 'ppid=,args=', '-p', str(pid)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, timeout=2
            ).stdout.strip()
            if not out:
                break
            seg = out.split(None, 1)
            proc_chain.append({
                'pid': pid,
                'cmdline': seg[1] if len(seg) > 1 else '',
                'ppid': seg[0]
            })
            ppid = seg[0]
            if ppid in ('0', '1', str(pid)):
                break
            pid = int(ppid)
    except Exception as e:
        proc_chain.append({'error': str(e)})

    # 3. 主机名
    hostname = ''
    try:
        hostname = socket.gethostname()
    except Exception:
        pass

    return {
        'env_hits': env_hits,
        'proc_chain': proc_chain,
        'hostname': hostname,
        'platform': str(os.uname()) if hasattr(os, 'uname') else '',
    }

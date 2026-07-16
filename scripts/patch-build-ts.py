import re, sys
path = sys.argv[1]
with open(path) as f:
    c = f.read()
c = re.sub(r'\s*\{\s*\n\s*os:\s*"win32",\s*\n\s*arch:\s*"arm64",\s*\n\s*\},', '', c)
with open(path, 'w') as f:
    f.write(c)
print('Patched build.ts: removed win32-arm64 target')

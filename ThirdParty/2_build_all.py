import os, platform, subprocess, sys, re

def check_msvc_env():
    try:
        cl_out = subprocess.run('cl', capture_output=True).stderr.decode()
    except:
        print('Run script from Visual Studio Command Prompt!')
        sys.exit(123)
    m = re.search(r'Microsoft \(R\) C\/C\+\+ Optimizing Compiler Version ([\w.]+) for (\w+)', cl_out)
    res = (m.group(1), m.group(2))
    print("CL compiler: version [%s], arch [%s]" % res)
    return res

def build_arch(compiler, arch, *, libcxx = None, runtime = None, buildtype = 'Release'):
    cmd = 'conan install . -s compiler="%s" -s arch="%s"' % (compiler, arch)
    if libcxx is not None:
        cmd += ' -s compiler.libcxx="%s"' % libcxx
    if runtime is not None:
        cmd += ' -s compiler.runtime=%s' % runtime
    if buildtype is not None:
        cmd += ' -s build_type=%s' % buildtype
    cmd += ' --build outdated'
    print("CMD: %s" % cmd)
    yesno = input('continue? (yes/no):')
    if yesno != 'yes':
        sys.exit(111)
    os.system(cmd)


assert platform.machine().endswith('64'), "Use 64-bit OS for builds"

sysname = platform.system().lower()
if 'windows' in sysname:
    is64bit = (check_msvc_env()[1] == 'x64')
    if is64bit:
        build_arch('Visual Studio', 'x86_64', runtime='MT') #, buildtype='RelWithDebInfo')
    else:
        build_arch('Visual Studio', 'x86', runtime='MT') #, buildtype='RelWithDebInfo')
else:
    build_arch('gcc', 'x86_64', libcxx='libstdc++')
    build_arch('gcc', 'x86', libcxx='libstdc++')
nsconfig = """
name: "python sandbox",
mode: ONCE,

hostname: "python_sandbox",
cwd: "/tmp",

rlimit_as: 4096
rlimit_cpu: 1000
rlimit_fsize: 1000
rlimit_nofile: 10000

time_limit: {{NSJAIL_TIMEOUT}}

clone_newnet: false
clone_newuser:  true
# clone_newipc: false
# clone_newpid: false
# clone_newns: false
# clone_newcgroup: false
# clone_newuts: false

iface_no_lo: true

keep_caps: false
keep_env:true
mount_proc: true

uidmap {
    inside_id: "99999"
    outside_id: ""
    count: 1
}

gidmap {
    inside_id: "65534"
    outside_id: ""
    count: 1
}

mount {
    src: "/bin"
    dst: "/bin"
    is_bind: true
}

mount {
    src: "/lib"
    dst: "/lib"
    is_bind: true
}

mount {
    src: "/lib64"
    dst: "/lib64"
    is_bind: true
    mandatory: false
}

mount {
    src: "/usr"
    dst: "/usr"
    is_bind: true
}

mount {
    src: "/dev/null"
    dst: "/dev/null"
    is_bind: true
    rw: true
}

mount {
    src: "/etc"
    dst: "/etc"
    is_bind: true
}

mount {
    dst: "/dev/shm"
    fstype: "tmpfs"
    rw: true
    is_bind: false
}

mount {
    src: "/dev/random"
    dst: "/dev/random"
    is_bind: true
}


mount {
    dst: "/tmp"
    fstype: "tmpfs"
    rw: true
    options: "size=500000000"
}

mount {
    src: "{{process_dir}}/script.py"
    dst: "/tmp/script.py"
    is_bind: true
}

mount {
    src: "{{process_dir}}/result.txt"
    dst: "/tmp/result.txt"
    is_bind: true
    rw: true
}

envar: "HOME=/tmp"
envar: "PATH=/usr/local/bin:/usr/bin:/bin"
"""

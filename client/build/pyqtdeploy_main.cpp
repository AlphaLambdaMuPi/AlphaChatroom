#include <Python.h>
#include <QtGlobal>

#if PY_MAJOR_VERSION >= 3
extern "C" PyObject *PyInit__json(void);
extern "C" PyObject *PyInit_binascii(void);
extern "C" PyObject *PyInit__datetime(void);
extern "C" PyObject *PyInit__sha1(void);
extern "C" PyObject *PyInit__pickle(void);
extern "C" PyObject *PyInit_pyexpat(void);
extern "C" PyObject *PyInit__md5(void);
extern "C" PyObject *PyInit__multiprocessing(void);
extern "C" PyObject *PyInit__ctypes(void);
extern "C" PyObject *PyInit__ssl(void);
extern "C" PyObject *PyInit_mmap(void);
extern "C" PyObject *PyInit_select(void);
extern "C" PyObject *PyInit__sha256(void);
extern "C" PyObject *PyInit__random(void);
extern "C" PyObject *PyInit_array(void);
extern "C" PyObject *PyInit__socket(void);
extern "C" PyObject *PyInit_math(void);
extern "C" PyObject *PyInit__heapq(void);
extern "C" PyObject *PyInit__sha512(void);
extern "C" PyObject *PyInit_time(void);
extern "C" PyObject *PyInit__bisect(void);
#if !defined(Q_OS_WIN)
extern "C" PyObject *PyInit__posixsubprocess(void);
extern "C" PyObject *PyInit_grp(void);
#endif
#if defined(Q_OS_WIN)
extern "C" PyObject *PyInit_msvcrt(void);
extern "C" PyObject *PyInit__winapi(void);
#endif

static struct _inittab extension_modules[] = {
    {"_json", PyInit__json},
    {"binascii", PyInit_binascii},
    {"_datetime", PyInit__datetime},
    {"_sha1", PyInit__sha1},
    {"_pickle", PyInit__pickle},
    {"pyexpat", PyInit_pyexpat},
    {"_md5", PyInit__md5},
    {"_multiprocessing", PyInit__multiprocessing},
    {"_ctypes", PyInit__ctypes},
    {"_ssl", PyInit__ssl},
    {"mmap", PyInit_mmap},
    {"select", PyInit_select},
    {"_sha256", PyInit__sha256},
    {"_random", PyInit__random},
    {"array", PyInit_array},
    {"_socket", PyInit__socket},
    {"math", PyInit_math},
    {"_heapq", PyInit__heapq},
    {"_sha512", PyInit__sha512},
    {"time", PyInit_time},
    {"_bisect", PyInit__bisect},
#if !defined(Q_OS_WIN)
    {"_posixsubprocess", PyInit__posixsubprocess},
    {"grp", PyInit_grp},
#endif
#if defined(Q_OS_WIN)
    {"msvcrt", PyInit_msvcrt},
    {"_winapi", PyInit__winapi},
#endif
    {NULL, NULL}
};
#else
extern "C" void init_json(void);
extern "C" void initbinascii(void);
extern "C" void init_datetime(void);
extern "C" void init_sha1(void);
extern "C" void init_pickle(void);
extern "C" void initpyexpat(void);
extern "C" void init_md5(void);
extern "C" void init_multiprocessing(void);
extern "C" void init_ctypes(void);
extern "C" void init_ssl(void);
extern "C" void initmmap(void);
extern "C" void initselect(void);
extern "C" void init_sha256(void);
extern "C" void init_random(void);
extern "C" void initarray(void);
extern "C" void init_socket(void);
extern "C" void initmath(void);
extern "C" void init_heapq(void);
extern "C" void init_sha512(void);
extern "C" void inittime(void);
extern "C" void init_bisect(void);
#if !defined(Q_OS_WIN)
extern "C" void init_posixsubprocess(void);
extern "C" void initgrp(void);
#endif
#if defined(Q_OS_WIN)
extern "C" void initmsvcrt(void);
extern "C" void init_winapi(void);
#endif

static struct _inittab extension_modules[] = {
    {"_json", init_json},
    {"binascii", initbinascii},
    {"_datetime", init_datetime},
    {"_sha1", init_sha1},
    {"_pickle", init_pickle},
    {"pyexpat", initpyexpat},
    {"_md5", init_md5},
    {"_multiprocessing", init_multiprocessing},
    {"_ctypes", init_ctypes},
    {"_ssl", init_ssl},
    {"mmap", initmmap},
    {"select", initselect},
    {"_sha256", init_sha256},
    {"_random", init_random},
    {"array", initarray},
    {"_socket", init_socket},
    {"math", initmath},
    {"_heapq", init_heapq},
    {"_sha512", init_sha512},
    {"time", inittime},
    {"_bisect", init_bisect},
#if !defined(Q_OS_WIN)
    {"_posixsubprocess", init_posixsubprocess},
    {"grp", initgrp},
#endif
#if defined(Q_OS_WIN)
    {"msvcrt", initmsvcrt},
    {"_winapi", init_winapi},
#endif
    {NULL, NULL}
};
#endif

extern int pyqtdeploy_start(int argc, char **argv,
        struct _inittab *extension_modules, const char *main_module,
        const char *entry_point, const char **path_dirs);

int main(int argc, char **argv)
{
    return pyqtdeploy_start(argc, argv, extension_modules, "__main__", NULL, NULL);
}

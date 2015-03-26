#include <Python.h>
#include <QtGlobal>

#if PY_MAJOR_VERSION >= 3
extern "C" PyObject *PyInit_pyexpat(void);
extern "C" PyObject *PyInit__socket(void);
extern "C" PyObject *PyInit__ssl(void);
extern "C" PyObject *PyInit__multiprocessing(void);
extern "C" PyObject *PyInit_QtQuickWidgets(void);
extern "C" PyObject *PyInit_QtWidgets(void);
extern "C" PyObject *PyInit_math(void);
extern "C" PyObject *PyInit__bisect(void);
extern "C" PyObject *PyInit_QtCore(void);
extern "C" PyObject *PyInit__pickle(void);
extern "C" PyObject *PyInit_binascii(void);
extern "C" PyObject *PyInit__json(void);
extern "C" PyObject *PyInit_array(void);
extern "C" PyObject *PyInit_Qt(void);
extern "C" PyObject *PyInit__sha512(void);
extern "C" PyObject *PyInit_mmap(void);
extern "C" PyObject *PyInit_select(void);
extern "C" PyObject *PyInit__random(void);
extern "C" PyObject *PyInit__sha256(void);
extern "C" PyObject *PyInit__sha1(void);
extern "C" PyObject *PyInit_QtGui(void);
extern "C" PyObject *PyInit_QtNetwork(void);
extern "C" PyObject *PyInit__datetime(void);
extern "C" PyObject *PyInit_sip(void);
extern "C" PyObject *PyInit__md5(void);
extern "C" PyObject *PyInit__ctypes(void);
extern "C" PyObject *PyInit_QtQml(void);
extern "C" PyObject *PyInit_QtQuick(void);
extern "C" PyObject *PyInit_time(void);
extern "C" PyObject *PyInit__heapq(void);
#if !defined(Q_OS_WIN)
extern "C" PyObject *PyInit_readline(void);
extern "C" PyObject *PyInit_grp(void);
extern "C" PyObject *PyInit__posixsubprocess(void);
#endif
#if defined(Q_OS_WIN)
extern "C" PyObject *PyInit__winapi(void);
extern "C" PyObject *PyInit_msvcrt(void);
#endif

static struct _inittab extension_modules[] = {
    {"pyexpat", PyInit_pyexpat},
    {"_socket", PyInit__socket},
    {"_ssl", PyInit__ssl},
    {"_multiprocessing", PyInit__multiprocessing},
    {"PyQt5.QtQuickWidgets", PyInit_QtQuickWidgets},
    {"PyQt5.QtWidgets", PyInit_QtWidgets},
    {"math", PyInit_math},
    {"_bisect", PyInit__bisect},
    {"PyQt5.QtCore", PyInit_QtCore},
    {"_pickle", PyInit__pickle},
    {"binascii", PyInit_binascii},
    {"_json", PyInit__json},
    {"array", PyInit_array},
    {"PyQt5.Qt", PyInit_Qt},
    {"_sha512", PyInit__sha512},
    {"mmap", PyInit_mmap},
    {"select", PyInit_select},
    {"_random", PyInit__random},
    {"_sha256", PyInit__sha256},
    {"_sha1", PyInit__sha1},
    {"PyQt5.QtGui", PyInit_QtGui},
    {"PyQt5.QtNetwork", PyInit_QtNetwork},
    {"_datetime", PyInit__datetime},
    {"sip", PyInit_sip},
    {"_md5", PyInit__md5},
    {"_ctypes", PyInit__ctypes},
    {"PyQt5.QtQml", PyInit_QtQml},
    {"PyQt5.QtQuick", PyInit_QtQuick},
    {"time", PyInit_time},
    {"_heapq", PyInit__heapq},
#if !defined(Q_OS_WIN)
    {"readline", PyInit_readline},
    {"grp", PyInit_grp},
    {"_posixsubprocess", PyInit__posixsubprocess},
#endif
#if defined(Q_OS_WIN)
    {"_winapi", PyInit__winapi},
    {"msvcrt", PyInit_msvcrt},
#endif
    {NULL, NULL}
};
#else
extern "C" void initpyexpat(void);
extern "C" void init_socket(void);
extern "C" void init_ssl(void);
extern "C" void init_multiprocessing(void);
extern "C" void initQtQuickWidgets(void);
extern "C" void initQtWidgets(void);
extern "C" void initmath(void);
extern "C" void init_bisect(void);
extern "C" void initQtCore(void);
extern "C" void init_pickle(void);
extern "C" void initbinascii(void);
extern "C" void init_json(void);
extern "C" void initarray(void);
extern "C" void initQt(void);
extern "C" void init_sha512(void);
extern "C" void initmmap(void);
extern "C" void initselect(void);
extern "C" void init_random(void);
extern "C" void init_sha256(void);
extern "C" void init_sha1(void);
extern "C" void initQtGui(void);
extern "C" void initQtNetwork(void);
extern "C" void init_datetime(void);
extern "C" void initsip(void);
extern "C" void init_md5(void);
extern "C" void init_ctypes(void);
extern "C" void initQtQml(void);
extern "C" void initQtQuick(void);
extern "C" void inittime(void);
extern "C" void init_heapq(void);
#if !defined(Q_OS_WIN)
extern "C" void initreadline(void);
extern "C" void initgrp(void);
extern "C" void init_posixsubprocess(void);
#endif
#if defined(Q_OS_WIN)
extern "C" void init_winapi(void);
extern "C" void initmsvcrt(void);
#endif

static struct _inittab extension_modules[] = {
    {"pyexpat", initpyexpat},
    {"_socket", init_socket},
    {"_ssl", init_ssl},
    {"_multiprocessing", init_multiprocessing},
    {"PyQt5.QtQuickWidgets", initQtQuickWidgets},
    {"PyQt5.QtWidgets", initQtWidgets},
    {"math", initmath},
    {"_bisect", init_bisect},
    {"PyQt5.QtCore", initQtCore},
    {"_pickle", init_pickle},
    {"binascii", initbinascii},
    {"_json", init_json},
    {"array", initarray},
    {"PyQt5.Qt", initQt},
    {"_sha512", init_sha512},
    {"mmap", initmmap},
    {"select", initselect},
    {"_random", init_random},
    {"_sha256", init_sha256},
    {"_sha1", init_sha1},
    {"PyQt5.QtGui", initQtGui},
    {"PyQt5.QtNetwork", initQtNetwork},
    {"_datetime", init_datetime},
    {"sip", initsip},
    {"_md5", init_md5},
    {"_ctypes", init_ctypes},
    {"PyQt5.QtQml", initQtQml},
    {"PyQt5.QtQuick", initQtQuick},
    {"time", inittime},
    {"_heapq", init_heapq},
#if !defined(Q_OS_WIN)
    {"readline", initreadline},
    {"grp", initgrp},
    {"_posixsubprocess", init_posixsubprocess},
#endif
#if defined(Q_OS_WIN)
    {"_winapi", init_winapi},
    {"msvcrt", initmsvcrt},
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

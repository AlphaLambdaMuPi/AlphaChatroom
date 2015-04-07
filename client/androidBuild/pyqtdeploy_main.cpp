#include <Python.h>
#include <QtGlobal>

#if PY_MAJOR_VERSION >= 3
extern "C" PyObject *PyInit__socket(void);
extern "C" PyObject *PyInit_select(void);
extern "C" PyObject *PyInit__datetime(void);
extern "C" PyObject *PyInit_time(void);
extern "C" PyObject *PyInit__pickle(void);
extern "C" PyObject *PyInit__ctypes(void);
extern "C" PyObject *PyInit__random(void);
extern "C" PyObject *PyInit_Qt(void);
extern "C" PyObject *PyInit__sha512(void);
extern "C" PyObject *PyInit_QtQuickWidgets(void);
extern "C" PyObject *PyInit__sha1(void);
extern "C" PyObject *PyInit_QtNetwork(void);
extern "C" PyObject *PyInit__json(void);
extern "C" PyObject *PyInit__md5(void);
extern "C" PyObject *PyInit_QtCore(void);
extern "C" PyObject *PyInit__multiprocessing(void);
extern "C" PyObject *PyInit_mmap(void);
extern "C" PyObject *PyInit__ssl(void);
extern "C" PyObject *PyInit_math(void);
extern "C" PyObject *PyInit__bisect(void);
extern "C" PyObject *PyInit_QtQml(void);
extern "C" PyObject *PyInit_pyexpat(void);
extern "C" PyObject *PyInit_QtWidgets(void);
extern "C" PyObject *PyInit_binascii(void);
extern "C" PyObject *PyInit_QtQuick(void);
extern "C" PyObject *PyInit_QtGui(void);
extern "C" PyObject *PyInit__sha256(void);
extern "C" PyObject *PyInit_array(void);
extern "C" PyObject *PyInit_sip(void);
extern "C" PyObject *PyInit__heapq(void);
#if !defined(Q_OS_WIN)
extern "C" PyObject *PyInit_grp(void);
extern "C" PyObject *PyInit_readline(void);
extern "C" PyObject *PyInit__posixsubprocess(void);
#endif
#if defined(Q_OS_WIN)
extern "C" PyObject *PyInit_msvcrt(void);
extern "C" PyObject *PyInit__winapi(void);
#endif

static struct _inittab extension_modules[] = {
    {"_socket", PyInit__socket},
    {"select", PyInit_select},
    {"_datetime", PyInit__datetime},
    {"time", PyInit_time},
    {"_pickle", PyInit__pickle},
    {"_ctypes", PyInit__ctypes},
    {"_random", PyInit__random},
    {"PyQt5.Qt", PyInit_Qt},
    {"_sha512", PyInit__sha512},
    {"PyQt5.QtQuickWidgets", PyInit_QtQuickWidgets},
    {"_sha1", PyInit__sha1},
    {"PyQt5.QtNetwork", PyInit_QtNetwork},
    {"_json", PyInit__json},
    {"_md5", PyInit__md5},
    {"PyQt5.QtCore", PyInit_QtCore},
    {"_multiprocessing", PyInit__multiprocessing},
    {"mmap", PyInit_mmap},
    {"_ssl", PyInit__ssl},
    {"math", PyInit_math},
    {"_bisect", PyInit__bisect},
    {"PyQt5.QtQml", PyInit_QtQml},
    {"pyexpat", PyInit_pyexpat},
    {"PyQt5.QtWidgets", PyInit_QtWidgets},
    {"binascii", PyInit_binascii},
    {"PyQt5.QtQuick", PyInit_QtQuick},
    {"PyQt5.QtGui", PyInit_QtGui},
    {"_sha256", PyInit__sha256},
    {"array", PyInit_array},
    {"sip", PyInit_sip},
    {"_heapq", PyInit__heapq},
#if !defined(Q_OS_WIN)
    {"grp", PyInit_grp},
    {"readline", PyInit_readline},
    {"_posixsubprocess", PyInit__posixsubprocess},
#endif
#if defined(Q_OS_WIN)
    {"msvcrt", PyInit_msvcrt},
    {"_winapi", PyInit__winapi},
#endif
    {NULL, NULL}
};
#else
extern "C" void init_socket(void);
extern "C" void initselect(void);
extern "C" void init_datetime(void);
extern "C" void inittime(void);
extern "C" void init_pickle(void);
extern "C" void init_ctypes(void);
extern "C" void init_random(void);
extern "C" void initQt(void);
extern "C" void init_sha512(void);
extern "C" void initQtQuickWidgets(void);
extern "C" void init_sha1(void);
extern "C" void initQtNetwork(void);
extern "C" void init_json(void);
extern "C" void init_md5(void);
extern "C" void initQtCore(void);
extern "C" void init_multiprocessing(void);
extern "C" void initmmap(void);
extern "C" void init_ssl(void);
extern "C" void initmath(void);
extern "C" void init_bisect(void);
extern "C" void initQtQml(void);
extern "C" void initpyexpat(void);
extern "C" void initQtWidgets(void);
extern "C" void initbinascii(void);
extern "C" void initQtQuick(void);
extern "C" void initQtGui(void);
extern "C" void init_sha256(void);
extern "C" void initarray(void);
extern "C" void initsip(void);
extern "C" void init_heapq(void);
#if !defined(Q_OS_WIN)
extern "C" void initgrp(void);
extern "C" void initreadline(void);
extern "C" void init_posixsubprocess(void);
#endif
#if defined(Q_OS_WIN)
extern "C" void initmsvcrt(void);
extern "C" void init_winapi(void);
#endif

static struct _inittab extension_modules[] = {
    {"_socket", init_socket},
    {"select", initselect},
    {"_datetime", init_datetime},
    {"time", inittime},
    {"_pickle", init_pickle},
    {"_ctypes", init_ctypes},
    {"_random", init_random},
    {"PyQt5.Qt", initQt},
    {"_sha512", init_sha512},
    {"PyQt5.QtQuickWidgets", initQtQuickWidgets},
    {"_sha1", init_sha1},
    {"PyQt5.QtNetwork", initQtNetwork},
    {"_json", init_json},
    {"_md5", init_md5},
    {"PyQt5.QtCore", initQtCore},
    {"_multiprocessing", init_multiprocessing},
    {"mmap", initmmap},
    {"_ssl", init_ssl},
    {"math", initmath},
    {"_bisect", init_bisect},
    {"PyQt5.QtQml", initQtQml},
    {"pyexpat", initpyexpat},
    {"PyQt5.QtWidgets", initQtWidgets},
    {"binascii", initbinascii},
    {"PyQt5.QtQuick", initQtQuick},
    {"PyQt5.QtGui", initQtGui},
    {"_sha256", init_sha256},
    {"array", initarray},
    {"sip", initsip},
    {"_heapq", init_heapq},
#if !defined(Q_OS_WIN)
    {"grp", initgrp},
    {"readline", initreadline},
    {"_posixsubprocess", init_posixsubprocess},
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
